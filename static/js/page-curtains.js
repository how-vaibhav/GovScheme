/**
 * GovAid — Professional Page Curtains
 * Effects: fade · wipe (multi-stripe) · doors · iris
 */
(function () {
  "use strict";

  var EFFECTS = ["fade", "wipe", "doors", "iris"];
  var DUR_OUT = 500;
  var DUR_IN  = 400;
  var STRIPES = 5;          // number of wipe stripes

  var effectIndex     = 0;
  var isTransitioning = false;
  var prefersReduced  = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function el(id) { return document.getElementById(id); }
  function nextEffect() {
    var e = EFFECTS[effectIndex % EFFECTS.length];
    effectIndex++;
    return e;
  }

  /* ───────────── CSS ───────────── */
  function injectStyles() {
    if (el("pc-styles")) return;
    var s = document.createElement("style");
    s.id = "pc-styles";

    /* Build per-stripe keyframe delays */
    var stripeCSS = "";
    for (var i = 0; i < STRIPES; i++) {
      var delay = Math.round(i * (DUR_OUT / STRIPES / 2));
      stripeCSS += [
        "#pc-wipe .pc-stripe:nth-child(" + (i + 1) + ") {",
        "  transition-delay: " + delay + "ms;",
        "}",
      ].join("");
    }

    s.textContent = [
      ":root{",
      "  --pc-dur-out:" + DUR_OUT + "ms;",
      "  --pc-dur-in:"  + DUR_IN  + "ms;",
      "  --pc-ease-close:cubic-bezier(0.87,0,0.13,1);",
      "  --pc-ease-open:cubic-bezier(0.87,0,0.13,1);",
      "  --pc-c1:#0a0f1e;",
      "  --pc-c2:#1e3a8a;",
      "  --pc-c3:#1d4ed8;",
      "}",
      "html.dark{--pc-c1:#020617;--pc-c2:#0f172a;--pc-c3:#1e40af;}",

      /* root */
      "#pc-root{pointer-events:none;position:fixed;inset:0;z-index:9998;}",

      /* ═════ FADE ═════ */
      "#pc-fade{",
      "  position:absolute;inset:0;",
      "  background:linear-gradient(160deg,var(--pc-c1) 0%,var(--pc-c2) 45%,var(--pc-c3) 100%);",
      "  opacity:0;transform:translateZ(0);will-change:opacity;",
      "  transition:opacity var(--pc-dur-out) var(--pc-ease-close);",
      "}",
      "#pc-fade.pc-show{opacity:1;}",
      "#pc-fade.pc-hide{opacity:0;transition:opacity var(--pc-dur-in) var(--pc-ease-open);}",

      /* ═════ MULTI-STRIPE WIPE ═════ */
      /* Container */
      "#pc-wipe{",
      "  position:absolute;inset:0;",
      "  display:flex;flex-direction:row;",
      "  pointer-events:none;",
      "}",
      /* Each stripe */
      "#pc-wipe .pc-stripe{",
      "  flex:1;",
      "  position:relative;",
      "  transform:scaleY(0);",
      "  transform-origin:bottom center;",
      "  transition:transform var(--pc-dur-out) var(--pc-ease-close);",
      "  will-change:transform;",
      "  overflow:hidden;",
      "}",
      /* Gradient fill on each stripe */
      "#pc-wipe .pc-stripe::before{",
      "  content:'';",
      "  position:absolute;inset:0;",
      "  background:linear-gradient(180deg,var(--pc-c3) 0%,var(--pc-c2) 60%,var(--pc-c1) 100%);",
      "}",
      /* Subtle shimmer line at leading edge of each stripe */
      "#pc-wipe .pc-stripe::after{",
      "  content:'';",
      "  position:absolute;",
      "  top:0;left:0;right:0;height:3px;",
      "  background:linear-gradient(90deg,transparent,rgba(147,197,253,.7),transparent);",
      "  opacity:0;",
      "  transition:opacity 150ms ease;",
      "}",
      "#pc-wipe.pc-show .pc-stripe::after{opacity:1;}",
      /* Show: stripes unfold from bottom */
      "#pc-wipe.pc-show .pc-stripe{transform:scaleY(1);}",
      /* Hide: stripes fold back from top (reverse origin) */
      "#pc-wipe.pc-hide .pc-stripe{",
      "  transform:scaleY(0);",
      "  transform-origin:top center;",
      "  transition:transform var(--pc-dur-in) var(--pc-ease-open);",
      "}",
      /* Stagger delays (generated above) */
      stripeCSS,
      /* Reverse stagger on hide (mirror) */
      (function(){
        var r="";
        for(var i=0;i<STRIPES;i++){
          var d = Math.round((STRIPES-1-i)*(DUR_IN/STRIPES/2));
          r+="#pc-wipe.pc-hide .pc-stripe:nth-child("+(i+1)+"){transition-delay:"+d+"ms;}";
        }
        return r;
      })(),

      /* ═════ DOORS ═════ */
      "#pc-dl,#pc-dr{",
      "  position:absolute;top:0;bottom:0;width:0%;",
      "  background:linear-gradient(160deg,var(--pc-c1) 0%,var(--pc-c2) 45%,var(--pc-c3) 100%);",
      "  transform:translateZ(0);will-change:width;",
      "  transition:width var(--pc-dur-out) var(--pc-ease-close);",
      "}",
      "#pc-dl{left:0;background:linear-gradient(135deg,var(--pc-c1),var(--pc-c2));}",
      "#pc-dr{right:0;background:linear-gradient(225deg,var(--pc-c1),var(--pc-c2));}",
      /* Door edge glows */
      "#pc-dl::after{content:'';position:absolute;top:0;bottom:0;right:0;width:3px;background:linear-gradient(180deg,transparent,#60a5fa,transparent);}",
      "#pc-dr::after{content:'';position:absolute;top:0;bottom:0;left:0;width:3px;background:linear-gradient(180deg,transparent,#60a5fa,transparent);}",
      "#pc-dl.pc-show,#pc-dr.pc-show{width:51%;}",
      "#pc-dl.pc-hide,#pc-dr.pc-hide{width:0%;transition:width var(--pc-dur-in) var(--pc-ease-open);}",

      /* ═════ IRIS ═════ */
      "#pc-iris{",
      "  position:absolute;inset:0;",
      "  background:radial-gradient(circle at 50% 46%,var(--pc-c3) 0%,var(--pc-c2) 40%,var(--pc-c1) 100%);",
      "  clip-path:circle(0% at 50% 46%);",
      "  transform:translateZ(0);will-change:clip-path;",
      "  transition:clip-path var(--pc-dur-out) var(--pc-ease-close);",
      "}",
      "#pc-iris.pc-show{clip-path:circle(150% at 50% 46%);}",
      "#pc-iris.pc-hide{clip-path:circle(0% at 50% 46%);transition:clip-path var(--pc-dur-in) var(--pc-ease-open);}",

      /* ═════ Brand badge (centre) ═════ */
      "#pc-brand{",
      "  position:absolute;top:50%;left:50%;",
      "  transform:translate(-50%,-54%);",
      "  display:flex;flex-direction:column;align-items:center;gap:.9rem;",
      "  opacity:0;transition:opacity 180ms ease 220ms;",
      "  pointer-events:none;z-index:2;",
      "}",
      "#pc-brand.pc-brand-show{opacity:1;}",
      "#pc-brand .pc-logo{",
      "  width:52px;height:52px;border-radius:50%;",
      "  background:rgba(255,255,255,.08);",
      "  border:1px solid rgba(255,255,255,.15);",
      "  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);",
      "  display:flex;align-items:center;justify-content:center;",
      "  box-shadow:0 0 32px rgba(59,130,246,.45),inset 0 1px 0 rgba(255,255,255,.12);",
      "}",
      "#pc-brand .pc-logo i{font-size:1.35rem;color:#93c5fd;animation:pc-pulse 1.5s ease-in-out infinite;}",
      "@keyframes pc-pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.65;transform:scale(.9)}}",
      "#pc-brand .pc-name{font:700 1rem/1 'Inter',system-ui,sans-serif;color:#f0f9ff;letter-spacing:.07em;}",
      "#pc-brand .pc-sub{font:400 .62rem/1 'Inter',system-ui,sans-serif;color:#93c5fd;letter-spacing:.14em;text-transform:uppercase;margin-top:-.35rem;}",
      "#pc-spinner{width:32px;height:32px;border-radius:50%;border:2px solid rgba(147,197,253,.15);border-top-color:#60a5fa;animation:pc-spin .7s linear infinite;}",
      "@keyframes pc-spin{to{transform:rotate(360deg)}}",

      /* ═════ Progress bar ═════ */
      "#pc-progress{",
      "  position:fixed;top:0;left:0;height:2.5px;",
      "  background:linear-gradient(90deg,#3b82f6,#60a5fa,#bfdbfe);",
      "  width:0%;z-index:10001;opacity:0;",
      "  transition:width .18s ease,opacity .3s ease;",
      "  box-shadow:0 0 8px rgba(59,130,246,.8),0 0 20px rgba(59,130,246,.35);",
      "}",
      "#pc-progress.pc-bar-on{opacity:1;}",
      "#pc-progress.pc-bar-done{opacity:0;width:100%!important;transition:width .12s ease,opacity .45s ease .12s;}",

      /* ═════ Content entrance ═════ */
      ".pc-enter{animation:pc-enter " + (DUR_IN + 120) + "ms cubic-bezier(0.22,1,0.36,1) both;}",
      "@keyframes pc-enter{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}",

      "html.pc-busy a,html.pc-busy button{pointer-events:none!important;}",
      "html.pc-busy{cursor:wait;}",
    ].join("\n");
    document.head.appendChild(s);
  }

  /* ───────────── DOM ───────────── */
  function buildDOM() {
    if (el("pc-root")) return;

    var bar = document.createElement("div");
    bar.id = "pc-progress";
    document.body.appendChild(bar);

    var root = document.createElement("div");
    root.id = "pc-root";
    root.setAttribute("aria-hidden","true");

    /* Build stripe divs */
    var stripeHTML = "";
    for (var i = 0; i < STRIPES; i++) {
      stripeHTML += '<div class="pc-stripe"></div>';
    }

    root.innerHTML = [
      '<div id="pc-fade"></div>',
      '<div id="pc-wipe">' + stripeHTML + '</div>',
      '<div id="pc-dl"></div>',
      '<div id="pc-dr"></div>',
      '<div id="pc-iris"></div>',
      '<div id="pc-brand">',
      '  <div class="pc-logo"><i class="fas fa-landmark"></i></div>',
      '  <div class="pc-name">GovAid</div>',
      '  <div class="pc-sub">Sikkim Portal</div>',
      '  <div id="pc-spinner"></div>',
      '</div>',
    ].join("");
    document.body.appendChild(root);
  }

  /* ───────────── Layer state ───────────── */
  function resetLayers() {
    ["pc-fade","pc-wipe","pc-dl","pc-dr","pc-iris"].forEach(function(id){
      var n = el(id);
      if (n) n.classList.remove("pc-show","pc-hide");
    });
    var brand = el("pc-brand");
    if (brand) brand.classList.remove("pc-brand-show");
  }

  function showCurtain(effect) {
    resetLayers();
    void el("pc-root").offsetWidth;
    el("pc-" + (effect === "doors" ? "dl" : effect)).classList.add("pc-show");
    if (effect === "doors") el("pc-dr").classList.add("pc-show");
    setTimeout(function(){
      var b = el("pc-brand");
      if (b) b.classList.add("pc-brand-show");
    }, DUR_OUT * 0.45);
  }

  function hideCurtain(effect) {
    var brand = el("pc-brand");
    if (brand) brand.classList.remove("pc-brand-show");
    el("pc-" + (effect === "doors" ? "dl" : effect)).classList.replace("pc-show","pc-hide");
    if (effect === "doors") el("pc-dr").classList.replace("pc-show","pc-hide");
  }

  /* ───────────── Progress bar ───────────── */
  function barStart() {
    var b = el("pc-progress");
    if (!b) return;
    b.style.width = "0%";
    b.classList.remove("pc-bar-done");
    void b.offsetWidth;
    b.classList.add("pc-bar-on");
    setTimeout(function(){ b.style.width="28%"; }, 40);
    setTimeout(function(){ b.style.width="52%"; }, 180);
    setTimeout(function(){ b.style.width="70%"; }, 340);
    setTimeout(function(){ b.style.width="86%"; }, 520);
  }
  function barDone() {
    var b = el("pc-progress");
    if (!b) return;
    b.style.width = "100%";
    b.classList.add("pc-bar-done");
    setTimeout(function(){ b.classList.remove("pc-bar-on","pc-bar-done"); b.style.width="0%"; }, 700);
  }

  /* ───────────── Content entrance ───────────── */
  function animateContent() {
    if (prefersReduced) return;
    var main = document.querySelector("main") || document.querySelector(".container");
    if (!main) return;
    main.classList.add("pc-enter");
    main.addEventListener("animationend", function(){ main.classList.remove("pc-enter"); }, { once:true });
  }

  /* ───────────── Navigate ───────────── */
  function goTo(href, effect) {
    if (isTransitioning) return;
    if (prefersReduced) { window.location.href = href; return; }
    isTransitioning = true;
    try { sessionStorage.setItem("pc-arrival-effect", effect); } catch(e) {}
    document.documentElement.classList.add("pc-busy");
    barStart();
    showCurtain(effect);
    setTimeout(function(){ window.location.href = href; }, DUR_OUT + 30);
    setTimeout(function(){
      isTransitioning = false;
      document.documentElement.classList.remove("pc-busy");
    }, DUR_OUT + 4000);
  }

  /* ───────────── Entry reveal ───────────── */
  function playEntry() {
    var effect;
    try { effect = sessionStorage.getItem("pc-arrival-effect"); } catch(e) {}
    if (!effect) { animateContent(); return; }
    try { sessionStorage.removeItem("pc-arrival-effect"); } catch(e) {}
    if (prefersReduced) { animateContent(); return; }

    /* Snap to closed without transition */
    var ids = ["pc-fade","pc-wipe","pc-dl","pc-dr","pc-iris"];
    ids.forEach(function(id){ var n=el(id); if(n) n.style.transition="none"; });
    /* also suppress stripe transitions */
    var stripes = el("pc-wipe") ? el("pc-wipe").querySelectorAll(".pc-stripe") : [];
    stripes.forEach(function(s){ s.style.transition="none"; s.style.transitionDelay="0ms"; });
    void el("pc-root").offsetWidth;

    resetLayers();
    el("pc-" + (effect === "doors" ? "dl" : effect)).classList.add("pc-show");
    if (effect === "doors") el("pc-dr").classList.add("pc-show");

    requestAnimationFrame(function(){
      requestAnimationFrame(function(){
        /* Re-enable transitions */
        ids.forEach(function(id){ var n=el(id); if(n) n.style.transition=""; });
        stripes.forEach(function(s){ s.style.transition=""; s.style.transitionDelay=""; });
        barDone();
        hideCurtain(effect);
        setTimeout(function(){
          resetLayers();
          isTransitioning = false;
          document.documentElement.classList.remove("pc-busy");
          animateContent();
        }, DUR_IN + 100);
      });
    });
  }

  /* ───────────── Link filter ───────────── */
  function isInternal(a) {
    if (!a || !a.href) return false;
    try {
      var url = new URL(a.href);
      if (url.origin !== location.origin)             return false;
      if (a.target === "_blank")                      return false;
      var raw = a.getAttribute("href") || "";
      if (!raw || raw === "#" || raw.charAt(0) === "#") return false;
      if (a.hasAttribute("download"))                 return false;
      if (url.protocol !== "http:" && url.protocol !== "https:") return false;
      if (a.hasAttribute("data-no-curtain"))          return false;
      if (url.href === location.href)                 return false;
      return true;
    } catch(e){ return false; }
  }

  /* ───────────── Init ───────────── */
  function init() {
    injectStyles();
    buildDOM();
    playEntry();
    document.addEventListener("click", function(e){
      var a = e.target.closest("a");
      if (!a || !isInternal(a)) return;
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      goTo(a.href, nextEffect());
    }, { capture: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
