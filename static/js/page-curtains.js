/**
 * Page Curtains — Vanilla JS
 * Inspired by Motion for React's @motion/page-curtains component.
 * Effects: fade · wipe · doors · iris
 */
(function () {
  "use strict";

  const EFFECTS = ["fade", "wipe", "doors", "iris"];
  let effectIndex = 0;

  function nextEffect() {
    const e = EFFECTS[effectIndex % EFFECTS.length];
    effectIndex++;
    return e;
  }

  function el(id) { return document.getElementById(id); }

  /* ── Build curtain DOM ── */
  function buildCurtain() {
    if (el("page-curtain-root")) return;
    const root = document.createElement("div");
    root.id = "page-curtain-root";
    root.setAttribute("aria-hidden", "true");
    root.innerHTML = `
      <div id="pc-cover"></div>
      <div id="pc-door-left"  class="pc-door"></div>
      <div id="pc-door-right" class="pc-door"></div>
      <div id="pc-iris"></div>
      <div id="pc-wipe"></div>
      <div id="pc-label" aria-live="polite"></div>
    `;
    document.body.appendChild(root);
  }

  /* ── Inject CSS ── */
  function injectStyles() {
    if (el("page-curtain-styles")) return;
    const style = document.createElement("style");
    style.id = "page-curtain-styles";
    style.textContent = `
      :root {
        --pc-color: #1d4ed8;
        --pc-duration-out: 420ms;
        --pc-duration-in:  340ms;
        --pc-ease: cubic-bezier(0.76, 0, 0.24, 1);
      }
      html.dark { --pc-color: #1e40af; }

      #page-curtain-root {
        pointer-events: none;
        position: fixed;
        inset: 0;
        z-index: 9999;
      }

      /* FADE */
      #pc-cover {
        position: absolute; inset: 0;
        background: var(--pc-color);
        opacity: 0;
        transform: translateZ(0);
        transition: opacity var(--pc-duration-out) var(--pc-ease);
      }
      #pc-cover.pc-visible { opacity: 1; }
      #pc-cover.pc-hiding  { opacity: 0; transition: opacity var(--pc-duration-in) var(--pc-ease); }

      /* WIPE */
      #pc-wipe {
        position: absolute; top: 0; bottom: 0; left: 0;
        width: 0%;
        background: linear-gradient(90deg, var(--pc-color), color-mix(in srgb, var(--pc-color) 80%, #60a5fa));
        transform: translateZ(0);
        transition: width var(--pc-duration-out) var(--pc-ease);
      }
      #pc-wipe.pc-visible { width: 100%; }
      #pc-wipe.pc-hiding  { width: 0%; left: auto; right: 0; transition: width var(--pc-duration-in) var(--pc-ease); }

      /* DOORS */
      .pc-door {
        position: absolute; top: 0; bottom: 0;
        width: 0%;
        background: linear-gradient(135deg, var(--pc-color), color-mix(in srgb, var(--pc-color) 70%, #1e3a8a));
        transform: translateZ(0);
        transition: width var(--pc-duration-out) var(--pc-ease);
      }
      #pc-door-left  { left: 0; }
      #pc-door-right { right: 0; }
      #pc-door-left.pc-visible,
      #pc-door-right.pc-visible { width: 50%; }
      #pc-door-left.pc-hiding,
      #pc-door-right.pc-hiding  { width: 0%; transition: width var(--pc-duration-in) var(--pc-ease); }

      /* IRIS */
      #pc-iris {
        position: absolute; top: 50%; left: 50%;
        width: 0px; height: 0px;
        border-radius: 50%;
        background: radial-gradient(circle, color-mix(in srgb, var(--pc-color) 90%, #60a5fa), var(--pc-color));
        transform: translate(-50%, -50%) scale(0) translateZ(0);
        transition: transform var(--pc-duration-out) var(--pc-ease),
                    width var(--pc-duration-out) var(--pc-ease),
                    height var(--pc-duration-out) var(--pc-ease);
      }
      #pc-iris.pc-visible {
        width: 300vmax; height: 300vmax;
        transform: translate(-50%, -50%) scale(1) translateZ(0);
      }
      #pc-iris.pc-hiding {
        width: 0px; height: 0px;
        transform: translate(-50%, -50%) scale(0) translateZ(0);
        transition: transform var(--pc-duration-in) var(--pc-ease),
                    width var(--pc-duration-in) var(--pc-ease),
                    height var(--pc-duration-in) var(--pc-ease);
      }

      /* LABEL */
      #pc-label {
        position: fixed;
        bottom: 1.5rem; left: 50%;
        transform: translateX(-50%) translateY(140%);
        background: rgba(15,23,42,0.92);
        color: #f8fafc;
        font: 600 0.72rem/1 'Inter', sans-serif;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        border: 1px solid rgba(148,163,184,0.2);
        backdrop-filter: blur(8px);
        opacity: 0;
        transition: opacity 220ms ease, transform 220ms ease;
        pointer-events: none;
        z-index: 10000;
        white-space: nowrap;
      }
      #pc-label.pc-label-show {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }

      html.pc-navigating * { pointer-events: none !important; }
    `;
    document.head.appendChild(style);
  }

  /* ── Reset all layers ── */
  function resetAll() {
    ["pc-cover","pc-wipe","pc-door-left","pc-door-right","pc-iris"].forEach(function(id) {
      var node = el(id);
      if (!node) return;
      node.className = node.id === "pc-door-left" || node.id === "pc-door-right" ? "pc-door" : "";
      if (id === "pc-wipe") { node.style.left = "0"; node.style.right = ""; }
    });
  }

  function showElements(effect) {
    resetAll();
    if (effect === "fade")  { el("pc-cover").getBoundingClientRect(); el("pc-cover").classList.add("pc-visible"); }
    if (effect === "wipe")  { el("pc-wipe").getBoundingClientRect();  el("pc-wipe").classList.add("pc-visible"); }
    if (effect === "doors") { el("pc-door-left").getBoundingClientRect(); el("pc-door-left").classList.add("pc-visible"); el("pc-door-right").classList.add("pc-visible"); }
    if (effect === "iris")  { el("pc-iris").getBoundingClientRect(); el("pc-iris").classList.add("pc-visible"); }
  }

  function hideElements(effect) {
    if (effect === "fade")  { el("pc-cover").classList.replace("pc-visible","pc-hiding"); }
    if (effect === "wipe")  { el("pc-wipe").style.left="auto"; el("pc-wipe").style.right="0"; el("pc-wipe").classList.replace("pc-visible","pc-hiding"); }
    if (effect === "doors") { el("pc-door-left").classList.replace("pc-visible","pc-hiding"); el("pc-door-right").classList.replace("pc-visible","pc-hiding"); }
    if (effect === "iris")  { el("pc-iris").classList.replace("pc-visible","pc-hiding"); }
  }

  /* ── Label ── */
  var labelTimer = null;
  function showLabel(effect) {
    var label = el("pc-label");
    if (!label) return;
    clearTimeout(labelTimer);
    label.textContent = effect.charAt(0).toUpperCase() + effect.slice(1);
    label.classList.add("pc-label-show");
    labelTimer = setTimeout(function(){ label.classList.remove("pc-label-show"); }, 1600);
  }

  /* ── Duration ── */
  function getDuration(cssVar) {
    var raw = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim();
    return parseInt(raw, 10) || 400;
  }

  /* ── Navigate ── */
  var isTransitioning = false;

  function navigateTo(href, effect) {
    if (isTransitioning) return;
    isTransitioning = true;
    document.documentElement.classList.add("pc-navigating");
    sessionStorage.setItem("pc-arrival-effect", effect);
    showElements(effect);
    showLabel(effect);
    var outDuration = getDuration("--pc-duration-out");
    setTimeout(function(){ window.location.href = href; }, outDuration + 30);
    setTimeout(function(){
      isTransitioning = false;
      document.documentElement.classList.remove("pc-navigating");
    }, outDuration + 2500);
  }

  /* ── Is internal link? ── */
  function isInternal(anchor) {
    if (!anchor || !anchor.href) return false;
    try {
      var url = new URL(anchor.href);
      if (url.origin !== location.origin) return false;
      if (anchor.target === "_blank") return false;
      var h = anchor.getAttribute("href") || "";
      if (h === "#" || h.startsWith("#")) return false;
      if (anchor.hasAttribute("download")) return false;
      if (url.protocol !== "http:" && url.protocol !== "https:") return false;
      if (anchor.hasAttribute("data-no-curtain")) return false;
      if (anchor.href === location.href) return false;
      return true;
    } catch(e) { return false; }
  }

  /* ── Entry animation (reveal on page load) ── */
  function playEntry() {
    var effect = sessionStorage.getItem("pc-arrival-effect") || "fade";
    sessionStorage.removeItem("pc-arrival-effect");
    var inDuration = getDuration("--pc-duration-in");

    // Disable transitions temporarily
    ["pc-cover","pc-wipe","pc-door-left","pc-door-right","pc-iris"].forEach(function(id){
      var node = el(id);
      if (node) node.style.transition = "none";
    });

    // Set immediately visible
    resetAll();
    if (effect === "fade")  { el("pc-cover").classList.add("pc-visible"); }
    if (effect === "wipe")  { el("pc-wipe").classList.add("pc-visible"); var w=el("pc-wipe"); w.style.width="100%"; }
    if (effect === "doors") { el("pc-door-left").classList.add("pc-visible"); el("pc-door-right").classList.add("pc-visible"); }
    if (effect === "iris")  { var iris=el("pc-iris"); iris.style.width="300vmax"; iris.style.height="300vmax"; iris.classList.add("pc-visible"); }

    requestAnimationFrame(function(){
      requestAnimationFrame(function(){
        // Re-enable transitions
        ["pc-cover","pc-wipe","pc-door-left","pc-door-right","pc-iris"].forEach(function(id){
          var node = el(id);
          if (node) node.style.transition = "";
        });
        hideElements(effect);
        setTimeout(function(){
          isTransitioning = false;
          document.documentElement.classList.remove("pc-navigating");
        }, inDuration + 100);
      });
    });
  }

  /* ── Click intercept ── */
  document.addEventListener("click", function(e){
    var anchor = e.target.closest("a");
    if (!anchor) return;
    if (!isInternal(anchor)) return;
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    navigateTo(anchor.href, nextEffect());
  }, { capture: true });

  /* ── Init ── */
  function init() {
    injectStyles();
    buildCurtain();
    playEntry();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
