"""Teste assistido do SPW (roda dentro do container que scripts/spw_assistido.sh monta; ver README).

O robô abre o login com o mesmo perfil do Chrome do robô, numa tela já compartilhada pelo noVNC, e só começa
quando a pessoa aperta Enter. Se o Google pedir o desafio de imagens, espera a pessoa resolver na tela; depois
entra, exporta pela consulta e valida o arquivo. Com --importar, importa pelo mesmo caminho do robô
(importar_spw.executar: mesmas conferências, registro em robo_execucoes, aparece no Início).
"""
import json
import select
import sys
import time
import requests

import config
import db
import importar_spw
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

P = "#ContentPlaceHolder1_"
ENDERECO = "http://localhost:16080/vnc.html?autoconnect=true&resize=scale"
# o teste segura o lock do robô, que também atende a emissão no SEI: não pode esperar o Enter para sempre
ESPERA_ENTER = 10 * 60


def passo(texto: str) -> None:
    print(time.strftime("%H:%M:%S"), texto, flush=True)


def esperar(condicao, segundos: float) -> bool:
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


def resolver_captcha_capsolver(env: dict, website_url: str, site_key: str) -> str:
    """Resolve o reCAPTCHA usando diretamente a API REST do CapSolver lendo o spw.env."""
    client_key = env.get("CAPSOLVER_API_KEY")
    if not client_key:
        raise importar_spw.RoboErro("CAPSOLVER_API_KEY não configurada no spw.env")

    payload = {
        "clientKey": client_key,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": site_key
        }
    }

    resp = requests.post("https://api.capsolver.com/createTask", json=payload).json()
    if resp.get("errorId") != 0:
        raise importar_spw.RoboErro(f"Erro ao criar tarefa no CapSolver: {resp.get('errorDescription')}")

    task_id = resp.get("taskId")

    for _ in range(30):
        time.sleep(2)
        res_payload = {
            "clientKey": client_key,
            "taskId": task_id
        }
        result = requests.post("https://api.capsolver.com/getTaskResult", json=res_payload).json()

        if result.get("status") == "ready":
            return result["solution"]["gRecaptchaResponse"]
        elif result.get("status") == "failed" or result.get("errorId") != 0:
            raise importar_spw.RoboErro(f"Falha na resolução do CAPTCHA: {result.get('errorDescription')}")

    raise TimeoutError("Tempo excedido aguardando a resolução do CapSolver.")


