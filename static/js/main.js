// ==========================================
// Magic UI Animated Theme Toggler Engine (View Transitions API)
// ==========================================

function polygonCollapsed(point, vertexCount) {
  const pairs = Array.from({ length: vertexCount }, () => point).join(", ");
  return `polygon(${pairs})`;
}

function getThemeTransitionClipPaths(variant, cx, cy, maxRadius, viewportWidth, viewportHeight) {
  const toX = (x) => `${(x / viewportWidth) * 100}%`;
  const toY = (y) => `${(y / viewportHeight) * 100}%`;
  const point = (x, y) => `${toX(x)} ${toY(y)}`;
  const toRadius = (r) => `${(r / (Math.hypot(viewportWidth, viewportHeight) / Math.SQRT2)) * 100}%`;

  const shape = variant || "circle";

  switch (shape) {
    case "circle":
      return [
        `circle(0% at ${point(cx, cy)})`,
        `circle(${toRadius(maxRadius)} at ${point(cx, cy)})`,
      ];
    case "square": {
      const halfW = Math.max(cx, viewportWidth - cx);
      const halfH = Math.max(cy, viewportHeight - cy);
      const halfSide = Math.max(halfW, halfH) * 1.05;
      const end = [
        point(cx - halfSide, cy - halfSide),
        point(cx + halfSide, cy - halfSide),
        point(cx + halfSide, cy + halfSide),
        point(cx - halfSide, cy + halfSide),
      ].join(", ");
      return [polygonCollapsed(point(cx, cy), 4), `polygon(${end})`];
    }
    case "triangle": {
      const scale = maxRadius * 2.2;
      const dx = (Math.sqrt(3) / 2) * scale;
      const verts = [
        point(cx, cy - scale),
        point(cx + dx, cy + 0.5 * scale),
        point(cx - dx, cy + 0.5 * scale),
      ].join(", ");
      return [polygonCollapsed(point(cx, cy), 3), `polygon(${verts})`];
    }
    case "diamond": {
      const R = maxRadius * Math.SQRT2;
      const end = [
        point(cx, cy - R),
        point(cx + R, cy),
        point(cx, cy + R),
        point(cx - R, cy),
      ].join(", ");
      return [polygonCollapsed(point(cx, cy), 4), `polygon(${end})`];
    }
    case "hexagon": {
      const R = maxRadius * Math.SQRT2;
      const verts = [];
      for (let i = 0; i < 6; i++) {
        const a = -Math.PI / 2 + (i * Math.PI) / 3;
        verts.push(point(cx + R * Math.cos(a), cy + R * Math.sin(a)));
      }
      return [polygonCollapsed(point(cx, cy), 6), `polygon(${verts.join(", ")})`];
    }
    case "rectangle": {
      const halfW = Math.max(cx, viewportWidth - cx);
      const halfH = Math.max(cy, viewportHeight - cy);
      const end = [
        point(cx - halfW, cy - halfH),
        point(cx + halfW, cy - halfH),
        point(cx + halfW, cy + halfH),
        point(cx - halfW, cy + halfH),
      ].join(", ");
      return [polygonCollapsed(point(cx, cy), 4), `polygon(${end})`];
    }
    case "star": {
      const R = maxRadius * Math.SQRT2 * 1.03;
      const innerRatio = 0.42;
      const starPolygon = (radius) => {
        const verts = [];
        for (let i = 0; i < 5; i++) {
          const outerA = -Math.PI / 2 + (i * 2 * Math.PI) / 5;
          verts.push(point(cx + radius * Math.cos(outerA), cy + radius * Math.sin(outerA)));
          const innerA = outerA + Math.PI / 5;
          verts.push(point(cx + radius * innerRatio * Math.cos(innerA), cy + radius * innerRatio * Math.sin(innerA)));
        }
        return `polygon(${verts.join(", ")})`;
      };
      const startR = Math.max(2, R * 0.025);
      return [starPolygon(startR), starPolygon(R)];
    }
    default:
      return [
        `circle(0% at ${point(cx, cy)})`,
        `circle(${toRadius(maxRadius)} at ${point(cx, cy)})`,
      ];
  }
}

let isThemeTransitioning = false;
let activeThemeAnimation = null;

