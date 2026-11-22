"""Robô do SPW: entra no sistema de patrimônio, exporta a relação de bens e importa em termos.db.

Roda dentro do container `robo` do compose (alvo `robo` do Dockerfile, com SeleniumBase + Playwright + xlrd): pela fila
(atender_pedidos.py, pedido tipo "spw") ou na hora, fora da fila, com

    docker compose exec -T robo python importar_spw.py

(é o que scripts/atualizar_base.sh chama; ver README "Robô do SPW"). Segredos em
secrets/spw.env, montado em /app/secrets (SPW_USUARIO, SPW_SENHA, SPW_LOGIN_URL, SPW_CONSULTA_URL
e CAPSOLVER_API_KEY para resolver o reCAPTCHA automaticamente).
Resultado de cada execução fica em robo_execucoes e aparece no Início. seleniumbase, playwright e xlrd são
importados dentro das funções: os testes rodam sem eles.
"""
import hashlib
import io
import json
import sqlite3
import sys
import time
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook

import config
import db
import segredos

RAIZ = Path(__file__).resolve().parent
ARQUIVO_ENV = RAIZ / "secrets" / "spw.env"
CHAVES_ENV = ("SPW_USUARIO", "SPW_SENHA", "SPW_LOGIN_URL", "SPW_CONSULTA_URL")
NOME_ARQUIVO = "SPW automático"
PASTA_SPW = "spw"            # dentro de config.pasta_dados(): ultimo.xls e erro.png


class RoboErro(Exception):
    """Erro previsto do robô; a mensagem vai para robo_execucoes e para o Início."""


# Usada por atender_pedidos.executar_spw para reconhecer login recusado sem repetir o texto.
MSG_LOGIN_RECUSADO = "login no SPW não chegou ao menu (usuário/senha?)"


def resolver_captcha(env: dict, website_url: str, site_key: str) -> str:
    """Resolve reCAPTCHA v2 pela API REST do CapSolver, como no teste assistido."""
    import requests

    client_key = env.get("CAPSOLVER_API_KEY")
    if not client_key:
        raise RoboErro("CAPSOLVER_API_KEY não configurada no spw.env")

    def consultar(operacao, payload):
        try:
            resposta = requests.post(
                f"https://api.capsolver.com/{operacao}", json=payload, timeout=20,
            )
            resposta.raise_for_status()
            resultado = resposta.json()
        except (requests.RequestException, ValueError):
            raise RoboErro("falha de comunicação com o CapSolver; nada foi enviado ao SPW") from None
        if not isinstance(resultado, dict):
            raise RoboErro("resposta inválida do CapSolver")
        if resultado.get("errorId") != 0 or resultado.get("status") == "failed":
            raise RoboErro("o CapSolver não conseguiu resolver o CAPTCHA; confira a chave e o saldo do serviço")
        return resultado

    tarefa = consultar("createTask", {
        "clientKey": client_key,
        "task": {"type": "ReCaptchaV2TaskProxyLess", "websiteURL": website_url, "websiteKey": site_key},
    })
    task_id = tarefa.get("taskId")
    if not task_id:
        raise RoboErro("o CapSolver não retornou o identificador da tarefa")
    limite = time.monotonic() + 120
    while time.monotonic() < limite:
        time.sleep(2)
        resultado = consultar("getTaskResult", {"clientKey": client_key, "taskId": task_id})
        if resultado.get("status") == "ready":
            token = (resultado.get("solution") or {}).get("gRecaptchaResponse")
            if not isinstance(token, str) or not token.strip():
                raise RoboErro("o CapSolver retornou uma solução sem token")
            return token
    raise RoboErro("tempo excedido aguardando a resolução do CapSolver")


def ler_env(caminho: Path | None = None) -> dict:
    """`caminho` omitido usa o ARQUIVO_ENV do módulo NA HORA da chamada (não travado na importação),
    para os testes poderem trocá-lo com monkeypatch.setattr(importar_spw, "ARQUIVO_ENV", ...)."""
    caminho = caminho or ARQUIVO_ENV
    try:
        return segredos.ler_env(caminho, CHAVES_ENV)
    except segredos.SegredoAusente as e:
        msg = str(e).replace(f"secrets/{caminho.name}", "secrets/spw.env", 1)
        raise RoboErro(msg)


