(() => {
  const storageKey = "afriq-theme";
  const root = document.documentElement;

  const prefersDark = () => {
    try {
      return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    } catch {
      return false;
    }
  };

  const getActiveTheme = () => {
    const explicit = root.getAttribute("data-theme");
    if (explicit === "dark" || explicit === "light") return explicit;
    return prefersDark() ? "dark" : "light";
  };

  const setTheme = (theme, persist) => {
    if (theme === "dark" || theme === "light") {
      root.setAttribute("data-theme", theme);
      if (persist) localStorage.setItem(storageKey, theme);
    } else {
      root.removeAttribute("data-theme");
      if (persist) localStorage.removeItem(storageKey);
    }
  };

  const createToggle = () => {
    if (document.querySelector(".afriq-theme-toggle")) return;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "afriq-theme-toggle";
    btn.setAttribute("aria-label", "Toggle theme");

    const label = document.createElement("span");
    label.className = "afriq-theme-toggle__label";
    btn.appendChild(label);

    const sync = () => {
      const theme = getActiveTheme();
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      label.textContent = theme === "dark" ? "NIGHT" : "DAY";
    };

    btn.addEventListener("click", () => {
      const next = getActiveTheme() === "dark" ? "light" : "dark";
      setTheme(next, true);
      sync();
    });

    const mount =
      document.querySelector(".banner-video .elementor-container") ||
      document.querySelector(".banner-video") ||
      document.querySelector(".afriq-header__row") ||
      document.body;
    mount.appendChild(btn);
    sync();

    try {
      const mq = window.matchMedia("(prefers-color-scheme: dark)");
      mq.addEventListener("change", () => {
        const saved = localStorage.getItem(storageKey);
        if (saved !== "dark" && saved !== "light") sync();
      });
    } catch {}
  };

  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === "dark" || saved === "light") setTheme(saved, false);
  } catch {}

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", createToggle);
  } else {
    createToggle();
  }
})();
