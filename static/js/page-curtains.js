/**
 * Page Curtains — Vanilla JS (fixed & polished)
 * Inspired by Motion for React @motion/page-curtains
 * Effects cycle: fade → wipe → doors → iris
 *
 * Bug fixes vs v1:
 *  - No blue flash on fresh page loads (entry only plays if arriving from an
 *    in-app navigation, not on external/direct opens)
 *  - Single click listener (removed duplicate registration)
 *  - Gradient shimmer on curtain layers for a premium look
 *  - Smooth iris uses clip-path instead of width/height (no layout thrash)
 *  - Effect label has icon + name
 */
(function () {
  "use strict";

  /* ── Effect cycle ── */
  var EFFECTS = ["fade", "wipe", "doors", "iris"];
  var effectIndex = 0;
  function nextEffect() {
    var e = EFFECTS[effectIndex % EFFECTS.length];
    effectIndex++;
    return e;
  }

  /* ── Helpers ── */
  function el(id) { return document.getElementById(id); }

  var isTransitioning = false;
  var labelTimer = null;

  /* ─────────────────────────────────────────
     CSS  (injected once)
  ───────────────────────────────────────── */
  function injectStyles() {
    if (el("page-curtain-styles")) return;
    var style = document.createElement("style");
    style.id = "page-curtain-styles";
    style.textContent = [
      ":root {",
      "  --pc-color-1: #1d4ed8;",           /* blue-700  */
      "  --pc-color-2: #312e81;",           /* indigo-900*/
      "  --pc-dur-out: 500ms;",
      "  --pc-dur-in:  420ms;",
      "  --pc-ease-close: cubic-bezier(0.87, 0, 0.13, 1);",
      "  --pc-ease-open:  cubic-bezier(0.87, 0, 0.13, 1);",
      "}",
      "html.dark { --pc-color-1: #1e3a8a; --pc-color-2: #0f172a; }",

      /* Root */
      "#page-curtain-root {",
      "  pointer-events: none;",
      "  position: fixed; inset: 0; z-index: 9999;",
      "}",

      /* Shared gradient used by every layer */
      "#page-curtain-root .pc-layer {",
      "  background: linear-gradient(135deg,",
      "    var(--pc-color-1) 0%,",
      "    var(--pc-color-2) 60%,",
      "    #0f172a 100%",
      "  );",
      "}",

      /* ── FADE ── */
      "#pc-cover {",
      "  position: absolute; inset: 0;",
      "  opacity: 0;",
      "  transform: translateZ(0);",
      "  transition: opacity var(--pc-dur-out) var(--pc-ease-close);",
      "  will-change: opacity;",
      "}",
      "#pc-cover.pc-show { opacity: 1; }",
      "#pc-cover.pc-hide {",
      "  opacity: 0;",
      "  transition: opacity var(--pc-dur-in) var(--pc-ease-open);",
      "}",

      /* ── WIPE ── */
      "#pc-wipe {",
      "  position: absolute; top: 0; bottom: 0; left: 0;",
      "  width: 0%;",
      "  transform: translateZ(0);",
      "  transition: width var(--pc-dur-out) var(--pc-ease-close);",
      "  will-change: width;",
      "}",
      "#pc-wipe.pc-show { width: 100%; }",
      "#pc-wipe.pc-hide {",
      "  left: auto; right: 0; width: 0%;",
      "  transition: width var(--pc-dur-in) var(--pc-ease-open);",
      "}",

      /* ── DOORS ── */
      ".pc-door {",
      "  position: absolute; top: 0; bottom: 0;",
      "  width: 0%;",
      "  transform: translateZ(0);",
      "  transition: width var(--pc-dur-out) var(--pc-ease-close);",
      "  will-change: width;",
      "}",
      "#pc-door-left  { left: 0; }",
      "#pc-door-right { right: 0; }",
      "#pc-door-left.pc-show,",
      "#pc-door-right.pc-show { width: 50.2%; }",  /* 0.2% overlap seam fix */
      "#pc-door-left.pc-hide,",
      "#pc-door-right.pc-hide {",
      "  width: 0%;",
      "  transition: width var(--pc-dur-in) var(--pc-ease-open);",
      "}",

      /* ── IRIS (clip-path circle — no layout thrash) ── */
      "#pc-iris {",
      "  position: absolute; inset: 0;",
      "  /* Start as invisible pinpoint at centre */",
      "  clip-path: circle(0% at 50% 50%);",
      "  transform: translateZ(0);",
      "  transition: clip-path var(--pc-dur-out) var(--pc-ease-close);",
      "  will-change: clip-path;",
      "}",
      "#pc-iris.pc-show {",
      "  clip-path: circle(150% at 50% 50%);",
      "}",
      "#pc-iris.pc-hide {",
      "  clip-path: circle(0% at 50% 50%);",
      "  transition: clip-path var(--pc-dur-in) var(--pc-ease-open);",
      "}",

      /* Shimmer sweep across curtain for premium feel */
      "#page-curtain-root .pc-layer::after {",
      "  content: '';",
      "  position: absolute; inset: 0;",
      "  background: linear-gradient(105deg,",
      "    transparent 40%,",
      "    rgba(255,255,255,0.07) 50%,",
      "    transparent 60%",
      "  );",
      "  background-size: 200% 100%;",
      "  animation: pc-shimmer 1.4s linear infinite;",
      "}",
      "@keyframes pc-shimmer {",
      "  from { background-position: 200% 0; }",
      "  to   { background-position: -200% 0; }",
      "}",

      /* ── LABEL ── */
      "#pc-label {",
      "  position: fixed;",
      "  bottom: 1.6rem; left: 50%;",
      "  transform: translateX(-50%) translateY(160%);",
      "  display: flex; align-items: center; gap: 0.4rem;",
      "  background: rgba(2, 6, 23, 0.88);",
      "  color: #e2e8f0;",
      "  font: 600 0.7rem/1 'Inter', system-ui, sans-serif;",
      "  letter-spacing: 0.1em;",
      "  text-transform: uppercase;",
      "  padding: 0.38rem 1rem;",
      "  border-radius: 9999px;",
      "  border: 1px solid rgba(148,163,184,0.18);",
      "  backdrop-filter: blur(12px);",
      "  -webkit-backdrop-filter: blur(12px);",
      "  opacity: 0;",
      "  transition: opacity 240ms ease, transform 240ms cubic-bezier(0.34,1.56,0.64,1);",
      "  pointer-events: none;",
      "  z-index: 10000;",
      "  white-space: nowrap;",
      "  box-shadow: 0 4px 24px rgba(0,0,0,0.4);",
      "}",
      "#pc-label .pc-label-dot {",
      "  width: 6px; height: 6px;",
      "  border-radius: 50%;",
      "  background: #60a5fa;",
      "  flex-shrink: 0;",
      "}",
      "#pc-label.pc-label-show {",
      "  opacity: 1;",
      "  transform: translateX(-50%) translateY(0);",
      "}",

      /* Lock interactions during transition */
      "html.pc-navigating { cursor: wait; }",
      "html.pc-navigating a,",
      "html.pc-navigating button { pointer-events: none !important; }",
    ].join("\n");
    document.head.appendChild(style);
  }

  /* ─────────────────────────────────────────
     DOM  (built once, reused every navigation)
  ───────────────────────────────────────── */
  function buildDOM() {
    if (el("page-curtain-root")) return;
    var root = document.createElement("div");
    root.id = "page-curtain-root";
    root.setAttribute("aria-hidden", "true");
    root.innerHTML = [
      '<div id="pc-cover"     class="pc-layer"></div>',
      '<div id="pc-wipe"      class="pc-layer"></div>',
      '<div id="pc-door-left" class="pc-door pc-layer"></div>',
      '<div id="pc-door-right"class="pc-door pc-layer"></div>',
      '<div id="pc-iris"      class="pc-layer"></div>',
      '<div id="pc-label"     aria-live="polite">',
      '  <span class="pc-label-dot"></span>',
      '  <span id="pc-label-text"></span>',
      '</div>',
    ].join("");
    document.body.appendChild(root);
  }

  /* ─────────────────────────────────────────
     Reset — remove all state classes
  ───────────────────────────────────────── */
  function resetAll() {
    var ids = ["pc-cover","pc-wipe","pc-door-left","pc-door-right","pc-iris"];
    ids.forEach(function(id) {
      var node = el(id);
      if (!node) return;
      node.classList.remove("pc-show","pc-hide");
      /* Wipe: restore left-to-right direction */
      if (id === "pc-wipe") {
        node.style.left  = "0";
        node.style.right = "auto";
      }
    });
  }

  /* ─────────────────────────────────────────
     Show curtain (EXIT animation)
  ───────────────────────────────────────── */
  function showCurtain(effect) {
    resetAll();
    /* Force reflow so transition fires on the next state change */
    void el("page-curtain-root").offsetWidth;

    if (effect === "fade") {
      el("pc-cover").classList.add("pc-show");
    } else if (effect === "wipe") {
      el("pc-wipe").classList.add("pc-show");
    } else if (effect === "doors") {
      el("pc-door-left").classList.add("pc-show");
      el("pc-door-right").classList.add("pc-show");
    } else if (effect === "iris") {
      el("pc-iris").classList.add("pc-show");
    }
  }

  /* ─────────────────────────────────────────
     Hide curtain (ENTRY / reveal animation)
     Called after the new page DOM is ready.
  ───────────────────────────────────────── */
  function hideCurtain(effect) {
    if (effect === "fade") {
      el("pc-cover").classList.replace("pc-show","pc-hide");
    } else if (effect === "wipe") {
      el("pc-wipe").style.left  = "auto";
      el("pc-wipe").style.right = "0";
      el("pc-wipe").classList.replace("pc-show","pc-hide");
    } else if (effect === "doors") {
      el("pc-door-left").classList.replace("pc-show","pc-hide");
      el("pc-door-right").classList.replace("pc-show","pc-hide");
    } else if (effect === "iris") {
      el("pc-iris").classList.replace("pc-show","pc-hide");
    }
  }

  /* ─────────────────────────────────────────
     Label badge
  ───────────────────────────────────────── */
  var EFFECT_ICONS = { fade:"●", wipe:"►", doors:"◀▶", iris:"◎" };
  function showLabel(effect) {
    var label    = el("pc-label");
    var labelTxt = el("pc-label-text");
    if (!label || !labelTxt) return;
    clearTimeout(labelTimer);
    labelTxt.textContent = (EFFECT_ICONS[effect] || "✦") + "  " + effect.toUpperCase();
    label.classList.add("pc-label-show");
    labelTimer = setTimeout(function() {
      label.classList.remove("pc-label-show");
    }, 1800);
  }

  /* ─────────────────────────────────────────
     Navigate — intercept link click
  ───────────────────────────────────────── */
  function getDur(cssVar) {
    var raw = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim();
    return parseInt(raw,10) || 500;
  }

  function goTo(href, effect) {
    if (isTransitioning) return;
    isTransitioning = true;

    /* Mark which effect the arriving page should use to reveal itself */
    try { sessionStorage.setItem("pc-arrival-effect", effect); } catch(e) {}

    document.documentElement.classList.add("pc-navigating");
    showCurtain(effect);
    showLabel(effect);

    /* Navigate after the curtain has fully covered the screen */
    var dur = getDur("--pc-dur-out");
    setTimeout(function() {
      window.location.href = href;
    }, dur + 20);

    /* Safety valve — unlock if navigation stalls */
    setTimeout(function() {
      isTransitioning = false;
      document.documentElement.classList.remove("pc-navigating");
    }, dur + 3000);
  }

  /* ─────────────────────────────────────────
     Entry reveal — runs on DOMContentLoaded of
     the NEW page. Only animates if we actually
     arrived via an in-app navigation.
  ───────────────────────────────────────── */
  function playEntryReveal() {
    var effect;
    try { effect = sessionStorage.getItem("pc-arrival-effect"); } catch(e) {}
    /* ← KEY FIX: no fallback — if no stored effect we were NOT doing
       an in-app navigation (direct URL, external link, browser refresh).
       In that case skip ALL curtain animation entirely. */
    if (!effect) return;
    try { sessionStorage.removeItem("pc-arrival-effect"); } catch(e) {}

    var inDur = getDur("--pc-dur-in");

    /* Snap the curtain to fully-closed position WITHOUT any CSS transition */
    var ids = ["pc-cover","pc-wipe","pc-door-left","pc-door-right","pc-iris"];
    ids.forEach(function(id) {
      var node = el(id);
      if (node) node.style.transition = "none";
    });
    void el("page-curtain-root").offsetWidth; /* flush */

    /* Depending on effect, force the "fully covered" CSS state instantly */
    resetAll();
    if (effect === "fade") {
      el("pc-cover").classList.add("pc-show");
    } else if (effect === "wipe") {
      var w = el("pc-wipe");
      w.style.width = "100%"; w.style.left = "0"; w.style.right = "auto";
      w.classList.add("pc-show");
    } else if (effect === "doors") {
      el("pc-door-left").classList.add("pc-show");
      el("pc-door-right").classList.add("pc-show");
    } else if (effect === "iris") {
      el("pc-iris").classList.add("pc-show");
    }

    /* Re-enable transitions, then trigger the reveal (open) */
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        ids.forEach(function(id) {
          var node = el(id);
          if (node) node.style.transition = "";
        });
        hideCurtain(effect);
        setTimeout(function() {
          resetAll(); /* fully clean up after reveal */
          isTransitioning = false;
          document.documentElement.classList.remove("pc-navigating");
        }, inDur + 80);
      });
    });
  }

  /* ─────────────────────────────────────────
     Link filter — only intercept same-origin
     non-hash, non-download, non-blank links
  ───────────────────────────────────────── */
  function isInternal(a) {
    if (!a || !a.href) return false;
    try {
      var url = new URL(a.href);
      if (url.origin !== location.origin)              return false;
      if (a.target === "_blank")                       return false;
      var raw = a.getAttribute("href") || "";
      if (raw === "#" || raw.charAt(0) === "#")        return false;
      if (a.hasAttribute("download"))                  return false;
      if (url.protocol !== "http:" && url.protocol !== "https:") return false;
      if (a.hasAttribute("data-no-curtain"))           return false;
      if (url.href === location.href)                  return false;
      return true;
    } catch(e) { return false; }
  }

  /* ─────────────────────────────────────────
     Single click interceptor (registered once)
  ───────────────────────────────────────── */
  function attachClickHandler() {
    document.addEventListener("click", function(e) {
      var a = e.target.closest("a");
      if (!a) return;
      if (!isInternal(a)) return;
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      goTo(a.href, nextEffect());
    }, { capture: true });
  }

  /* ─────────────────────────────────────────
     Bootstrap
  ───────────────────────────────────────── */
  function init() {
    injectStyles();
    buildDOM();
    playEntryReveal();   /* reveals curtain only if arriving from in-app nav */
    attachClickHandler();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

})();