window.toggleAnimatedTheme = function (event, options = {}) {
  const root = document.documentElement;
  if (isThemeTransitioning || root.dataset.magicuiThemeVt === "active") return;

  const duration = options.duration || 450;
  const shape = options.variant || "circle";
  const fromCenter = options.fromCenter || false;

  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  let x, y;
  const btn = event && (event.currentTarget || event.target?.closest("button") || event.target);
  if (fromCenter || !btn || typeof btn.getBoundingClientRect !== "function") {
    x = viewportWidth / 2;
    y = viewportHeight / 2;
  } else {
    const rect = btn.getBoundingClientRect();
    x = rect.left + rect.width / 2;
    y = rect.top + rect.height / 2;
  }

  const maxRadius = Math.hypot(
    Math.max(x, viewportWidth - x),
    Math.max(y, viewportHeight - y)
  );

  const applyTheme = () => {
    const isDark = root.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    const darkModeToggle = document.getElementById("darkModeToggle");
    if (darkModeToggle) darkModeToggle.checked = isDark;
  };

  // Fallback for browsers without View Transitions API
  if (typeof document.startViewTransition !== "function") {
    applyTheme();
    return;
  }

  const clipPath = getThemeTransitionClipPaths(shape, x, y, maxRadius, viewportWidth, viewportHeight);

  root.dataset.magicuiThemeVt = "active";
  root.style.setProperty("--magicui-theme-toggle-vt-duration", `${duration}ms`);
  root.style.setProperty("--magicui-theme-vt-clip-from", clipPath[0]);

  const cleanup = () => {
    isThemeTransitioning = false;
    delete root.dataset.magicuiThemeVt;
    root.style.removeProperty("--magicui-theme-toggle-vt-duration");
    root.style.removeProperty("--magicui-theme-vt-clip-from");
    if (activeThemeAnimation) {
      activeThemeAnimation.cancel();
      activeThemeAnimation = null;
    }
  };

  isThemeTransitioning = true;
  const transition = document.startViewTransition(() => {
    applyTheme();
  });

  if (transition && typeof transition.finished?.finally === "function") {
    transition.finished.finally(cleanup).catch(() => {});
  } else {
    cleanup();
  }

  if (transition?.ready && typeof transition.ready.then === "function") {
    transition.ready
      .then(() => {
        activeThemeAnimation = document.documentElement.animate(
          { clipPath },
          {
            duration,
            easing: shape === "star" ? "linear" : "ease-in-out",
            fill: "forwards",
            pseudoElement: "::view-transition-new(root)",
          }
        );
      })
      .catch(() => {});
  }
};

// Initialize Theme on load
function initDarkMode() {
  const html = document.documentElement;
  const savedTheme = localStorage.getItem("theme");
  const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const isDark = savedTheme === "dark" || (!savedTheme && systemPrefersDark);
  if (isDark) {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }

  const darkModeToggle = document.getElementById("darkModeToggle");
  if (darkModeToggle) {
    darkModeToggle.checked = isDark;
    darkModeToggle.addEventListener("change", function (e) {
      window.toggleAnimatedTheme(e);
    });
  }
}

// Toast Notification System
function showToast(message, type = "success", duration = 4000) {
  const toast = document.createElement("div");
  toast.className = `toast ${type === "error" ? "border-red-500" : type === "warning" ? "border-yellow-500" : "border-green-500"}`;

  const icon =
    type === "success"
      ? "fa-check-circle text-green-500"
      : type === "error"
        ? "fa-exclamation-circle text-red-500"
        : "fa-info-circle text-yellow-500";

  toast.innerHTML = `
    <div class="flex-shrink-0">
      <i class="fas ${icon} text-xl"></i>
    </div>
    <div class="flex-1">
      <p class="font-medium text-gray-900 dark:text-gray-100">${message}</p>
    </div>
    <button onclick="this.parentElement.remove()" 
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 focus-outline rounded">
      <i class="fas fa-times"></i>
    </button>
  `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(400px)";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Handle Login/Logout Messages
function handleAuthMessages() {
  if (localStorage.getItem("justLoggedIn") === "true") {
    setTimeout(() => {
      showToast("Welcome back! You have logged in successfully.", "success");
    }, 100);
    localStorage.removeItem("justLoggedIn");
  }

  if (localStorage.getItem("justLoggedOut") === "true") {
    setTimeout(() => {
      showToast("You have been logged out successfully.", "success");
    }, 100);
    localStorage.removeItem("justLoggedOut");
  }
}

// Mobile Menu Toggle
function toggleMobileMenu() {
  const mobileMenu = document.getElementById("mobileMenu");
  const overlay = document.getElementById("menuOverlay");

  if (mobileMenu && overlay) {
    mobileMenu.classList.toggle("-translate-x-full");
    overlay.classList.toggle("hidden");
  }
}

// Profile Dropdown Toggle
function toggleProfileDropdown() {
  const dropdown = document.getElementById("profileDropdown");
  if (dropdown) {
    dropdown.classList.toggle("hidden");
  }
}

// Close dropdown when clicking outside
document.addEventListener("click", function (event) {
  const profileButton = document.getElementById("profileButton");
  const dropdown = document.getElementById("profileDropdown");

  if (
    dropdown &&
    profileButton &&
    !profileButton.contains(event.target) &&
    !dropdown.contains(event.target)
  ) {
    dropdown.classList.add("hidden");
  }
});

// Form Validation with Inline Feedback
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  const inputs = form.querySelectorAll(
    "input[required], select[required], textarea[required]",
  );

  inputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateField(this);
    });

    input.addEventListener("input", function () {
      if (this.classList.contains("input-error")) {
        validateField(this);
      }
    });
  });

  form.addEventListener("submit", function (e) {
    let isValid = true;
    inputs.forEach((input) => {
      if (!validateField(input)) {
        isValid = false;
      }
    });

    if (!isValid) {
      e.preventDefault();
      showToast("Please fix the errors before submitting.", "error");
    }
  });
}