def baixar(sb, env, destino) -> list[list]:
    """Login (com a pessoa olhando) e exportação; devolve as linhas do export já lidas."""
    if not esperar(lambda: sb.evaluate("document.readyState") == "complete", 30):
        raise TimeoutError("a página de login do SPW não terminou de carregar em 30 s; nada foi enviado")
    print(f"\nTela pronta. Com o túnel aberto, abra no seu navegador:\n  {ENDERECO}\n"
          "Quando estiver vendo o login do SPW, aperte Enter aqui (Ctrl+C cancela; sem Enter em 10 min, desiste).",
          flush=True)
    if not select.select([sys.stdin], [], [], ESPERA_ENTER)[0]:
        raise TimeoutError("ninguém apertou Enter em 10 min; nada foi enviado ao SPW")
    sys.stdin.readline()
    passo("digitando usuário e senha e marcando 'Não sou um robô'")
    sb.type(P + "txtUsuario_I", env["SPW_USUARIO"])
    sb.type(P + "txtSenha_I", env["SPW_SENHA"])

    # --- INTEGRAÇÃO CAPSOLVER (lendo a chave do spw.env) ---
    if env.get("CAPSOLVER_API_KEY"):
        try:
            site_key = sb.get_attribute("[data-sitekey]", "data-sitekey")
            if site_key:
                passo("resolvendo CAPTCHA automaticamente via CapSolver...")
                token_captcha = resolver_captcha_capsolver(env, sb.get_current_url(), site_key)
                sb.evaluate("""
                    (() => {
                        const el = document.getElementById('g-recaptcha-response');
                        const token = %s;
                        if (el) {
                            el.innerHTML = token;
                            el.value = token;
                        }
                    })()
                """ % json.dumps(token_captcha))
        except Exception as e:
            passo(f"Falha ao tentar resolver via CapSolver, aguardando intervenção manual: {e}")
            sb.solve_captcha()
    else:
        sb.solve_captcha()
    # --------------------------------------------------------

    def token_ok():
        return sb.evaluate("grecaptcha.getResponse().length") > 0

    if not esperar(token_ok, 15):
        passo("o Google pediu o desafio de imagens: resolva na tela e clique em Verificar "
              "(não clique em Entrar); esperando até 10 min")
        if not esperar(token_ok, 10 * 60):
            raise importar_spw.RoboErro("ninguém resolveu o desafio em 10 min; nada foi enviado")
    passo("reCAPTCHA liberado; entrando")
    if (sb.evaluate(f"document.querySelector('{P}txtUsuario_I').value") != env["SPW_USUARIO"]
            or sb.evaluate(f"document.querySelector('{P}txtSenha_I').value.length") != len(env["SPW_SENHA"])):
        raise importar_spw.RoboErro("usuário/senha sumiram dos campos do login; nada foi enviado")
    sb.click(P + "btnEntrar_I")
    if not esperar(lambda: "MenuChamador" in sb.get_current_url(), 60):
        raise importar_spw.RoboErro(importar_spw.MSG_LOGIN_RECUSADO + ": " + sb.get_current_url())
    passo("logado; exportando Bens Patrimoniais (Excel/Detalhado)")
    with sync_playwright() as p:
        pagina = p.chromium.connect_over_cdp(sb.get_endpoint_url()).contexts[0].pages[0]
        # mesmos passos de importar_spw.baixar_export: se o SPW mudar a consulta, ajustar os dois
        pagina.goto(env["SPW_CONSULTA_URL"], wait_until="networkidle", timeout=60000)
        pagina.click("button[onclick*='modalExportacao']")
        pagina.wait_for_selector("#modalExportacao", state="visible", timeout=30000)
        pagina.select_option(P + "cboArquivo", label="Excel", force=True)
        pagina.select_option(P + "cboModeloExportacao", label="Detalhado", force=True)
        with pagina.expect_download(timeout=300000) as dl:
            pagina.click(P + "ASPxButton3")
        dl.value.save_as(destino)
    linhas = importar_spw.ler_xls(destino)
    cabecalho = [db._texto(c) for c in linhas[0]]
    faltando = [c for c in db.COLUNAS_EXPORT if c not in cabecalho]
    if faltando:
        raise importar_spw.RoboErro("o export veio sem as colunas " + ", ".join(faltando))
    passo(f"baixado em dados/spw/{destino.name}: {len(linhas) - 1} bens, com todas as colunas")
    return linhas


def main() -> int:
    importar = "--importar" in sys.argv[1:]
    env = importar_spw.ler_env()
    pasta = config.pasta_dados() / importar_spw.PASTA_SPW
    perfil = pasta / "chrome-perfil"
    for trava in ("SingletonLock", "SingletonCookie", "SingletonSocket"):   # ver importar_spw.baixar_export
        (perfil / trava).unlink(missing_ok=True)
    # headed=True: usa a tela :99 já compartilhada, em vez de o SeleniumBase criar uma tela própria
    sb = sb_cdp.Chrome(env["SPW_LOGIN_URL"], user_data_dir=str(perfil), headed=True)
    try:
        linhas = baixar(sb, env, pasta / "assistido.xls")
    except (KeyboardInterrupt, EOFError):
        passo("cancelado")
        return 1
    except TimeoutError as exc:
        passo(str(exc))
        return 1
    except Exception as exc:
        try:
            sb.save_screenshot(str(pasta / "assistido-erro.png"))
        except Exception:
            pass
        passo(f"falhou: {str(exc)[:300] or type(exc).__name__} (tela em dados/spw/assistido-erro.png)")
        return 1
    finally:
        sb.quit()
    if not importar:
        passo("teste concluído; a base não foi alterada (para importar, rode com --importar)")
        return 0
    conn = db.conectar()
    try:
        db.criar_esquema(conn)
        r = importar_spw.executar(conn, baixar=lambda: linhas)
    finally:
        conn.close()
    passo(f"importação: {r['resultado']}: {r['mensagem']}")
    return 0 if r["resultado"] != "erro" else 1


if __name__ == "__main__":
    sys.exit(main())
