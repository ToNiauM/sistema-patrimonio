/*
 * zoom.js — clicar numa captura do conteúdo abre a imagem em tela cheia
 * sobre fundo escuro; Esc, o botão × ou um clique fecham.
 * Compatível com navigation.instant (document$ do Material).
 */
(function () {
  "use strict";

  var overlay, overlayImg, caption, opener;

  function build() {
    if (overlay) return;
    overlay = document.createElement("div");
    overlay.className = "zoom-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Imagem ampliada");
    overlay.innerHTML =
      '<button type="button" class="zoom-close" aria-label="Fechar imagem ampliada">&times;</button>' +
      '<img alt="">' +
      '<p class="zoom-caption"></p>';
    overlayImg = overlay.querySelector("img");
    caption = overlay.querySelector(".zoom-caption");
    overlay.addEventListener("click", close);
    document.body.appendChild(overlay);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && overlay.classList.contains("is-open")) close();
    });
  }

  function open(img) {
    build();
    opener = img;
    overlayImg.src = img.currentSrc || img.src;
    overlayImg.alt = img.alt;
    caption.textContent = img.alt;
    overlay.classList.add("is-open");
    overlay.querySelector(".zoom-close").focus();
  }

  function close() {
    if (!overlay) return;
    overlay.classList.remove("is-open");
    overlayImg.removeAttribute("src");
    if (opener) {
      opener.focus();
      opener = null;
    }
  }

  function init() {
    if (overlay && !document.body.contains(overlay)) overlay = null;
    document.querySelectorAll(".md-content article img").forEach(function (img) {
      if (img.dataset.zoom === "1" || img.closest("a") || img.closest(".twemoji")) return;
      img.dataset.zoom = "1";
      img.classList.add("zoomable");
      img.tabIndex = 0;
      img.setAttribute("role", "button");
      img.setAttribute("aria-label", "Ampliar imagem: " + (img.alt || ""));
      img.addEventListener("click", function () {
        open(img);
      });
      img.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open(img);
        }
      });
    });
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
