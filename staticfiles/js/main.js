// Dark Mode Toggle with System Preference
function initDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const html = document.documentElement;

  // Check for saved theme preference or default to system preference
  const savedTheme = localStorage.getItem("theme");
  const systemPrefersDark = window.matchMedia(
    "(prefers-color-scheme: dark)",
  ).matches;

  if (savedTheme === "dark" || (!savedTheme && systemPrefersDark)) {
    html.classList.add("dark");
    if (darkModeToggle) darkModeToggle.checked = true;
  }

  // Toggle dark mode
  if (darkModeToggle) {
    darkModeToggle.addEventListener("change", function () {
      if (this.checked) {
        html.classList.add("dark");
        localStorage.setItem("theme", "dark");
      } else {
        html.classList.remove("dark");
        localStorage.setItem("theme", "light");
      }
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