function validateField(field) {
  const errorDiv = field.nextElementSibling;

  if (!field.validity.valid) {
    field.classList.add("input-error");
    if (errorDiv && errorDiv.classList.contains("error-message")) {
      errorDiv.classList.remove("hidden");
    }
    return false;
  } else {
    field.classList.remove("input-error");
    if (errorDiv && errorDiv.classList.contains("error-message")) {
      errorDiv.classList.add("hidden");
    }
    return true;
  }
}

// Loading State for Buttons
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = `
      <span class="spinner mr-2"></span>
      <span>Processing...</span>
    `;
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || button.innerHTML;
  }
}

// Smooth Scroll to Element
function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// Scroll Reveal Animations
function initScrollReveal() {
  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  if (prefersReduced) return;

  const elements = document.querySelectorAll(
    "[data-animate], .card, .scheme-card, .scheme-item, .feature-card, .stat-card, .timeline-item, .form-card, .panel, table, .list-card",
  );

  if (!elements.length) return;

  elements.forEach((el, index) => {
    if (el.dataset.animateInitialized) return;
    el.dataset.animateInitialized = "true";
    el.classList.add("reveal");
    el.style.setProperty("--reveal-delay", `${Math.min(index * 60, 360)}ms`);
  });

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal-active");
          obs.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.12,
      rootMargin: "0px 0px -10% 0px",
    },
  );

  elements.forEach((el) => observer.observe(el));
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  initDarkMode();
  handleAuthMessages();
  initScrollReveal();

  // Add page transition effect
  document.body.classList.add("page-transition");

  // Initialize tooltips
  const tooltips = document.querySelectorAll("[data-tooltip]");
  tooltips.forEach((el) => {
    el.addEventListener("mouseenter", function () {
      const tooltip = this.getAttribute("data-tooltip");
      showTooltip(this, tooltip);
    });
  });
});

// Tooltip System
function showTooltip(element, text) {
  const tooltip = document.createElement("div");
  tooltip.className =
    "absolute z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg -top-10 left-1/2 transform -translate-x-1/2 whitespace-nowrap";
  tooltip.textContent = text;

  element.style.position = "relative";
  element.appendChild(tooltip);

  element.addEventListener(
    "mouseleave",
    function () {
      tooltip.remove();
    },
    { once: true },
  );
}

// Skeleton Screen Loader
function showSkeletonLoader(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = `
    <div class="space-y-4 animate-pulse">
      <div class="skeleton h-8 w-3/4"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-5/6"></div>
      <div class="skeleton h-4 w-4/6"></div>
    </div>
  `;
}

// Image Lazy Loading with Placeholder
function lazyLoadImages() {
  const images = document.querySelectorAll("img[data-src]");

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.remove("skeleton");
        observer.unobserve(img);
      }
    });
  });

  images.forEach((img) => imageObserver.observe(img));
}

// Copy to Clipboard with Feedback
function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> Copied!';
    button.classList.add("bg-green-500");

    setTimeout(() => {
      button.innerHTML = originalHTML;
      button.classList.remove("bg-green-500");
    }, 2000);
  });
}
