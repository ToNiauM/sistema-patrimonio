/* analise.js — gráficos da tela Análise na casca DSGov (templates/analise.html), carregado só nela, DEPOIS de
 * echarts-dsgov.js (cópia congelada do padrão DSGov: tema "dsgov", paletas e formatadores em window.dsgov.graficos).
 * Complementa o tema sem editá-lo: os cards de painel.cards_analise (os mesmos do Tabler) trazem o que o
 * montar() do padrão DSGov não entende —
 *   - tooltip.valueFormatter "moeda"/"percentual" (graficos.py: JSON não leva função);
 *   - total no furo da rosca ("165,4 mi / em R$"), que acompanha a legenda e fica no centro real do anel;
 *   - modelos "{b}<br/>R$ {c} ({d}%)" com número cru; eixos com números grandes (abreviados: 12 mil, 1,5 mi);
 *   - cores da classificação na paleta do Tabler (graficos.CORES_CATEGORICA), trocadas pela categórica do DSGov;
 *   - seletores (br-select) que trocam a variante do card (g-explorar--ccusto--valor) e a tabela "Ver dados".
 * Este script roda com o DOM já lido (fim do <body>): monta os gráficos da página e os marca com
 * data-dsgov-grafico, então o montar() do padrão DSGov (no DOMContentLoaded) não os monta de novo.
 */
