(() => {
  const focusableSelector =
    'a[href],button:not([disabled]),textarea:not([disabled]),input:not([disabled]),select:not([disabled]),[tabindex]:not([tabindex="-1"])';

  const getFocusable = (root) => Array.from(root.querySelectorAll(focusableSelector)).filter((el) => el.offsetParent !== null);

  const trapFocus = (container) => {
    const onKeyDown = (e) => {
      if (e.key !== "Tab") return;
      const focusables = getFocusable(container);
      if (focusables.length === 0) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement;

      if (e.shiftKey) {
        if (active === first || active === container) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };

    container.addEventListener("keydown", onKeyDown);
    return () => container.removeEventListener("keydown", onKeyDown);
  };

  const initElementorPopupFocusTrap = () => {
    let cleanup = null;
    let lastFocused = null;

    const applyTrapIfOpen = () => {
      const modal = document.querySelector(".elementor-popup-modal");
      const message = modal?.querySelector(".dialog-message");
      const isOpen = !!(modal && message && getComputedStyle(modal).display !== "none");

      if (!isOpen) {
        if (cleanup) cleanup();
        cleanup = null;
        if (lastFocused && document.contains(lastFocused)) lastFocused.focus();
        lastFocused = null;
        return;
      }

      if (cleanup) return;
      lastFocused = document.activeElement instanceof HTMLElement ? document.activeElement : null;

      message.setAttribute("role", "dialog");
      message.setAttribute("aria-modal", "true");
      message.setAttribute("tabindex", "-1");

      cleanup = trapFocus(message);

      const focusables = getFocusable(message);
      if (focusables[0]) focusables[0].focus();
      else message.focus();
    };

    const mo = new MutationObserver(applyTrapIfOpen);
    mo.observe(document.documentElement, { attributes: true, childList: true, subtree: true });
    applyTrapIfOpen();
  };

  const initMenuAria = () => {
    const toggles = document.querySelectorAll(".hfe-nav-menu__toggle");
    toggles.forEach((toggle) => {
      toggle.setAttribute("role", "button");
      toggle.setAttribute("tabindex", "0");
      if (!toggle.hasAttribute("aria-expanded")) toggle.setAttribute("aria-expanded", "false");

      const sync = () => {
        const expanded = toggle.classList.contains("active") || toggle.classList.contains("hfe-active-menu");
        toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
      };

      toggle.addEventListener("click", sync);
      toggle.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggle.click();
        }
      });

      sync();
    });
  };

  const init = () => {
    initElementorPopupFocusTrap();
    initMenuAria();
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
