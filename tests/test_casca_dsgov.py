"""Casca DSGov (templates/, sem a pasta tabler/): padrão da família CFC e os dois defeitos de exibição corrigidos.

1. `.br-message` define `display: flex` e vence o atributo `hidden` — mensagem escondida usa `d-none`.
2. O BRTable do core 3.7.0 tira do DOM o `<table>` de todo `.br-table` sem `.table-header` (o `_header` é null
   e `_makeResponsiveTable` falha depois de mover a tabela) — todo `.br-table` leva a barra, mesmo vazia.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATES = [p for p in (RAIZ / "templates").rglob("*.html") if "tabler" not in p.parts]


def test_nenhum_componente_com_display_proprio_esconde_por_hidden():
    """br-message e br-button têm display próprio no core.min.css: com `hidden` continuam à vista."""
    achados = []
    for arq in TEMPLATES:
        for tag in re.findall(r"<[a-z]+\b[^>]*>", arq.read_text(encoding="utf-8")):
            classes = re.search(r'class="([^"]*)"', tag)
            if classes and re.search(r"\bbr-(message|button)\b", classes.group(1)) and re.search(r"\shidden(?=[\s/>=])", tag):
                achados.append(f"{arq.name}: {tag[:80]}")
    assert not achados


def test_todo_br_table_tem_table_header():
    achados = []
    for arq in TEMPLATES:
        texto = arq.read_text(encoding="utf-8")
        for m in re.finditer(r'<div class="br-table[^"]*"[^>]*>', texto):
            if not re.match(r'\s*<div class="table-header', texto[m.end():]):
                achados.append(f"{arq.name}: {texto[m.start():m.end() + 60]}")
    assert not achados


def test_sala_do_inventario_tabelas_e_aviso(cliente):
    from tests.test_app import _abrir
    eid = _abrir(cliente)
    cliente.post(f"/inventario/{eid}/sala/01 - SALA CCI/ler", json={"numero": "1001"})
    html = cliente.get(f"/inventario/{eid}/sala/01 - SALA CCI").text
    assert 'id="dados-trazidos"' not in html and 'id="tabela-bens"' not in html     # Bens em seções (br-tab), não em br-table
    assert '<div class="br-table"><div class="table-header"></div><table id="dados-sobras"' not in html   # sem sobras, sem tabela
    assert 'id="aviso" class="br-message mt-2 mb-0 d-none"' in html and 'd-none" type="button" id="btn-sobra"' in html


def test_cabecalho_em_uma_linha_com_menu_do_usuario(cliente):
    html = cliente.get("/").text
    cabecalho = html.split('<header', 1)[1].split('</header>', 1)[0]
    assert 'class="br-header dsgov-cabecalho-linha' in html
    assert 'class="br-sign-in dsgov-usuario"' in cabecalho and 'id="avatar-menu"' in cabecalho
    menu_usuario = cabecalho.split('id="avatar-menu"', 1)[1]
    for texto in ("Meus acessos", "Trocar senha", "Sair"):
        assert texto in menu_usuario
    assert re.search(r'<form method="post" action="/sair"><input type="hidden" name="csrf"', menu_usuario)
    assert 'id="pesquisa-q"' in cabecalho and 'placeholder="Número, descrição, nome ou centro de custo"' in cabecalho
    assert "header-logo" not in cabecalho and "header-sign" not in cabecalho   # sem logo/órgão no topo


def test_menu_da_familia_cfc(cliente):
    html = cliente.get("/cadastros/pessoas").text
    menu = html.split('id="main-navigation"', 1)[1].split('class="menu-scrim"', 1)[0]
    assert re.search(r'<div class="menu-title">\s*<img src="/static/img/logo-cfc.png"', menu)
    assert re.search(r'<div class="menu-footer">\s*<div class="menu-info">', menu)
    itens = re.findall(r'<span class="content">([^<]+)</span>', menu)
    assert itens[0] == "Início"
    pastas = re.findall(r'<div class="menu-folder[^"]*">\s*<a class="menu-item" href="([^"]+)"', menu)
    assert pastas and set(pastas) == {"javascript:void(0)"}
    assert '<div class="menu-folder active">' in menu
    assert re.search(r'class="menu-item active" href="/cadastros/pessoas"[^>]*aria-current="page"', menu)


def test_rodape_da_familia_cfc(cliente):
    html = cliente.get("/").text
    rodape = html.split('<footer class="br-footer" id="footer">', 1)[1].split("</footer>", 1)[0]
    assert 'class="dsgov-rodape"' in rodape and 'class="dsgov-rodape-links"' in rodape
