"""Sala do inventário na casca DSGov (templates/inventario_sala.html + static/js/sala.js) — da paridade
DSGov × Tabler: o desenho completo do Tabler (três seções com contador, faixa de leitura presa, busca, Todos,
Lista/Quadros, menu ⋮, ficha do bem, lote que só aparece com bens marcados) com componentes do padrão DSGov."""
import json
import re
from pathlib import Path

from tests.conftest import SENHA_PADRAO, logar
from tests.test_app import _abrir

RAIZ = Path(__file__).resolve().parent.parent
SALA = "01 - SALA CCI"


def _cenario(cliente, comissao=("Fulano", "Beltrana")):
    """1001 lido aqui (localizado); 1002 lido em outra sala (pendente aqui); 1004 de outra sala lido aqui
    (divergente); 1003 não ativo lido aqui (em Divergentes, fora da contagem)."""
    eid = _abrir(cliente, comissao)
    url = f"/inventario/{eid}/sala/{SALA}"
    assert cliente.post(f"{url}/ler", json={"numero": "1001"}).get_json()["situacao"] == "localizado"
    assert cliente.post(f"/inventario/{eid}/sala/99 - SEM MAPA/ler", json={"numero": "1002"}).status_code == 200
    assert cliente.post(f"{url}/ler", json={"numero": "1004"}).get_json()["situacao"] == "divergente"
    assert cliente.post(f"{url}/ler", json={"numero": "1003"}).status_code == 200
    return eid, url


def _secao(html, nome):
    return html.split(f'id="secao-{nome}"', 1)[1].split('class="tab-panel', 1)[0].split('<template id="modelo-lista">')[0]


def _json(html, id_):
    return json.loads(html.split(f'<script type="application/json" id="{id_}">')[1].split("</script>")[0])


def test_sala_dsgov_tres_secoes_em_br_tab_com_contador(cliente):
    eid, url = _cenario(cliente)
    html = cliente.get(url).text
    assert "govbr-ds/core.min.css" in html and ' style="' not in html.split("<body")[1]
    # pré-título e título
    assert 'text-uppercase text-gray-60 mb-1">Inventário · sala</p>' in html and f'<h1 class="mb-0">{SALA}</h1>' in html
    # br-tab com contador; Pendentes aberta; "verificar" em Divergentes quando há algum
    assert '<div class="br-tab" data-counter="true" id="contadores" data-total="2">' in html
    assert 'id="n-pendentes">1<' in html and 'id="n-divergentes">1<' in html and 'id="n-localizados">1<' in html
    assert '<li class="tab-item active" title="Pendentes" role="presentation">' in html
    assert 'data-panel="secao-pendentes" aria-controls="secao-pendentes" aria-selected="true"' in html
    assert '<div class="tab-panel active" id="secao-pendentes"' in html and '<div class="tab-panel" id="secao-divergentes"' in html
    assert '<span class="ml-1" data-papel="alerta-divergentes"><span class="br-tag small bg-warning text-gray-80 d-none d-sm-inline-flex">verificar</span><span class="br-tag status bg-warning d-sm-none" title="verificar"></span></span>' in html
    pend, div, loc = _secao(html, "pendentes"), _secao(html, "divergentes"), _secao(html, "localizados")
    # bem da sala lido em outra sala: continua Pendente, com "Encontrado em" e quem leu
    assert 'data-bem="1002"' in pend and "Encontrado em 99 - SEM MAPA" in pend and "Lido por Fulano em" in pend and ">Pendente<" in pend
    assert 'data-bem="1002"' not in div + loc
    # divergentes misturados nas seções (não há mais a tabela "Trazidos")
    assert 'data-bem="1004"' in div and "Cadastrado em 99 - SEM MAPA" in div and ">Divergente<" in div and "Lido aqui por Fulano" in div
    assert 'data-bem="1003"' in div and ">Não ativo<" in div and "BAIXADO" in div
    assert 'data-bem="1001"' in loc and ">Localizado<" in loc and 'data-bem="1001"' not in pend + div
    assert "Trazidos de outras salas" not in html and 'id="dados-trazidos"' not in html
    # cada bem nas duas visualizações; sem JS: lista no celular, quadros a partir de md
    for n in (1001, 1002, 1003, 1004):
        assert html.count(f'data-bem="{n}" data-copia="lista"') == 1 and html.count(f'data-bem="{n}" data-copia="grade"') == 1
        assert f'<a class="text-weight-bold" href="/bem?numero={n}" data-papel="numero"' in html
    assert '<div class="d-md-none" data-papel="caixa-lista">' in html and 'class="row d-none d-md-flex" id="grade-pendentes"' in html