# o ramo numérico (repr(float(v))) é proposital: faz o float do xlrd e o int do openpyxl darem o
# mesmo hash; não trocar por db._texto (que formataria os dois como texto de forma diferente).
def _normalizar(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%d/%m/%Y")
    if isinstance(v, (int, float)):
        return repr(float(v))
    return " ".join(str(v).split())


def hash_linhas(linhas: list[list]) -> str:
    """SHA-256 das linhas (cabeçalho incluído) com os valores normalizados como db._texto faria."""
    h = hashlib.sha256()
    for linha in linhas:
        h.update("\t".join(_normalizar(c) for c in linha).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def linhas_para_xlsx(linhas: list[list]) -> io.BytesIO:
    """Planilha no formato que db.importar_bens aceita: cabeçalho na linha 1, uma aba."""
    wb = Workbook()
    ws = wb.active
    for linha in linhas:
        ws.append(list(linha))
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def executar(conn, baixar=None, agora=None, env: dict | None = None) -> dict:
    """Fluxo completo de uma execução; nunca levanta: devolve {"resultado", "mensagem", "importacao_id"}.
    baixar(env) devolve as linhas do export (cabeçalho primeiro); os testes injetam listas prontas.
    `env` vem do trabalhador: pela fila do site é a credencial de quem pediu (atender_pedidos.executar_spw);
    sem `env` (cron / scripts/atualizar_base.sh) baixar() é chamado sem argumento e lê spw.env inteiro sozinho."""
    baixar = baixar or baixar_e_ler
    agora = agora or db._agora
    iniciado = agora()
    try:
        linhas = baixar(env) if env is not None else baixar()
        cabecalho = [db._texto(c) for c in (linhas[0] if linhas else [])]
        faltando = [c for c in db.COLUNAS_EXPORT if c not in cabecalho]
        if faltando:
            raise RoboErro("cabeçalho do SPW mudou: faltam " + ", ".join(faltando))
        atuais = conn.execute("SELECT count(*) FROM bens").fetchone()[0]
        if atuais and len(linhas) - 1 < atuais * 0.9:
            raise RoboErro(f"export do SPW veio curto: {len(linhas) - 1} bens contra {atuais} na base; "
                           "confira no SPW e use Atualizar base se a queda for real")
        h = hash_linhas(linhas)
        if h == db.ultimo_hash_robo(conn):
            mensagem = f"{len(linhas) - 1} bens no export, nada mudou"
            db.registrar_execucao_robo(conn, iniciado, "sem_mudanca", hash=h, mensagem=mensagem)
            return {"resultado": "sem_mudanca", "mensagem": mensagem, "importacao_id": None}
        r = db.importar_bens(conn, linhas_para_xlsx(linhas), nome_arquivo=NOME_ARQUIVO)
        mensagem = (f"{r['total']} bens ({r['ativos']} ativos): {r['novos']} novo(s), {r['removidos']} removido(s), "
                    f"{r['movidos']} movido(s), {r['situacao']} com situação alterada")
        db.registrar_execucao_robo(conn, iniciado, "importado", hash=h, importacao_id=r["importacao_id"], mensagem=mensagem)
        return {"resultado": "importado", "mensagem": mensagem, "importacao_id": r["importacao_id"]}
    except Exception as exc:
        mensagem = (str(exc) or type(exc).__name__)[:500]
        try:
            db.registrar_execucao_robo(conn, iniciado, "erro", mensagem=mensagem)
        except sqlite3.Error:
            pass                                    # banco travado: fica só no log do cron
        return {"resultado": "erro", "mensagem": mensagem, "importacao_id": None}


def _esperar(condicao, segundos: float) -> bool:
    """Aguarda uma condição, tolerando falhas transitórias durante a navegação."""
    limite = time.monotonic() + segundos
    while True:
        try:
            if condicao():
                return True
        except Exception:
            pass
        restante = limite - time.monotonic()
        if restante <= 0:
            return False
        time.sleep(min(0.5, restante))


def baixar_export(env: dict, destino: Path) -> Path:
    """Login com CapSolver e exportação Excel/Detalhado, conforme o teste assistido.

    O SeleniumBase dirige o login em CDP puro; só depois o Playwright assume a consulta.
    Em erro, salva a tela e o HTML ao lado do destino para diagnóstico dos seletores.
    O chamador mantém robo.lock durante o uso do perfil persistente do Chrome.
    """
    from seleniumbase import sb_cdp
    from playwright.sync_api import sync_playwright

    P = "#ContentPlaceHolder1_"
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    perfil = destino.parent / "chrome-perfil"
    # Sob robo.lock, remove travas deixadas pelo hostname de um container anterior.
    for trava in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
        (perfil / trava).unlink(missing_ok=True)
    sb = sb_cdp.Chrome(env["SPW_LOGIN_URL"], user_data_dir=str(perfil))
    try:
        try:
            if not _esperar(lambda: sb.evaluate("document.readyState") == "complete", 30):
                raise RoboErro("a página de login do SPW não terminou de carregar; nada foi enviado")
            sb.type(P + "txtUsuario_I", env["SPW_USUARIO"])
            sb.type(P + "txtSenha_I", env["SPW_SENHA"])
            site_key = sb.get_attribute("[data-sitekey]", "data-sitekey")
            if not site_key:
                raise RoboErro("não foi possível identificar o reCAPTCHA do SPW; nada foi enviado")
            token = resolver_captcha(env, sb.get_current_url(), site_key)
            # CDPMethods.evaluate recebe somente o JavaScript; o token vai escapado como JSON.
            sb.evaluate("""
                (() => {
                    const el = document.getElementById('g-recaptcha-response');
                    const token = %s;
                    if (el) {
                        el.innerHTML = token;
                        el.value = token;
                    }
                })()
            """ % json.dumps(token))
            if not _esperar(lambda: sb.evaluate("grecaptcha.getResponse().length") > 0, 15):
                raise RoboErro("o reCAPTCHA do login do SPW não liberou após o CapSolver; nada foi enviado")
            if (sb.evaluate(f"document.querySelector('{P}txtUsuario_I').value") != env["SPW_USUARIO"]
                    or sb.evaluate(f"document.querySelector('{P}txtSenha_I').value.length") != len(env["SPW_SENHA"])):
                raise RoboErro("usuário/senha sumiram dos campos do login do SPW; nada foi enviado")
            sb.click(P + "btnEntrar_I")
            if not _esperar(lambda: "MenuChamador" in sb.get_current_url(), 60):
                raise RoboErro(MSG_LOGIN_RECUSADO + ": " + sb.get_current_url())
        except Exception:
            try:
                sb.save_screenshot(str(destino.parent / "erro.png"))
            except Exception:
                pass
            raise

        # O loop do SeleniumBase não pode rodar dentro do sync_playwright.
        endpoint = sb.get_endpoint_url()
        with sync_playwright() as p:
            pagina = p.chromium.connect_over_cdp(endpoint).contexts[0].pages[0]
            try:
                pagina.goto(env["SPW_CONSULTA_URL"], wait_until="networkidle", timeout=60000)
                pagina.click("button[onclick*='modalExportacao']")
                pagina.wait_for_selector("#modalExportacao", state="visible", timeout=30000)
                pagina.select_option(P + "cboArquivo", label="Excel", force=True)
                pagina.select_option(P + "cboModeloExportacao", label="Detalhado", force=True)
                if (pagina.eval_on_selector(P + "cboArquivo", "e => e.value") != "0"
                        or pagina.eval_on_selector(P + "cboModeloExportacao", "e => e.value") != "0"):
                    raise RoboErro("modal de exportação do SPW não ficou em Excel/Detalhado")
                with pagina.expect_download(timeout=300000) as dl:
                    pagina.click(P + "ASPxButton3")
                dl.value.save_as(destino)
            except Exception:
                try:
                    pagina.screenshot(path=str(destino.parent / "erro.png"), full_page=True)
                    (destino.parent / "erro.html").write_text(pagina.content(), encoding="utf-8")
                except Exception:
                    pass
                raise
    finally:
        sb.quit()
    if destino.stat().st_size < 1000:
        raise RoboErro(f"export do SPW veio vazio ({destino.stat().st_size} bytes)")
    return destino


def ler_xls(caminho: Path) -> list[list]:
    """Lê a planilha do SPW e devolve as linhas a partir do cabeçalho 'Número Bem'. O export sempre veio .xls (BIFF);
    se o SPW passar a mandar .xlsx (um zip, começa com PK), lê com openpyxl, pelo conteúdo e não pela extensão."""
    with open(caminho, "rb") as f:
        if f.read(4) == b"PK\x03\x04":
            from openpyxl import load_workbook
            f.seek(0)
            wb = load_workbook(f, read_only=True, data_only=True)
            linhas = [list(linha) for linha in wb.worksheets[0].iter_rows(values_only=True)]
            wb.close()
        else:
            linhas = _ler_biff(caminho)
    for i, linha in enumerate(linhas):
        if linha and db._texto(linha[0]) == "Número Bem":
            return linhas[i:]
    raise RoboErro("export do SPW sem a linha de cabeçalho 'Número Bem'")


def _ler_biff(caminho: Path) -> list[list]:
    import xlrd
    wb = xlrd.open_workbook(str(caminho))
    ws = wb.sheet_by_index(0)
    linhas = []
    for i in range(ws.nrows):
        linha = []
        for c in ws.row(i):
            if c.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                linha.append(None)
            elif c.ctype == xlrd.XL_CELL_DATE:
                linha.append(xlrd.xldate_as_datetime(c.value, wb.datemode))
            elif c.ctype == xlrd.XL_CELL_NUMBER:
                linha.append(c.value)
            else:
                linha.append(str(c.value))
        linhas.append(linha)
    return linhas


def baixar_e_ler(env: dict | None = None) -> list[list]:
    pasta = config.pasta_dados() / PASTA_SPW
    return ler_xls(baixar_export(env or ler_env(), pasta / "ultimo.xls"))


def main() -> int:
    inicio = time.monotonic()
    conn = db.conectar()
    try:
        iniciado = db._agora()
        try:
            db.criar_esquema(conn)           # idempotente; garante robo_execucoes mesmo antes do rebuild
            r = executar(conn)
        except Exception as exc:
            mensagem = (str(exc) or type(exc).__name__)[:500]
            try:
                db.registrar_execucao_robo(conn, iniciado, "erro", mensagem=mensagem)
            except sqlite3.Error:
                pass                          # robo_execucoes pode nem existir ainda: fica só no log do cron
            r = {"resultado": "erro", "mensagem": mensagem, "importacao_id": None}
    finally:
        conn.close()
    print(f"{db._agora()} {r['resultado']} {r['mensagem']} ({time.monotonic() - inicio:.0f}s)", flush=True)
    return 0 if r["resultado"] != "erro" else 1


if __name__ == "__main__":
    sys.exit(main())
