"""Regressões do login automático: API do solver, CDP e interrupção antes de Entrar."""
import json
import sys
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

import importar_spw as robo


def api_falsa(monkeypatch, resultados):
    pendentes = iter(resultados)
    chamadas = []
    class ErroHTTP(Exception):
        pass
    def post(url, *, json, timeout):
        chamadas.append((url, json, timeout))
        resultado = next(pendentes)
        if isinstance(resultado, Exception):
            raise resultado
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: resultado)
    monkeypatch.setitem(sys.modules, 'requests', SimpleNamespace(post=post, RequestException=ErroHTTP))
    relogio = SimpleNamespace(now=0)
    monkeypatch.setattr(robo.time, 'monotonic', lambda: relogio.now)
    monkeypatch.setattr(robo.time, 'sleep', lambda segundos: setattr(relogio, 'now', relogio.now + segundos))
    return chamadas, ErroHTTP


def test_solver_processa_ate_retornar_token(monkeypatch):
    chamadas, _ = api_falsa(monkeypatch, [
        {'errorId': 0, 'taskId': 'tarefa'},
        {'errorId': 0, 'status': 'processing'},
        {'errorId': 0, 'status': 'ready', 'solution': {'gRecaptchaResponse': 'resposta'}},
    ])
    assert robo.resolver_captcha({'CAPSOLVER_API_KEY': 'chave'}, 'https://spw/login', 'site') == 'resposta'
    assert chamadas[0][1]['task']['websiteKey'] == 'site'
    assert chamadas[1][1]['taskId'] == 'tarefa'
    assert all(chamada[2] == 20 for chamada in chamadas)


@pytest.mark.parametrize('resultados,erro', [
    ([{'errorId': 1, 'errorDescription': 'segredo'}], 'não conseguiu'),
    ([{'errorId': 0}], 'identificador'),
    ([{'errorId': 0, 'taskId': 't'}, {'errorId': 0, 'status': 'ready', 'solution': {}}], 'sem token'),
    ([{'errorId': 0, 'taskId': 't'}] + [{'errorId': 0, 'status': 'processing'}] * 60, 'tempo excedido'),
])
def test_solver_falha_sem_expor_segredos(monkeypatch, resultados, erro):
    api_falsa(monkeypatch, resultados)
    with pytest.raises(robo.RoboErro, match=erro) as exc:
        robo.resolver_captcha({'CAPSOLVER_API_KEY': 'segredo'}, 'https://spw/login', 'site')
    assert 'segredo' not in str(exc.value)


def test_solver_exige_chave_sem_chamar_api(monkeypatch):
    chamadas, _ = api_falsa(monkeypatch, [])
    with pytest.raises(robo.RoboErro, match='CAPSOLVER_API_KEY'):
        robo.resolver_captcha({}, 'https://spw/login', 'site')
    assert chamadas == []


def test_solver_erro_de_rede_nao_expoe_segredos(monkeypatch):
    resultados = []
    _, erro = api_falsa(monkeypatch, resultados)
    resultados.append(erro('segredo'))
    with pytest.raises(robo.RoboErro, match='comunicação') as exc:
        robo.resolver_captcha({'CAPSOLVER_API_KEY': 'segredo'}, 'https://spw/login', 'site')
    assert 'segredo' not in str(exc.value)


@pytest.mark.parametrize('falha', [None, 'solver', 'token', 'campos', 'formato'])
def test_login_e_exportacao_sem_intervencao(monkeypatch, tmp_path, falha):
    env = {'SPW_LOGIN_URL': 'https://spw/login', 'SPW_CONSULTA_URL': 'https://spw/consulta',
           'SPW_USUARIO': 'usuario', 'SPW_SENHA': 'senha', 'CAPSOLVER_API_KEY': 'chave'}
    eventos = []
    estado = SimpleNamespace(token=False, entrou=False, playwright=False)
    token = 'resposta"\\\n'
    def solver(*args):
        if falha == 'solver':
            raise robo.RoboErro('solver indisponível')
        return token
    monkeypatch.setattr(robo, 'resolver_captcha', solver)
    monkeypatch.setattr(robo, '_esperar', lambda condicao, segundos: bool(condicao()))
    class Browser:
        def type(self, seletor, valor):
            eventos.append(('type', seletor))
        def get_attribute(self, *args):
            return 'site'
        def get_current_url(self):
            return 'https://spw/MenuChamador' if estado.entrou else env['SPW_LOGIN_URL']
        def evaluate(self, script):  # CDP aceita um só argumento.
            assert not estado.playwright
            if script == 'document.readyState':
                return 'complete'
            if script == 'grecaptcha.getResponse().length':
                return int(estado.token and falha != 'token')
            if 'const token = ' in script:
                literal = script.split('const token = ', 1)[1].split(';', 1)[0]
                assert json.loads(literal) == token
                estado.token = True
                return
            if 'txtUsuario_I' in script:
                return '' if falha == 'campos' else env['SPW_USUARIO']
            if 'txtSenha_I' in script:
                return len(env['SPW_SENHA'])
            raise AssertionError(script)
        def click(self, seletor):
            assert seletor == '#ContentPlaceHolder1_btnEntrar_I'
            estado.entrou = True
            eventos.append(('login', seletor))
        def get_endpoint_url(self):
            assert not estado.playwright
            return 'endpoint'
        def save_screenshot(self, *args):
            pass
        def quit(self):
            eventos.append(('quit', None))
    class Pagina:
        def goto(self, url, **kwargs):
            assert url == env['SPW_CONSULTA_URL']
        def click(self, seletor):
            eventos.append(('click', seletor))
        def wait_for_selector(self, seletor, **kwargs):
            assert seletor == '#modalExportacao'
        def select_option(self, seletor, **kwargs):
            eventos.append(('select', kwargs['label']))
        def eval_on_selector(self, seletor, script):
            return '1' if falha == 'formato' else '0'
        @contextmanager
        def expect_download(self, **kwargs):
            yield SimpleNamespace(value=SimpleNamespace(save_as=lambda destino: destino.write_bytes(b'x' * 1200)))
        def screenshot(self, **kwargs):
            pass
        def content(self):
            return '<html></html>'
    @contextmanager
    def playwright():
        assert estado.entrou
        estado.playwright = True
        try:
            yield SimpleNamespace(chromium=SimpleNamespace(connect_over_cdp=lambda endpoint: SimpleNamespace(
                contexts=[SimpleNamespace(pages=[Pagina()])])) )
        finally:
            estado.playwright = False
    monkeypatch.setitem(sys.modules, 'seleniumbase', SimpleNamespace(sb_cdp=SimpleNamespace(Chrome=lambda *a, **k: Browser())))
    monkeypatch.setitem(sys.modules, 'playwright.sync_api', SimpleNamespace(sync_playwright=playwright))
    destino = tmp_path / 'ultimo.xls'
    if falha:
        with pytest.raises(robo.RoboErro):
            robo.baixar_export(env, destino)
        assert not destino.exists()
        if falha != 'formato':
            assert not estado.entrou
    else:
        assert robo.baixar_export(env, destino) == destino
        assert ('click', '#ContentPlaceHolder1_ASPxButton3') in eventos
        assert ('select', 'Excel') in eventos and ('select', 'Detalhado') in eventos
        assert destino.stat().st_size == 1200
    assert eventos[-1] == ('quit', None)