def test_sala_dsgov_faixa_busca_visao_e_mensagens_de_vazio(cliente):
    eid = _abrir(cliente)
    html = cliente.get(f"/inventario/{eid}/sala/{SALA}").text
    # faixa de leitura: campo, câmera, digitar, aviso e contadores (presa no topo pelo patrimonio.css)
    faixa = html.split('id="faixa-leitura"')[1].split('class="br-tab"')[0]
    assert 'id="leitura" type="text" inputmode="none"' in faixa and 'id="btn-camera"' in faixa and 'id="btn-digitar"' in faixa
    assert 'id="leitor-camera"' in faixa and 'id="aviso"' in faixa and 'id="btn-sobra"' in faixa
    for nome in ("pendentes", "divergentes", "localizados"):
        assert f'data-contador="{nome}"' in faixa
    # busca, Todos e Lista/Quadros
    assert 'id="busca-bens" type="search"' in html and 'id="busca-contagem" aria-live="polite"' in html
    assert '<div class="br-checkbox mr-3"><input id="selecionar-todos" type="checkbox"' in html
    assert 'data-visao="lista"' in html and 'data-visao="quadros"' in html
    # nada lido: Pendentes cheia; Divergentes e Localizados com a mensagem de vazio (br-message, não hidden)
    assert re.search(r'<div class="br-message info d-none" data-papel="vazio">.*?Nenhum bem pendente\.', _secao(html, "pendentes"), re.S)
    assert '<div class="br-message info" data-papel="vazio">' in _secao(html, "divergentes") and "Nenhum bem divergente." in _secao(html, "divergentes")
    assert "Nenhum bem localizado ainda." in _secao(html, "localizados")
    assert re.search(r'data-papel="caixa-lista" hidden>', _secao(html, "localizados"))
    assert '<span class="ml-1 d-none" data-papel="alerta-divergentes">' in html   # sem divergente: alerta escondido


def test_sala_dsgov_menu_do_bem_e_lote(cliente, monkeypatch):
    import fotos
    for v in fotos.VARIAVEIS:
        monkeypatch.setenv(v, "x")
    eid, url = _cenario(cliente)
    html = cliente.get(url).text
    # menu ⋮: br-list role=menu acionado por data-toggle="dropdown" (o sala.js inicializa, sem o dsgov.js)
    menu = html.split('data-target="menu-grade-1001"', 1)[1].split("</div>", 1)[0]
    assert 'data-toggle="dropdown" data-target="menu-lista-1001" data-dsgov-init="1"' in html
    assert '<div class="br-list" id="menu-grade-1001" role="menu" data-papel="menu-bem" hidden>' in menu
    for acao, texto in (("detalhes", "Detalhes"), ("ler", "Registrar leitura nesta sala"), ("desfazer", "Desfazer leitura")):
        assert f'data-acao="{acao}"' in menu and texto in menu
    assert '<label class="br-item" for="foto-bem" role="menuitem" tabindex="0" data-acao="foto" aria-label="Nova foto do bem 1001">' in menu
    # 1002 foi lido em outra sala: Desfazer aparece; sem leitura nenhuma (sala sem leitura) Desfazer fica escondido
    assert 'class="br-item text-danger" type="button" role="menuitem" data-acao="desfazer"' in html.split('id="menu-lista-1002"', 1)[1].split("</div>", 1)[0]
    # lote: barra presa embaixo, escondida até marcar; os números vão por campos ocultos montados no envio
    assert '<div class="br-card mb-3 d-none" id="barra-lote">' in html
    lote = html.split('id="barra-lote"')[1].split("</form>")[0]
    assert 'id="form-lote"' in lote and 'id="n-selecionados">0<' in lote and 'value="marcar"' in lote and 'value="desmarcar"' in lote
    assert 'name="numeros"' not in html.split('<template id="modelo-lista">')[0]
    assert html.count('data-papel="selecao"') >= 8   # 4 bens × 2 cópias (mais as dos modelos)
    # o POST do lote continua o mesmo
    r = cliente.post(f"{url}/lote", data={"acao": "marcar", "numeros": ["1002"]}, follow_redirects=True)
    assert b"1 bem(ns) marcado(s)" in r.data


