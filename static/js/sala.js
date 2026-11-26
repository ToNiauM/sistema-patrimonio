/* sala.js — Sala do inventário na casca DSGov (templates/inventario_sala.html), carregado só nessa tela.
 *
 * Mesma lógica do JS inline de templates/tabler/inventario_sala.html, trocando as peças do Bootstrap pelas do padrão DSGov
 * dsgov: abas no br-tab (o BRTab do core troca o painel; aqui só se recontam e limpam a seleção), menu ⋮ com o
 * Dropdown do core, ficha do bem em br-scrim-util + br-modal (como em inventario_relatorio.html) e mostrar/esconder
 * sempre pela classe d-none (o `hidden` perde para componentes do DS que têm display próprio).
 *
 * Cada bem aparece duas vezes (Lista e Quadros, data-copia="lista"|"grade"): toda atualização vale para as duas.
 * Dados do servidor: #sala-config (URLs e flags) e #fichas (ficha de cada bem na tela, por número).
 */
(function () {
  "use strict";
  var cfgEl = document.getElementById("sala-config"), campo = document.getElementById("leitura");
  if (!cfgEl || !campo) return;
  var CFG = JSON.parse(cfgEl.textContent);
  var FICHAS = JSON.parse(document.getElementById("fichas").textContent);
  var CSRF = document.querySelector('meta[name="csrf"]').content;
  var NOMES = {pendente: "pendentes", localizado: "localizados", divergente: "divergentes"};
  var aviso = document.getElementById("aviso"), avisoTexto = document.getElementById("aviso-texto");
  var btnSobra = document.getElementById("btn-sobra"), cardSobra = document.getElementById("card-sobra"), formSobra = document.getElementById("form-sobra");
  var formLote = document.getElementById("form-lote"), barraLote = document.getElementById("barra-lote");
  var contadores = document.getElementById("contadores");
  var ultimoLido = "", ultimoQuando = 0, timerAviso = null, modalNumero = null, fotoAlvo = null;

  function mostrarEl(el, sim) { if (el) el.classList.toggle("d-none", !sim); }
  function copias(numero) { return document.querySelectorAll('[data-bem="' + numero + '"]'); }
  function urlLeitura(numero) { return CFG.url_leitura.replace(/\/0$/, "/" + numero); }
  function painelAtivo() { return document.querySelector(".tab-panel.active[data-secao-painel]"); }

  function focar() {
    if (campo.disabled || modalNumero !== null) return;
    campo.value = ""; campo.focus({preventScroll: true});
  }
  function mostrar(tipo, texto, sobra) {
    aviso.className = "br-message mt-2 mb-0 " + tipo; avisoTexto.textContent = texto;
    mostrarEl(btnSobra, !!sobra); clearTimeout(timerAviso);
    if (!sobra) timerAviso = setTimeout(function () { aviso.classList.add("d-none"); }, 4000);
  }

  // ---------------------------------------------------------------- contadores, seções vazias e busca
  function definir(nome, n) {
    document.getElementById("n-" + nome).textContent = n;
    document.querySelectorAll('[data-contador="' + nome + '"]').forEach(function (c) { c.textContent = n; });
  }
  function contar() {
    var loc = document.querySelectorAll("#lista-localizados [data-bem]").length;
    var div = document.querySelectorAll('#lista-divergentes [data-bem][data-ativo="sim"]').length;
    definir("localizados", loc);
    definir("divergentes", div);
    definir("pendentes", contadores.dataset.total - loc);
    document.querySelectorAll('[data-papel="alerta-divergentes"]').forEach(function (a) { mostrarEl(a, div > 0); });
    Object.keys(NOMES).forEach(function (s) {
      var painel = document.getElementById("secao-" + NOMES[s]), n = painel.querySelectorAll("#lista-" + NOMES[s] + " [data-bem]").length;
      painel.querySelector('[data-papel="caixa-lista"]').hidden = !n;
      if (!(s === "pendente" && contadores.dataset.total === "0")) mostrarEl(painel.querySelector('[data-papel="vazio"]'), !n);   // sala sem bens: aviso fixo
    });
  }
  function normalizar(s) { return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  var busca = document.getElementById("busca-bens"), buscaContagem = document.getElementById("busca-contagem");
  // Esconde o que não casa com a busca e reconta a seção visível. Chamada também depois de cada leitura, desfazer ou
  // troca de aba: um bem que muda de seção entra já filtrado e o "N de M" acompanha.
  function filtrar() {
    var termo = normalizar(busca.value.trim());
    document.querySelectorAll("[data-bem]").forEach(function (el) {
      el.classList.toggle("d-none", !!termo && normalizar(el.textContent).indexOf(termo) === -1);
    });
    var painel = painelAtivo(); if (!painel) return;
    var itens = painel.querySelectorAll('[data-bem][data-copia="lista"]'), visiveis = 0;
    itens.forEach(function (el) { if (!el.classList.contains("d-none")) visiveis++; });
    if (!termo) buscaContagem.textContent = itens.length ? itens.length + " bem(ns) nesta seção." : "";
    else if (!itens.length) buscaContagem.textContent = "";
    else if (!visiveis) buscaContagem.textContent = "Nenhum bem desta seção corresponde à busca.";
    else buscaContagem.textContent = visiveis + " de " + itens.length + " bem(ns) desta seção correspondem à busca.";
  }
  busca.addEventListener("input", filtrar);
  busca.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") ev.preventDefault();
    else if (ev.key === "Escape") { busca.value = ""; filtrar(); }
  });

  // ---------------------------------------------------------------- abas (o BRTab troca o painel)
  var todos = document.getElementById("selecionar-todos");
  document.querySelectorAll("[data-aba]").forEach(function (a) {
    a.addEventListener("click", function () {
      if (todos) todos.checked = false;
      setTimeout(filtrar, 0);   // depois do BRTab marcar o painel ativo
    });
  });

  // ---------------------------------------------------------------- Lista ou Quadros, lembrada neste aparelho
  // (sem escolha salva: Lista abaixo do md do DS, 992px, e Quadros acima — o mesmo corte das classes d-md-*)
  var CHAVE_VISAO = "inventario.sala.visao";
  function aplicarVisao(visao) {
    document.querySelectorAll('[data-papel="caixa-lista"]').forEach(function (c) { c.classList.remove("d-md-none"); c.classList.toggle("d-none", visao !== "lista"); });
    document.querySelectorAll('[data-papel="caixa-grade"]').forEach(function (c) { c.classList.remove("d-md-flex"); c.classList.toggle("d-none", visao !== "quadros"); });
    document.querySelectorAll("[data-visao]").forEach(function (b) {
      var ativa = b.dataset.visao === visao; b.classList.toggle("active", ativa); b.setAttribute("aria-pressed", ativa ? "true" : "false");
    });
  }
  var visaoSalva = null;
  try { visaoSalva = window.localStorage.getItem(CHAVE_VISAO); } catch (e) { visaoSalva = null; }
  aplicarVisao(visaoSalva === "lista" || visaoSalva === "quadros" ? visaoSalva : (window.matchMedia("(min-width: 992px)").matches ? "quadros" : "lista"));
  document.querySelectorAll("[data-visao]").forEach(function (b) {
    b.addEventListener("click", function () {
      aplicarVisao(b.dataset.visao);
      try { window.localStorage.setItem(CHAVE_VISAO, b.dataset.visao); } catch (e) { /* aba privada: vale só agora */ }
    });
  });

  // ---------------------------------------------------------------- menu ⋮ (Dropdown do core, sem trocar o ícone)
  function iniciarMenus(raiz) {
    if (!window.core || !window.core.Dropdown) return;
    raiz.querySelectorAll('[data-papel="acoes-bem"] [data-toggle="dropdown"]').forEach(function (btn) {
      if (btn.dataset.salaMenu) return;
      btn.dataset.salaMenu = "1";
      try { new window.core.Dropdown({trigger: btn, useIcons: false}).setBehavior(); } catch (e) { console.warn("sala: menu", e); }
    });
  }
  function fecharMenus() {
    document.querySelectorAll('[data-papel="menu-bem"]:not([hidden])').forEach(function (m) {
      var gatilho = document.querySelector('[data-target="' + m.id + '"]'); if (gatilho) gatilho.click();
    });
  }
  iniciarMenus(document);

  // ---------------------------------------------------------------- desenho de um bem a partir da ficha
  function rotulo(f) {
    if (f.secao === "localizado") return ["Localizado", "bg-success"];
    if (f.secao === "divergente") return f.situacao === "ATIVO" ? ["Divergente", "bg-warning text-gray-80"] : ["Não ativo", "bg-danger"];
    return ["Pendente", "bg-gray-20 text-gray-80"];
  }
  function no(tag, classe, texto) { var n = document.createElement(tag); if (classe) n.className = classe; if (texto !== undefined) n.textContent = texto; return n; }
  function link(href, texto) { var a = no("a", "", texto); a.href = href; return a; }
  function icone(classe) { var i = no("i", classe); i.setAttribute("aria-hidden", "true"); return i; }
  // Foto quadrada do quadro (a lista não tem foto): primeira foto ou o ícone da categoria.
  function trocarAvatar(el, numero, fotos) {
    var atual = el.querySelector('[data-papel="avatar"]'), f = fotos[0];
    if (!atual) return;
    var novo = no("div", "bg-gray-2 text-gray-40");
    novo.dataset.papel = "avatar";
    if (f && /^https?:\/\//.test(f.url)) {
      novo.title = "Foto do bem";
      var img = no("img"); img.src = f.url; img.alt = "Foto " + f.nfoto + " do bem " + numero; novo.appendChild(img);
    } else {
      novo.title = "Bem sem foto";
      novo.appendChild(icone("fas " + (el.dataset.icone || "fa-box") + " fa-3x"));
    }
    atual.replaceWith(novo);
  }
  function selos(el) {
    var f = FICHAS[el.dataset.bem], caixa = el.querySelector('[data-papel="selos"]'); if (!caixa || !f) return;
    caixa.textContent = "";
    function selo(classe, texto, titulo) { var s = no("span", "br-tag small " + classe, texto); if (titulo) s.title = titulo; caixa.appendChild(s); }
    if (f.conservacao) selo("bg-blue-warm-vivid-70", f.conservacao);
    if (f.lido && !f.conservacao) selo("bg-orange-vivid-10 text-orange-vivid-70", "sem conservação");
    if (f.lido && CFG.fotos_ativas && !f.fotos.length) selo("bg-orange-vivid-10 text-orange-vivid-70", "sem foto");
    if (f.fotos.length > 1) selo("bg-gray-10 text-gray-80", "+" + (f.fotos.length - 1) + " foto(s)", "Todas as fotos estão nos detalhes do bem");
  }
  function atualizarItem(el) {
    var f = FICHAS[el.dataset.bem], r = rotulo(f);
    el.dataset.secao = f.secao; el.dataset.ativo = f.situacao === "ATIVO" ? "sim" : "nao";
    var tag = el.querySelector('[data-papel="situacao"]'); tag.textContent = r[0]; tag.className = "br-tag small " + r[1];
    var encontrado = el.querySelector('[data-papel="encontrado"]'); if (encontrado && f.secao !== "pendente") encontrado.remove();
    mostrarEl(el.querySelector('[data-papel="leitura"]'), f.lido);
    el.querySelector('[data-papel="leitura-texto"]').textContent = f.lido ? (f.secao === "divergente" ? "Lido aqui" : "Lido") + " por " + f.integrante + " em " + String(f.lido_em).slice(0, 16) : "";
    mostrarEl(el.querySelector('[data-acao="desfazer"]'), f.lido);
    var foto = el.querySelector('[data-acao="foto"]');
    if (foto) { foto.classList.toggle("disabled", !f.lido); if (f.lido) foto.removeAttribute("aria-disabled"); else foto.setAttribute("aria-disabled", "true"); }
    selos(el);
  }
  // Bem de outra sala (ou não ativo) lido agora: cria as duas cópias a partir dos modelos.
  function novoItem(f) {
    return ["modelo-lista", "modelo-grade"].map(function (id) {
      var caixa = document.createElement("div");
      caixa.innerHTML = document.getElementById(id).innerHTML.split("__N__").join(String(f.numero)).trim();
      var el = caixa.firstElementChild;
      el.querySelector('[data-papel="descricao"]').textContent = f.descricao + (f.complemento ? " " + f.complemento : "");
      el.querySelector('[data-papel="local"]').textContent = "Cadastrado em " + (f.localizacao || "—") + (f.situacao !== "ATIVO" ? " · " + f.situacao : "");
      el.querySelector('[data-papel="responsavel"]').textContent = f.pessoa || f.responsavel_centro || "—";
      var entrada = el.querySelector('[data-papel="entrada"]');   // só no quadro
      if (entrada) entrada.textContent = (f.data_entrada || "—") + " · " + (f.valor_atual || "valor não informado");
      var numero = el.querySelector('[data-papel="numero"]'); if (numero && numero.tagName === "A") numero.href = f.url_bem;
      trocarAvatar(el, f.numero, f.fotos);
      iniciarMenus(el);
      return el;
    });
  }
  function mover(el, secao) {
    document.getElementById((el.dataset.copia === "lista" ? "lista-" : "grade-") + NOMES[secao]).prepend(el);
  }
  function aplicar(j) {
    var f = j.ficha; FICHAS[f.numero] = f;
    var els = Array.prototype.slice.call(copias(f.numero)); if (!els.length) els = novoItem(f);
    els.forEach(function (el) { mover(el, f.secao); atualizarItem(el); });
    contar();
    filtrar();
    if (String(modalNumero) === String(f.numero)) preencherFicha(f.numero);
  }

  // ---------------------------------------------------------------- leitura (leitor, Digitar, câmera, menu, ficha)
  function ler(numero) {
    numero = String(numero || "").trim(); if (!numero) return;
    var agora = Date.now(); if (numero === ultimoLido && agora - ultimoQuando < 3000) return;   // leitura dupla do leitor/câmera
    ultimoLido = numero; ultimoQuando = agora;
    fetch(CFG.url_ler, {method: "POST", headers: {"Content-Type": "application/json", "X-CSRF": CSRF}, body: JSON.stringify({numero: numero})})
      .then(function (r) { return r.json().then(function (j) { return {status: r.status, j: j}; }); })
      .then(function (res) {
        var j = res.j;
        if (res.status === 404) { mostrar("danger", "Bem " + numero + " não está na base.", true); return; }
        if (res.status !== 200) { mostrar("danger", j.erro || "Erro ao registrar a leitura."); return; }
        var texto = j.situacao === "localizado" ? "Bem " + j.numero + " localizado." : "Bem " + j.numero + " cadastrado em " + j.cadastrado_em + "; registrado aqui como divergente.";
        if (!j.ativo) texto = "Bem " + j.numero + " está " + j.situacao_bem + "; leitura registrada.";
        if (j.reler && j.leitura_anterior) texto += " Já lido em " + j.leitura_anterior.lido_em.slice(8, 10) + "/" + j.leitura_anterior.lido_em.slice(5, 7) + " por " + j.leitura_anterior.integrante + " em " + j.leitura_anterior.localizacao + ". Atualizado.";
        mostrar(!j.ativo ? "info" : (j.situacao === "localizado" ? "success" : "warning"), texto);
        aplicar(j);
      })
      .catch(function () { mostrar("danger", "Sem conexão; tente de novo."); })
      .finally(focar);
  }
  campo.addEventListener("keydown", function (ev) { if (ev.key === "Enter") { ev.preventDefault(); ler(campo.value); } });
  document.getElementById("btn-digitar").addEventListener("click", function () { campo.inputMode = "numeric"; campo.placeholder = "Digite o número e Enter"; campo.focus(); });
  campo.addEventListener("blur", function () { campo.inputMode = "none"; });
  btnSobra.addEventListener("click", function () { if (cardSobra) { cardSobra.hidden = false; formSobra.querySelector("#s-descricao").focus(); } });
  var btnCancelar = document.getElementById("btn-cancelar-sobra");
  if (btnCancelar) btnCancelar.addEventListener("click", function () { cardSobra.hidden = true; focar(); });

  // Câmera (html5-qrcode): fica aberta para leituras seguidas até fechar.
  var leitor = null, cameraDiv = document.getElementById("camera"), cameraAberta = false;
  document.getElementById("btn-camera").addEventListener("click", function () {
    if (cameraAberta) return;
    cameraAberta = true;
    cameraDiv.hidden = false;
    if (!leitor) leitor = new window.Html5QrcodeScanner("leitor-camera", {fps: 10, qrbox: {width: 250, height: 120}}, false);
    leitor.render(function (texto) { ler(texto); }, function () {});
  });
  document.getElementById("btn-fechar-camera").addEventListener("click", function () {
    cameraDiv.hidden = true; if (leitor) leitor.clear().catch(function () {}); leitor = null; cameraAberta = false; focar();
  });

  // ---------------------------------------------------------------- seleção e ações em lote
  function selecionados() {
    var n = {}; document.querySelectorAll('[data-papel="selecao"]:checked').forEach(function (c) { n[c.value] = true; }); return Object.keys(n);
  }
  function atualizarLote() {
    if (!formLote) return;
    var n = selecionados().length;
    document.getElementById("n-selecionados").textContent = n;
    mostrarEl(barraLote, n > 0);
  }
  function marcar(numero, sim) {
    copias(numero).forEach(function (c) {
      var x = c.querySelector('[data-papel="selecao"]'); if (x) x.checked = sim;
      if (c.classList.contains("br-item")) c.classList.toggle("selected", sim);
    });
  }
  document.addEventListener("change", function (ev) {
    var el = ev.target;
    if (el.dataset && el.dataset.papel === "selecao") { marcar(el.value, el.checked); atualizarLote(); }
    else if (el.id === "selecionar-todos") {
      // só os bens da seção aberta que a busca deixou visíveis
      var painel = painelAtivo(); if (!painel) return;
      painel.querySelectorAll('[data-bem][data-copia="lista"]').forEach(function (c) { if (!c.classList.contains("d-none")) marcar(c.dataset.bem, el.checked); });
      atualizarLote();
    }
  });
  function numerosNoLote(nums) {
    formLote.querySelectorAll('input[name="numeros"], input[name="acao"]').forEach(function (i) { i.remove(); });
    nums.forEach(function (n) { var i = document.createElement("input"); i.type = "hidden"; i.name = "numeros"; i.value = n; formLote.appendChild(i); });
  }
  if (formLote) formLote.addEventListener("submit", function (ev) {
    var nums = selecionados();
    if (!nums.length) { ev.preventDefault(); mostrar("warning", "Selecione ao menos um bem na lista."); return; }
    if (ev.submitter && ev.submitter.value === "desmarcar" && !window.confirm("Desfazer a leitura de " + nums.length + " bem(ns)? Eles voltam a pendentes e as fotos são apagadas.")) { ev.preventDefault(); return; }
    numerosNoLote(nums);   // cada número uma vez só, mesmo marcado nas duas cópias
  });
  function desfazer(numero) {
    if (!formLote || !window.confirm("Desfazer a leitura do bem " + numero + "? Ele volta a pendente e as fotos são apagadas.")) return;
    numerosNoLote([numero]);
    var a = document.createElement("input"); a.type = "hidden"; a.name = "acao"; a.value = "desmarcar"; formLote.appendChild(a);
    HTMLFormElement.prototype.submit.call(formLote);
  }

  // ---------------------------------------------------------------- ficha do bem (br-scrim-util + br-modal)
  var scrim = document.getElementById("scrim-bem"), erroFicha = document.getElementById("det-erro");
  function erro(texto) { document.getElementById("det-erro-texto").textContent = texto || ""; mostrarEl(erroFicha, !!texto); }
  function desenharFotos(f) {
    var caixa = document.getElementById("det-fotos"); caixa.textContent = "";
    document.getElementById("det-n-fotos").textContent = f.fotos.length;
    mostrarEl(document.getElementById("det-sem-fotos"), !f.fotos.length);
    f.fotos.forEach(function (foto) {
      var col = no("div", "col-6 col-sm-4 mb-3"), card = no("div", "br-card mb-0"), topo;
      if (/^https?:\/\//.test(foto.url)) {
        topo = link(foto.url); topo.target = "_blank"; topo.rel = "noopener";
        topo.setAttribute("aria-label", "Abrir a foto " + foto.nfoto + " em tamanho real");
        var img = no("img"); img.src = foto.url; img.alt = "Foto " + foto.nfoto + " do bem " + f.numero; topo.appendChild(img);
      } else {
        topo = no("div", "d-flex align-items-center justify-content-center bg-gray-2 p-4");
        topo.appendChild(icone("fas fa-image fa-2x text-gray-40"));
      }
      var corpo = no("div", "card-content d-flex align-items-center justify-content-between py-1");
      corpo.appendChild(no("span", "text-down-01 text-gray-70", "Foto " + foto.nfoto));
      if (!CFG.fechado) {
        var b = no("button", "br-button circle small"); b.type = "button"; b.dataset.nfoto = foto.nfoto;
        b.setAttribute("aria-label", "Excluir foto " + foto.nfoto); b.title = "Excluir foto " + foto.nfoto;
        b.appendChild(icone("fas fa-trash")); corpo.appendChild(b);
      }
      card.appendChild(topo); card.appendChild(corpo); col.appendChild(card); caixa.appendChild(col);
    });
  }
  function preencherFicha(numero) {
    var f = FICHAS[numero], r = rotulo(f);
    erro("");
    var titulo = document.getElementById("det-link"); titulo.textContent = "Bem " + f.numero;
    if (CFG.pode_bem) titulo.href = f.url_bem; else titulo.removeAttribute("href");
    document.getElementById("det-titulo").textContent = f.descricao;
    var tag = document.getElementById("det-situacao"); tag.textContent = r[0]; tag.className = "br-tag small " + r[1];
    var valores = {descricao: f.descricao, complemento: f.complemento, classificacao: f.classificacao, situacao: f.situacao,
                   localizacao: f.localizacao, data_entrada: f.data_entrada, valor_compra: f.valor_compra, valor_atual: f.valor_atual,
                   lido_em_sala: f.lido_em_sala, integrante: f.integrante, lido_em: f.lido_em};
    scrim.querySelectorAll("[data-ficha]").forEach(function (c) { c.textContent = valores[c.dataset.ficha] || "—"; });
    var centro = document.getElementById("det-centro"); centro.textContent = "";
    if (f.ccustos) { centro.appendChild(link(f.url_ccustos, f.ccustos)); centro.appendChild(document.createTextNode(" — " + (f.responsavel_centro || ""))); }
    else centro.textContent = "sem mapeamento";
    var pessoa = document.getElementById("det-pessoa"); pessoa.textContent = "";
    if (f.pessoa) pessoa.appendChild(link(f.url_pessoa, f.pessoa)); else pessoa.textContent = "— (responde o setor)";
    mostrarEl(document.getElementById("modal-bem-aviso"), !f.lido);
    scrim.querySelectorAll('input[name="det-conservacao"]').forEach(function (r) { r.checked = r.value === (f.conservacao || ""); });
    document.getElementById("det-quem-usa").value = f.quem_usa || "";
    document.getElementById("det-observacao").value = f.observacao || "";
    scrim.querySelectorAll("[data-campo]").forEach(function (c) { c.disabled = CFG.fechado || !f.lido; });
    var nova = document.getElementById("det-nova-foto");
    if (nova) { nova.classList.toggle("disabled", !f.lido); if (f.lido) nova.removeAttribute("aria-disabled"); else nova.setAttribute("aria-disabled", "true"); }
    mostrarEl(document.getElementById("det-desfazer"), f.lido);
    mostrarEl(document.getElementById("det-ler"), f.secao !== "localizado");
    desenharFotos(f);
  }
  function abrirFicha(numero) {
    modalNumero = numero; preencherFicha(numero);
    scrim.hidden = false; scrim.classList.add("active");
    document.getElementById("det-fechar").focus();
  }
  function fecharFicha() {
    if (modalNumero === null) return;
    scrim.classList.remove("active"); scrim.hidden = true; modalNumero = null; focar();
  }
  ["det-fechar", "det-concluir"].forEach(function (id) { document.getElementById(id).addEventListener("click", fecharFicha); });
  scrim.addEventListener("click", function (ev) { if (ev.target === scrim) fecharFicha(); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && modalNumero !== null) fecharFicha(); });
  var btnLerFicha = document.getElementById("det-ler");
  if (btnLerFicha) btnLerFicha.addEventListener("click", function () { ultimoLido = ""; ler(modalNumero); });
  var btnDesfazerFicha = document.getElementById("det-desfazer");
  if (btnDesfazerFicha) btnDesfazerFicha.addEventListener("click", function () { desfazer(modalNumero); });
  scrim.addEventListener("change", function (ev) {
    var el = ev.target; if (!el.dataset.campo || modalNumero === null) return;
    var numero = modalNumero, corpo = {}; corpo[el.dataset.campo] = el.value;
    fetch(urlLeitura(numero), {method: "POST", headers: {"Content-Type": "application/json", "X-CSRF": CSRF}, body: JSON.stringify(corpo)})
      .then(function (r) {
        if (!r.ok) return r.json().then(function (j) { erro(j.erro || "Erro ao salvar."); });
        FICHAS[numero][el.dataset.campo] = el.value;
        copias(numero).forEach(selos);
      })
      .catch(function () { erro("Sem conexão; alteração não salva."); });
  });
  // Excluir foto na ficha: confirma, apaga e redesenha sem recarregar.
  document.getElementById("det-fotos").addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-nfoto]"); if (!b || modalNumero === null) return;
    var numero = modalNumero, nfoto = b.dataset.nfoto;
    if (!window.confirm("Excluir a foto " + nfoto + " do bem " + numero + "? Ela é apagada definitivamente.")) return;
    b.disabled = true;
    fetch(CFG.url_foto_excluir.replace(/\/0\/foto\/0\//, "/" + numero + "/foto/" + nfoto + "/"), {method: "POST", headers: {"Accept": "application/json", "X-CSRF": CSRF}})
      .then(function (r) { return r.json().then(function (j) { return {ok: r.ok, j: j}; }); })
      .then(function (res) {
        if (!res.ok) { b.disabled = false; erro(res.j.erro || "Erro ao excluir a foto."); return; }
        fotosNovas(numero, res.j.fotos);
      })
      .catch(function () { b.disabled = false; erro("Sem conexão; foto não excluída."); });
  });

  // ---------------------------------------------------------------- fotos de bem (menu "Nova foto" ou ficha)
  function fotosNovas(numero, fotos) {
    FICHAS[numero].fotos = fotos.map(function (f) { return {nfoto: f.nfoto, url: f.url}; });
    copias(numero).forEach(function (c) { trocarAvatar(c, numero, FICHAS[numero].fotos); selos(c); });
    if (String(modalNumero) === String(numero)) desenharFotos(FICHAS[numero]);
  }
  function enviarFoto(numero, arquivo, input) {
    var fd = new FormData(); fd.append("foto", arquivo);
    function falha(texto) { if (modalNumero !== null) erro(texto); else mostrar("danger", texto); }
    fetch(urlLeitura(numero) + "/foto", {method: "POST", headers: {"X-CSRF": CSRF}, body: fd})
      .then(function (r) { return r.json().then(function (j) { return {ok: r.ok, j: j}; }); })
      .then(function (res) {
        if (!res.ok) { falha(res.j.erro || "Erro ao salvar."); return; }
        fotosNovas(numero, res.j.fotos);
        if (modalNumero === null) mostrar("success", "Foto do bem " + numero + " enviada.");
      })
      .catch(function () { falha("Sem conexão; foto não enviada."); })
      .finally(function () { input.value = ""; fotoAlvo = null; });
  }
  var inputFoto = document.getElementById("foto-bem");
  if (inputFoto) inputFoto.addEventListener("change", function () {
    var numero = fotoAlvo !== null ? fotoAlvo : modalNumero;
    if (inputFoto.files && inputFoto.files[0] && numero !== null) enviarFoto(numero, inputFoto.files[0], inputFoto);
  });

  // ---------------------------------------------------------------- cliques: menu, item (abre a ficha), resto (foca a leitura)
  document.addEventListener("click", function (ev) {
    var botao = ev.target.closest("[data-acao]");
    if (botao) {
      var item = botao.closest("[data-bem]"), numero = item ? item.dataset.bem : modalNumero;
      if (botao.dataset.acao === "foto") {
        // rótulo do #foto-bem: o navegador abre a câmera/arquivos depois deste clique, a menos que o bem não esteja lido
        if (numero === null || !FICHAS[numero] || !FICHAS[numero].lido) {
          ev.preventDefault();
          if (modalNumero !== null) erro("Registre a leitura deste bem antes de fotografar.");
          else mostrar("warning", "Registre a leitura do bem " + numero + " antes de fotografar.");
        } else fotoAlvo = numero;
        if (item) fecharMenus();
        return;
      }
      fecharMenus();
      if (botao.dataset.acao === "ler") { ultimoLido = ""; ler(numero); }
      else if (botao.dataset.acao === "desfazer") desfazer(numero);
      else if (botao.dataset.acao === "detalhes") abrirFicha(numero);
      return;
    }
    var clicado = ev.target.closest("[data-bem]");
    if (clicado && !ev.target.closest("a, button, input, label, [data-papel='acoes-bem']")) { abrirFicha(clicado.dataset.bem); return; }
    if (!ev.target.closest("input, select, textarea, button, label, a, #camera, #scrim-bem, [data-bem], [data-papel='acoes-bem']")) focar();
  });
  // teclado no "Nova foto" (é um <label>): Enter/Espaço abrem o seletor como o clique
  document.addEventListener("keydown", function (ev) {
    var el = ev.target;
    if ((ev.key === "Enter" || ev.key === " ") && el.dataset && el.dataset.acao === "foto" && el.tagName === "LABEL") { ev.preventDefault(); el.click(); }
  });

  // A faixa de leitura (sticky) para logo abaixo do cabeçalho fixo do DS, que encolhe ao rolar: mede e grava --sala-topo.
  var cabecalho = document.getElementById("header"), medindo = false;
  function medirTopo() {
    medindo = false;
    var h = cabecalho && window.getComputedStyle(cabecalho).position !== "static" ? cabecalho.getBoundingClientRect().bottom : 0;
    document.documentElement.style.setProperty("--sala-topo", Math.max(0, Math.round(h)) + "px");
  }
  function pedirMedida() { if (!medindo) { medindo = true; window.requestAnimationFrame(medirTopo); } }
  window.addEventListener("scroll", pedirMedida, {passive: true});
  window.addEventListener("resize", pedirMedida);
  document.addEventListener("DOMContentLoaded", pedirMedida);

  contar();
  filtrar();
  atualizarLote();
  medirTopo();
  focar();
})();
