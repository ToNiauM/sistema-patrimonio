/*
 * checklist.js — checklist interativo dos procedimentos (equivalente ao
 * ChecklistControls do portal Astro).
 *
 * - Pré-requisitos (`- [ ]`, fora dos passos) e cada passo numerado
 *   (lista dentro de <div class="steps">) viram caixas de verificação.
 * - Estado salvo só no localStorage deste navegador, na chave
 *   "checklist:<procedureId>", com o formato { count, checked: {índice: bool} }.
 *   Se o número de itens da página mudar, o estado salvo é descartado.
 * - "Limpar checklist" pede confirmação e zera o procedimento.
 * - Compatível com navigation.instant (document$ do Material).
 */
(function () {
  "use strict";

  var PREFIX = "checklist:";

  function load(id) {
    try {
      var raw = window.localStorage.getItem(PREFIX + id);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed.count !== "number" || typeof parsed.checked !== "object" || !parsed.checked) {
        return null;
      }
      var checked = {};
      Object.keys(parsed.checked).forEach(function (k) {
        var i = Number(k);
        if (Number.isInteger(i)) checked[i] = parsed.checked[k] === true;
      });
      return { count: parsed.count, checked: checked };
    } catch (e) {
      return null;
    }
  }

  function save(id, count, checked) {
    try {
      window.localStorage.setItem(PREFIX + id, JSON.stringify({ count: count, checked: checked }));
    } catch (e) {
      /* armazenamento indisponível (modo privado, cota): segue sem salvar */
    }
  }

  function clear(id) {
    try {
      window.localStorage.removeItem(PREFIX + id);
    } catch (e) {
      /* idem */
    }
  }

  function textOf(el) {
    return (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
  }

  function init() {
    var root = document.querySelector(".checklist-controls[data-procedure-id]");
    if (!root || root.dataset.ready === "1") return;
    root.dataset.ready = "1";
    var id = root.dataset.procedureId;
    var article = root.closest("article") || document;

    var entries = [];

    // Pré-requisitos: task lists fora dos passos.
    article.querySelectorAll("li.task-list-item input[type=checkbox]").forEach(function (input) {
      if (input.closest(".steps")) return;
      var li = input.closest("li");
      input.disabled = false;
      input.setAttribute("aria-label", "Pré-requisito: " + textOf(li));
      entries.push({ item: li, checkbox: input });
    });

    // Passos: cada <li> de primeiro nível da lista numerada.
    article.querySelectorAll(".steps > ol").forEach(function (ol) {
      var start = Number(ol.getAttribute("start") || 1);
      Array.prototype.forEach.call(ol.children, function (li, pos) {
        if (li.tagName !== "LI") return;
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.className = "checklist-step-checkbox";
        cb.setAttribute("aria-label", "Passo " + (start + pos) + ": " + textOf(li));
        // Na mesma linha do título do passo (primeiro parágrafo), quando houver.
        var first = li.firstElementChild;
        var host = first && first.tagName === "P" ? first : li;
        host.insertBefore(cb, host.firstChild);
        entries.push({ item: li, checkbox: cb });
      });
    });

    var total = entries.length;
    if (total === 0) return;

    var state = load(id);
    if (state && state.count !== total) {
      clear(id);
      state = null;
    }
    state = state || { count: total, checked: {} };

    var progress = root.querySelector(".checklist-progress");

    function refresh() {
      var done = 0;
      entries.forEach(function (e) {
        e.item.classList.toggle("checklist-checked", e.checkbox.checked);
        if (e.checkbox.checked) done++;
      });
      if (progress) progress.textContent = done + " de " + total + " itens marcados";
    }

    function persist() {
      var checked = {};
      entries.forEach(function (e, i) {
        checked[i] = e.checkbox.checked;
      });
      save(id, total, checked);
    }

    entries.forEach(function (e, i) {
      e.checkbox.checked = !!state.checked[i];
      e.checkbox.addEventListener("change", function () {
        refresh();
        persist();
      });
    });
    refresh();

    var printBtn = root.querySelector(".checklist-print-button");
    if (printBtn) {
      printBtn.addEventListener("click", function () {
        window.print();
      });
    }

    var clearBtn = root.querySelector(".checklist-clear-button");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        if (!window.confirm("Limpar progresso deste procedimento?")) return;
        clear(id);
        entries.forEach(function (e) {
          e.checkbox.checked = false;
        });
        refresh();
        entries[0].checkbox.focus();
      });
    }
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
