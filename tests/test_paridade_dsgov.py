"""Paridade DSGov × Tabler (plano interno).

O comportamento no navegador (filtrar, contar, fixar) foi conferido com Playwright na instância descartável do
manual; aqui ficam as guardas do markup e dos ganchos que esse comportamento usa.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TABELAS_JS = (RAIZ / "static/js/tabelas.js").read_text(encoding="utf-8")
PATRIMONIO_CSS = (RAIZ / "static/css/patrimonio.css").read_text(encoding="utf-8")
TEMPLATES = [p for p in (RAIZ / "templates").rglob("*.html") if "tabler" not in p.parts]


def _antes_do_h1(html):
    return html.split("<h1", 1)[0].rsplit("</nav>", 1)[-1]


# ---------- busca e contagem nas tabelas ----------

def test_tabelas_js_filtra_e_conta_so_no_dsgov():
    corpo = TABELAS_JS.split("function prepararBusca(tabela)", 1)[1].split("/* ---------- inicialização", 1)[0]
    assert "if (TABLER || !componente || !componente.dataset.search) return;" in corpo   # o Tabler segue no astra.js
    assert '.search-bar input[type=search]' in corpo
    assert 'normalize("NFD")' in TABELAS_JS and ".toLowerCase()" in TABELAS_JS          # sem acento, sem maiúsculas
    assert '" registro(s)"' in corpo and '" de "' in corpo                              # "N registro(s)" / "N de M"
    assert "Nenhum registro corresponde à busca." in corpo
    assert 'rodape.className = "table-footer"' in corpo                                 # rodapé do br-table (table.md)
    assert '[data-dismiss="search"]' in corpo and '"Escape"' in corpo                   # fechar devolve as linhas
    assert "dataset.parent" in corpo and "tr.hidden" in corpo                           # "selecionar todas" respeita a busca
    assert "prepararBusca(tabela);" in TABELAS_JS.split("function iniciar(tabela)", 1)[1].split("}", 1)[0]


def test_css_esconde_linha_filtrada_e_estiliza_a_contagem():
    assert ".br-table tr[hidden] { display: none !important; }" in PATRIMONIO_CSS
    assert ".br-table .table-footer .tabela-contagem" in PATRIMONIO_CSS


def test_cabecalho_tabela_tem_os_ganchos_da_busca(cliente):
    html = cliente.get("/centro-custos").text
    assert '<div class="br-table" data-search="data-search">' in html
    assert 'id="campo-busca-centros" type="search"' in html and 'data-dismiss="search"' in html
    assert '<table id="dados-centros" data-tabela>' in html
    assert re.search(r'<script src="/static/js/tabelas\.js\?v=[^"]+" data-aparencia="dsgov"></script>', html)


def test_toda_tabela_com_busca_usa_o_macro():
    """A busca só funciona com a .search-bar do macro; tabela com data-search escrita à mão ficaria sem filtro."""
    achados = [p.name for p in TEMPLATES if p.name != "_macros.html" and 'data-search' in p.read_text(encoding="utf-8")]
    assert not achados


# ---------- acabamentos ----------

def test_pre_titulo_acima_do_h1(cliente):
    for url, pre in [("/termos-emitidos", "Termos de Responsabilidade"), ("/inventario", "Inventário"),
                     ("/cadastros/responsaveis/novo", "Cadastros"), ("/senha", "Minha conta"),
                     ("/administracao", "Administração")]:
        html = cliente.get(url).text
        assert f'<p class="text-down-01 text-weight-semi-bold text-uppercase text-gray-60 mb-1">{pre}</p>' in _antes_do_h1(html), url


def test_pre_titulo_vazio_nao_gera_markup(dados):
    from app import app
    with app.test_request_context():
        macros = app.jinja_env.get_template("_macros.html").module
        assert str(macros.pre_titulo(None)).strip() == ""


def test_eventos_com_barra_de_progresso(cliente):
    from tests.test_app import _abrir
    _abrir(cliente)
    html = cliente.get("/inventario").text
    assert re.search(r'<progress class="dsgov-barra" value="[\d.]+" max="100" aria-labelledby="progresso-\d+">', html)
    assert "dos bens localizados." in html


def test_salas_do_evento_viram_blocos_no_celular(cliente):
    from tests.test_app import _abrir
    eid = _abrir(cliente)
    html = cliente.get(f"/inventario/{eid}").text
    assert '<td data-coluna="sala">' in html and 'data-rotulo="Pendentes"' in html and '<td data-coluna="situacao">' in html
    bloco = PATRIMONIO_CSS.split("@media (max-width: 767.98px) {\n  #dados-salas thead", 1)
    assert len(bloco) == 2 and "#dados-salas td[data-rotulo]::before" in bloco[1]


def test_textos_com_salvar_fixo(cliente):
    html = cliente.get("/textos").text
    assert '<div class="br-card mb-0" id="salvar-textos">' in html
    assert "#salvar-textos { position: sticky; bottom: 0;" in PATRIMONIO_CSS


def test_ajuda_com_sumario_lateral_fixo(cliente):
    html = cliente.get("/ajuda").text
    assert '<nav class="br-card mb-0" id="sumario-ajuda" aria-label="Sumário da ajuda">' in html
    assert "Nesta página" in html
    coluna = html.split('<div class="col-lg-9 order-lg-1">', 1)
    assert len(coluna) == 2 and '<section class="br-card mb-4" id="inicio"' in coluna[1]
    assert "#sumario-ajuda { position: sticky;" in PATRIMONIO_CSS


def test_pesquisa_com_campo_no_corpo(cliente):
    sem_termo = cliente.get("/pesquisa").text
    assert '<form class="mb-4" method="get" action="/pesquisa" role="search">' in sem_termo
    com_termo = cliente.get("/pesquisa?q=cadeira").text
    assert '<form class="mb-4 d-md-none" method="get" action="/pesquisa" role="search">' in com_termo   # só no celular
    assert 'id="busca-pesquisa" name="q" type="search" value="cadeira"' in com_termo
    assert 'id="busca-pesquisa"' not in cliente.get("/pesquisa?ccusto=CCI").text                  # bens de um centro: não


def test_importacao_e_atualizar_base_com_icones(cliente, tmp_path):
    from tests.test_db import xlsx
    import db
    arq = xlsx(tmp_path, [
        [1001, "ATIVO", "CADEIRA", "GIRATÓRIA", "MÓVEIS", "02 - OUTRA", "31/12/1996", 75.94, 64.54],
        [1002, "ATIVO", "NOTEBOOK", "DELL", "EQUIPAMENTOS", "01 - SALA CCI", "06/12/2012", 3000, 1500],
    ])
    with open(arq, "rb") as f:
        cliente.post("/upload", data={"arquivo": (f, "export.xlsx")}, content_type="multipart/form-data")
    html = cliente.get(f"/importacoes/{db.importacoes(db.conectar())[0]['id']}").text
    for icone in ("fa-plus", "fa-minus", "fa-exchange-alt", "fa-sync"):
        assert re.search(rf'<span class="br-tag icon large bg-\w+ mr-3" title="[^"]+" aria-hidden="true"><i class="fas {icone}"', html)
    upload = cliente.get("/upload").text
    assert '<i class="fas fa-boxes mr-2 text-gray-60" aria-hidden="true"></i>Bens' in upload
    assert '<i class="fas fa-address-book mr-2 text-gray-60" aria-hidden="true"></i>Cadastros' in upload


def test_formularios_com_botoes_no_rodape_do_card(cliente):
    from tests.test_app import _abrir
    eid = _abrir(cliente)
    for url in ("/cadastros/responsaveis/novo", f"/inventario/{eid}/comissao", f"/inventario/{eid}/excluir"):
        html = cliente.get(url).text
        form = html.split("<h1", 1)[1].split('<form method="post"', 1)[1].split("</form>", 1)[0]
        assert '<div class="br-card">' in form and '<div class="card-content">' in form, url
        rodape = form.split('<div class="card-footer"><div class="d-flex justify-content-end">', 1)
        assert len(rodape) == 2 and "Cancelar</a>" in rodape[1] and 'type="submit"' in rodape[1], url
        assert "dsgov-acoes-formulario" not in form, url


def test_formulario_de_centro_sem_card_dentro_de_card(cliente):
    html = cliente.get("/cadastros/responsaveis/CCI/editar").text
    form = html.split("<h1", 1)[1].split('<form method="post"', 1)[1].split("</form>", 1)[0]
    assert form.count('class="br-card') == 1 and "Localizações vinculadas" in form


def test_termos_emitidos_mostra_email_como_etiqueta():
    texto = (RAIZ / "templates/termos_emitidos.html").read_text(encoding="utf-8")
    assert ('{% if t.email_enviado_em %}<span class="br-tag bg-success text-pure-0"><span>'
            '{{ t.email_enviado_em[8:10] }}/{{ t.email_enviado_em[5:7] }}/{{ t.email_enviado_em[:4] }}</span></span>') in texto


def test_dsgov_sem_painel_de_aparencia():
    """Decisão do usuário: o painel "Personalizar aparência" (e o modo escuro) é só do Tabler."""
    for arq in TEMPLATES:
        texto = arq.read_text(encoding="utf-8")
        assert "_painel_aparencia" not in texto and "/aparencia" not in texto and "APARENCIA" not in texto, arq.name


# ---------- Análise com os cards de painel.cards_analise ----------

ANALISE_JS = (RAIZ / "static/js/analise.js").read_text(encoding="utf-8")


def test_analise_dsgov_tem_os_seis_cards_novos_com_seletores_e_destaque(cliente):
    import json
    html = cliente.get("/analise").text
    for id_ in ("g-valor", "g-concentracao", "g-compra", "g-cobertura--quantidade", "g-cobertura--valor",
                "g-entradas--quantidade", "g-entradas--compra"):
        assert f'<script type="application/json" id="{id_}"' in html, id_
    for d in ("ccusto", "localizacao", "classificacao", "pessoa"):
        for m in ("quantidade", "valor"):
            assert f'id="g-explorar--{d}--{m}"' in html and f'data-grafico-tabela="g-explorar--{d}--{m}"' in html
    assert 'data-grafico="g-explorar--ccusto--quantidade" data-grafico-base="g-explorar"' in html
    assert 'data-grafico-tabela="g-explorar--ccusto--quantidade">' in html          # a primeira visível
    assert 'data-grafico-tabela="g-explorar--ccusto--valor" hidden>' in html        # as outras escondidas
    # seletores: br-select do padrão DSGov (macro select), um por seletor, a primeira opção marcada
    assert html.count('data-grafico-seletor="g-explorar"') == 2
    assert html.count('data-grafico-seletor="g-entradas"') == 1 and html.count('data-grafico-seletor="g-cobertura"') == 1
    seletor = html.split('data-grafico-seletor="g-explorar">', 1)[1].split("</div>\n  </div>", 1)[0]
    assert '<div class="br-select">' in seletor and 'id="g-explorar-seletor-1_exibicao"' in seletor
    assert 'name="g-explorar-seletor-1" type="radio" value="ccusto" checked="checked"' in seletor
    assert "<select" not in html.split('id="g-valor"')[0].split("Bens no recorte")[-1]   # nada de <select> nativo
    # frase de destaque dos cards de concentração e cobertura
    assert re.search(r'<p class="text-up-01 mb-2"><span class="text-weight-bold">\d+ (bem|bens)</span> \(', html)
    assert "concentram 80% do valor atual" in html or "concentra 80% do valor atual" in html
    assert "com termo em dia</p>" in html
    # conjunto antigo aposentado; JS da Análise carregado depois do tema do padrão DSGov
    for velho in ("g-situacao", "g-centro", "g-faixa", "g-idade", "g-ano", "g-pessoa"):
        assert f'id="{velho}"' not in html, velho
    ordem = [html.index(x) for x in ("echarts.min.js", "echarts-dsgov.js", "js/analise.js")]
    assert ordem == sorted(ordem)
    json.loads(html.split('id="g-explorar--ccusto--valor" data-resumo="')[1].split('">', 1)[1].split("</script>")[0])
    corpo = html.split('id="g-valor"')[1].split("Bens do recorte")[0]
    assert "style=" not in corpo and not re.search(r'class="[^"]*#', corpo)


def test_analise_dsgov_filtro_fixado_sai_do_seletor(cliente):
    html = cliente.get("/analise?situacao=ATIVO&ccusto=CCI").text
    assert 'id="g-explorar--ccusto--quantidade"' not in html and 'id="g-explorar--localizacao--quantidade"' in html
    assert 'value="ccusto"' not in html.split('data-grafico-seletor="g-explorar">', 1)[1].split("Ver dados", 1)[0]


def test_analise_js_complementa_o_tema_da_padrao():
    import graficos
    # cores da classificação: o espelho da paleta do Python é trocado pela categórica oficial (dsgov.graficos)
    for cor in graficos.CORES_CATEGORICA:
        assert f'"{cor}"' in ANALISE_JS, cor
    assert "G.categorica[i % G.categorica.length]" in ANALISE_JS
    assert "moeda: function" in ANALISE_JS and "percentual: function" in ANALISE_JS          # valueFormatter da view
    assert 'typeof op.tooltip.valueFormatter === "string"' in ANALISE_JS
    assert '" mi"' in ANALISE_JS and '" mil"' in ANALISE_JS                                   # eixos abreviados
    assert "legendselectchanged" in ANALISE_JS and 'id = "total-rosca"' in ANALISE_JS          # total no furo
    assert "el.dataset.dsgovGrafico = \"1\"" in ANALISE_JS                                    # o montar() do padrão DSGov pula
    assert "inst.setOption(inst.getOption())" in ANALISE_JS                                   # graficos.md, regra 11
    assert '"onChange"' in ANALISE_JS and "[data-grafico-seletor]" in ANALISE_JS
    assert "ResizeObserver" in ANALISE_JS
    assert not (RAIZ / "static/dsgov/js/echarts-dsgov.js").read_text(encoding="utf-8").count("analise")


def test_cards_antigos_da_analise_sairam_do_codigo():
    import painel
    assert not hasattr(painel, "cards_graficos") and not hasattr(painel, "_grafico")
    for p in TEMPLATES + [RAIZ / "templates/tabler/analise.html"]:
        assert "for g in cards %}" not in p.read_text(encoding="utf-8") or p.name.endswith("inventario_painel.html"), p