def test_sala_dsgov_ficha_do_bem_em_br_modal(cliente, monkeypatch):
    import db, fotos, inventario
    for v in fotos.VARIAVEIS:
        monkeypatch.setenv(v, "x")
    eid, url = _cenario(cliente)
    inventario.adicionar_foto(db.conectar(), eid, 1001, lambda c: "https://x/1.webp")
    inventario.adicionar_foto(db.conectar(), eid, 1001, lambda c: "https://x/2.webp")
    html = cliente.get(url).text
    modal = html.split('id="scrim-bem"')[1].split('<h2 class="text-up-01 mt-4 mb-2">Sobras')[0]
    assert '<div class="br-scrim-util foco" id="scrim-bem" data-scrim="true" hidden>' in html
    assert '<div class="br-modal dsgov-modal-largo" role="dialog" aria-modal="true" aria-labelledby="modal-bem-titulo">' in modal
    for rotulo in ("Descrição", "Complemento", "Classificação", "Situação", "Localização", "Data de entrada", "Valor de compra",
                   "Valor atual", "Centro de custo", "Responsável individual", "Sala da leitura", "Lido por", "Data/hora da leitura"):
        assert f"<dt>{rotulo}</dt>" in modal
    # leitura editável: conservação (br-radio), quem usa e observação (br-input); fotos; ações
    assert modal.count('name="det-conservacao" type="radio"') == 5 and 'value="Inservível" data-campo="conservacao"' in modal
    assert 'id="det-quem-usa" type="text" data-campo="quem_usa"' in modal and 'id="det-observacao" type="text" data-campo="observacao"' in modal
    assert 'id="det-fotos"' in modal and 'for="foto-bem" id="det-nova-foto" data-acao="foto"' in modal
    assert 'id="det-ler"' in modal and 'id="det-desfazer"' in modal and 'id="det-concluir"' in modal
    # fichas e configuração para o sala.js
    f = _json(html, "fichas")
    assert [(x["nfoto"], x["url"]) for x in f["1001"]["fotos"]] == [(1, "https://x/1.webp"), (2, "https://x/2.webp")]
    assert f["1004"]["secao"] == "divergente" and f["1002"]["secao"] == "pendente" and f["1001"]["secao"] == "localizado"
    cfg = _json(html, "sala-config")
    assert cfg == {"url_ler": f"/inventario/{eid}/sala/01%20-%20SALA%20CCI/ler", "url_leitura": f"/inventario/{eid}/leitura/0",
                   "url_foto_excluir": f"/inventario/{eid}/leitura/0/foto/0/excluir", "fotos_ativas": True, "fechado": False,
                   "pode_bem": True}
    # os POSTs que a ficha usa continuam: campo da leitura, nova foto e excluir foto em JSON
    assert cliente.post(f"/inventario/{eid}/leitura/1001", json={"conservacao": "Bom"}).get_json() == {"ok": True}
    apagadas = []
    monkeypatch.setattr(fotos, "apagar", apagadas.append)
    r = cliente.post(f"/inventario/{eid}/leitura/1001/foto/1/excluir", headers={"Accept": "application/json"})
    assert r.status_code == 200 and r.get_json() == {"fotos": [{"nfoto": 2, "url": "https://x/2.webp"}]} and apagadas == ["https://x/1.webp"]


def test_sala_dsgov_somente_consulta_sem_controles_de_escrita(cliente, dados):
    import usuarios
    usuarios.criar(dados, "chefe", "Chefe", SENHA_PADRAO, ["consulta_inventarios"], trocar_senha=False)
    eid, url = _cenario(cliente)
    cliente.post("/sair"); logar(cliente, "chefe", SENHA_PADRAO)
    html = cliente.get(url).text
    assert 'id="barra-lote"' not in html and 'id="selecionar-todos"' not in html and 'data-papel="selecao"' not in html
    assert 'data-acao="ler"' not in html and 'data-acao="desfazer"' not in html and 'id="det-ler"' not in html
    assert 'data-acao="detalhes"' in html and _json(html, "sala-config")["fechado"] is True
    assert _json(html, "sala-config")["pode_bem"] is False and 'href="/bem?numero=' not in html   # quem não abre a ficha do bem


def test_sala_dsgov_formulario_de_sobra_tem_o_texto_do_upload(cliente, monkeypatch):
    """BRUpload do core: sem um .text-base irmão do componente, anexar a foto dá TypeError (null.style)."""
    import fotos
    for v in fotos.VARIAVEIS:
        monkeypatch.setenv(v, "x")
    eid = _abrir(cliente)
    html = cliente.get(f"/inventario/{eid}/sala/{SALA}").text
    assert re.search(r'<div class="br-upload">.*?<div class="upload-list"></div></div>\s*<p class="text-base mt-1">', html, re.S)
    assert html.count('class="text-base') == 1


def test_sala_dsgov_css_e_js_proprios():
    css = (RAIZ / "static/css/patrimonio.css").read_text(encoding="utf-8")
    assert re.search(r"#faixa-leitura \{ position: sticky; top: var\(--sala-topo", css)
    assert re.search(r"#barra-lote \{ position: sticky; bottom: 0;", css)
    js = (RAIZ / "static/js/sala.js").read_text(encoding="utf-8")
    assert 'var CHAVE_VISAO = "inventario.sala.visao"' in js
    assert re.search(r"try \{ visaoSalva = window\.localStorage\.getItem\(CHAVE_VISAO\); \} catch", js)
    assert re.search(r"try \{ window\.localStorage\.setItem\(CHAVE_VISAO", js)
    assert "filtrar();" in js.split("function aplicar(j)")[1].split("function ler(")[0]   # leitura reconta a busca
    tpl = (RAIZ / "templates/inventario_sala.html").read_text(encoding="utf-8")
    assert "js/sala.js" in tpl and "<script>\n" not in tpl   # o comportamento mora no sala.js, não inline