(function () {
  "use strict";
  if (!window.echarts || !window.dsgov || !window.dsgov.graficos) return;
  var G = window.dsgov.graficos;

  /* Espelho de graficos.CORES_CATEGORICA (Python): a mesma classificação tem a mesma cor em todos os gráficos;
     na casca DSGov, a i-ésima cor vira a i-ésima da paleta categórica oficial (tests/test_paridade_dsgov.py guarda). */
  var CATEGORICA_TABLER = ["#066fd1", "#2fb344", "#f76707", "#ae3ec9", "#17a2b8", "#f59f00", "#d6336c", "#4263eb", "#74b816", "#0ca678"];
  var TROCA = {};
  CATEGORICA_TABLER.forEach(function (c, i) { TROCA[c] = G.categorica[i % G.categorica.length]; });

  var fmtInteiro = new Intl.NumberFormat("pt-BR");
  var fmtCurto = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 1 });
  var fmtDecimal = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function numero(v) { return v && typeof v === "object" ? v.value : v; }
  function fmtValor(v) { return typeof v === "number" ? fmtInteiro.format(Math.round(v * 100) / 100) : v; }
  /* Eixo e rótulo no gráfico: 1,2 bi · 150 mi · 12 mil; o valor exato fica no tooltip e em "Ver dados" */
  function fmtEixo(v) {
    if (typeof v !== "number") return v;
    var a = Math.abs(v);
    if (a >= 1e9) return fmtCurto.format(v / 1e9) + " bi";
    if (a >= 1e6) return fmtCurto.format(v / 1e6) + " mi";
    if (a >= 1e4) return fmtCurto.format(v / 1e3) + " mil";
    return fmtInteiro.format(v);
  }
  var FORMATOS_DICA = {
    moeda: function (v) { return typeof v === "number" ? G.moeda(v) : (v == null ? "-" : v); },
    percentual: function (v) { return typeof v === "number" ? fmtCurto.format(v) + "%" : v; },
  };

  function trocarCores(no) {
    if (Array.isArray(no)) { for (var i = 0; i < no.length; i++) no[i] = trocarCores(no[i]); return no; }
    if (no && typeof no === "object") { for (var k in no) if (Object.prototype.hasOwnProperty.call(no, k)) no[k] = trocarCores(no[k]); return no; }
    if (typeof no === "string") return TROCA[no.toLowerCase()] || no;
    return no;
  }

  /* "{b}: {c} ({d}%)" → função com número formatado: curto no gráfico, exato (moeda quando "R$ {c}") no tooltip */
  function modelo(f, curto) {
    if (typeof f !== "string" || !/\{[bcd]\}/.test(f)) return f;
    return function (p) {
      var v = numero(p.value);
      return f.replace(/\{b\}/g, p.name).replace(/R\$ \{c\}/g, curto ? "R$ " + fmtEixo(v) : G.moeda(v))
              .replace(/\{c\}/g, (curto ? fmtEixo : fmtValor)(v))
              .replace(/\{d\}/g, typeof p.percent === "number" ? fmtCurto.format(p.percent) : "");
    };
  }

  function preparar(op, largura) {
    var estreito = largura < 480;
    trocarCores(op);
    [].concat(op.xAxis || [], op.yAxis || []).forEach(function (eixo) {
      if (!eixo) return;
      eixo.axisLabel = eixo.axisLabel || {};
      if (eixo.type === "value" && !eixo.axisLabel.formatter) eixo.axisLabel.formatter = fmtEixo;
      if (eixo.type === "category") {
        eixo.axisLabel.hideOverlap = true;
        if (estreito) eixo.axisLabel.fontSize = 11;
      }
    });
    /* categorias no eixo Y (barras deitadas): nome longo cortado com reticências, nunca empurra o desenho */
    [].concat(op.yAxis || []).forEach(function (e) {
      if (e && e.type === "category") { e.axisLabel.overflow = "truncate"; e.axisLabel.width = estreito ? 96 : 180; }
    });
    var series = op.series || [];
    var temLegenda = op.legend && op.legend.show !== false;
    series.forEach(function (s) {
      if (s.label && s.label.show && !s.label.formatter) s.label.formatter = function (p) { return fmtEixo(numero(p.value)); };
      if (s.label) s.label.formatter = modelo(s.label.formatter, true);
      if (s.type === "bar" && s.stack) { s.itemStyle = s.itemStyle || {}; if (s.itemStyle.borderRadius === undefined) s.itemStyle.borderRadius = 0; }
      if (s.type === "pie") {
        /* anel acima da legenda: centro a 45% e raio externo de no máximo 70%; nomes na legenda e no tooltip */
        s.center = s.center || ["50%", "45%"];
        if (Array.isArray(s.radius) && parseFloat(s.radius[1]) > 70) {
          var k = 70 / parseFloat(s.radius[1]);
          s.radius = [(parseFloat(s.radius[0]) * k).toFixed(1) + "%", "70%"];
        }
        if (temLegenda) { s.label = Object.assign({}, s.label || {}, { show: false }); s.labelLine = { show: false }; }
      }
    });
    /* celular com muitas barras rotuladas: os números se atropelam — ficam só no tooltip e em "Ver dados" */
    if (estreito) {
      var categorias = 0;
      [].concat(op.xAxis || [], op.yAxis || []).forEach(function (e) { if (e && e.type === "category" && Array.isArray(e.data)) categorias = Math.max(categorias, e.data.length); });
      if (categorias > 6) series.forEach(function (s) { if (s.type === "bar" && s.label && s.label.position !== "inside") s.label.show = false; });
    }
    /* legenda embaixo (paginada pelo tema): a grade reserva a altura dela, o desenho nunca a cobre */
    if (temLegenda) {
      op.legend.textStyle = Object.assign({ overflow: "truncate", width: estreito ? 110 : 180 }, op.legend.textStyle || {});
      [].concat(op.grid || []).forEach(function (g) { g.bottom = Math.max(parseInt(g.bottom, 10) || 0, 44); });
      if (!op.grid && (op.xAxis || op.yAxis)) op.grid = { bottom: 44 };
    }
    /* rótulo à direita da barra ("60 mi"): o containLabel não o conta, a grade reserva a folga */
    var rotuloDireita = series.some(function (s) { return s.type === "bar" && s.label && s.label.show && s.label.position === "right"; });
    [].concat(op.grid || []).forEach(function (g) {
      g.containLabel = true;
      g.right = rotuloDireita ? 64 : (g.right === undefined || parseInt(g.right, 10) > 40 ? (estreito ? 12 : 24) : g.right);
    });
    op.tooltip = op.tooltip || {};
    if (typeof op.tooltip.valueFormatter === "string") op.tooltip.valueFormatter = FORMATOS_DICA[op.tooltip.valueFormatter];
    if (!op.tooltip.valueFormatter) op.tooltip.valueFormatter = fmtValor;
    if (op.tooltip.trigger === "item") op.tooltip.formatter = modelo(op.tooltip.formatter, false);
    op.tooltip.confine = true;   /* tooltip nunca sai do card */
    return op;
  }

  /* Total no furo da rosca: o texto vem como "165,4 mi\nem R$" (painel.moeda_curta) ou "133\nbens". Posiciona no
     centro do anel (em pixels) e, se o número é a soma das fatias, reescreve-o ao ligar/desligar fatias na legenda. */
  function totalDaRosca(op, largura, altura) {
    var pizza = (op.series || []).filter(function (s) { return s.type === "pie"; })[0];
    var texto = [].concat(op.graphic || [])[0];
    if (!pizza || !texto || texto.type !== "text" || !texto.style || typeof texto.style.text !== "string") return null;
    texto.id = "total-rosca";
    ["left", "top", "right", "bottom"].forEach(function (k) { delete texto[k]; });
    var c = pizza.center;
    texto.x = parseFloat(c[0]) / 100 * largura;
    texto.y = parseFloat(c[1]) / 100 * altura;
    Object.assign(texto.style, { textAlign: "center", textVerticalAlign: "middle", fill: G.cores.texto },
                  largura < 480 ? { fontSize: 16, lineHeight: 20 } : {});
    var linhas = texto.style.text.split("\n");
    var soma = function (sel) {
      return (pizza.data || []).reduce(function (t, d) { return sel && d && sel[d.name] === false ? t : t + (Number(numero(d)) || 0); }, 0);
    };
    var curta = function (v) {
      var a = Math.abs(v), s = v < 0 ? "-" : "";
      if (a >= 1e6) return s + (a / 1e6).toFixed(1).replace(".", ",") + " mi";
      if (a >= 1e3) return s + (a / 1e3).toFixed(1).replace(".", ",") + " mil";
      return fmtDecimal.format(v);
    };
    var limpo = function (t) { return String(t).replace(/\s/g, " "); };
    var formato = [String, fmtInteiro.format.bind(fmtInteiro), G.moeda, curta]
      .filter(function (f) { return limpo(f(soma())) === limpo(linhas[0]); })[0];
    if (!formato) return null;
    return function (sel) { return { id: texto.id, style: Object.assign({}, texto.style, { text: [formato(soma(sel))].concat(linhas.slice(1)).join("\n") }) }; };
  }

  function montar(el) {
    var script = document.getElementById(el.dataset.grafico);
    if (!script) return;
    var largura = el.clientWidth || 600, altura = el.clientHeight || 400;
    var op = preparar(JSON.parse(script.textContent), largura);
    var total = totalDaRosca(op, largura, altura);
    var inst = echarts.init(el, "dsgov", { renderer: "canvas" });
    inst.setOption(op);
    inst.setOption(inst.getOption());   /* segunda passada: legenda paginada desenhada certo (graficos.md, regra 11) */
    el.dataset.dsgovGrafico = "1";
    el.__estreito = largura < 480;
    if (total) inst.on("legendselectchanged", function (ev) { inst.setOption({ graphic: { elements: [total(ev.selected)] } }); });
    inst.on("click", function (p) {   /* drill-down declarativo, como o echarts-dsgov.js */
      var url = p && p.data && typeof p.data === "object" ? p.data.url : null;
      if (typeof url === "string" && url) window.location.assign(url);
    });
  }

  function remontar(el) {
    var inst = echarts.getInstanceByDom(el);
    if (inst) echarts.dispose(el);
    montar(el);
  }

  /* Mudou a largura (girar o celular, abrir o menu): redimensiona; cruzou 480px, refaz as proteções de layout */
  function observar(el) {
    var ajustar = function () {
      var inst = echarts.getInstanceByDom(el);
      if (!inst || !el.clientWidth) return;
      if ((el.clientWidth < 480) !== el.__estreito) remontar(el);
      else {
        inst.resize();
        var op = inst.getOption(), pizza = (op.series || []).filter(function (s) { return s.type === "pie"; })[0];
        if (pizza && op.graphic && op.graphic[0] && op.graphic[0].elements && op.graphic[0].elements.length) {
          inst.setOption({ graphic: { elements: [{ id: "total-rosca", x: parseFloat(pizza.center[0]) / 100 * el.clientWidth,
                                                   y: parseFloat(pizza.center[1]) / 100 * el.clientHeight }] } });
        }
      }
    };
    if (window.ResizeObserver) new ResizeObserver(ajustar).observe(el);
    else window.addEventListener("resize", ajustar);
  }

  /* Seletor do card: cada [data-grafico-seletor="base"] envolve um br-select; o id da variante é a base mais os
     valores marcados, na ordem da página, unidos por "--". Troca o gráfico, o aria-label e a tabela "Ver dados". */
  function trocarVariante(base) {
    var valores = [];
    document.querySelectorAll('[data-grafico-seletor="' + base + '"]').forEach(function (s) {
      var marcado = s.querySelector('input[type="radio"]:checked');
      if (marcado) valores.push(marcado.value);
    });
    var id = [base].concat(valores).join("--");
    var el = document.querySelector('[data-grafico-base="' + base + '"]');
    var script = document.getElementById(id);
    if (!el || !script || el.dataset.grafico === id) return;
    el.dataset.grafico = id;
    var resumo = script.getAttribute("data-resumo");
    if (resumo) el.setAttribute("aria-label", resumo);
    document.querySelectorAll("[data-grafico-tabela]").forEach(function (t) {
      var alvo = t.getAttribute("data-grafico-tabela");
      if (alvo.indexOf(base + "--") === 0) t.hidden = alvo !== id;
    });
    remontar(el);
  }
  function aoEscolher(ev) {
    var caixa = ev.target && ev.target.closest && ev.target.closest("[data-grafico-seletor]");
    if (caixa) trocarVariante(caixa.getAttribute("data-grafico-seletor"));
  }
  document.addEventListener("change", aoEscolher);
  document.addEventListener("onChange", aoEscolher);   /* evento do BRSelect (core.min.js) ao escolher um item */

  document.querySelectorAll("[data-grafico]").forEach(function (el) {
    if (el.dataset.dsgovGrafico) return;
    montar(el);
    observar(el);
  });
})();
