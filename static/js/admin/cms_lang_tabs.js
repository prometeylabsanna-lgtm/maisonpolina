(() => {
  const STORAGE_KEY = "cms-admin-lang";
  const TAB_SELECTOR = ".cms-lang-tab[data-cms-lang]";

  const getLang = () => {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    return saved === "en" ? "en" : "ru";
  };

  const applyLang = (lang) => {
    const next = lang === "en" ? "en" : "ru";
    // Needed for CSS: html[data-cms-lang="en"] .cms-lang-pane--*
    document.documentElement.dataset.cmsLang = next;
    window.localStorage.setItem(STORAGE_KEY, next);
    // Only tab buttons — never <html>, which also gets data-cms-lang
    document.querySelectorAll(TAB_SELECTOR).forEach((btn) => {
      const active = btn.getAttribute("data-cms-lang") === next;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-selected", active ? "true" : "false");
    });
    window.dispatchEvent(
      new CustomEvent("cms-lang-changed", { detail: { lang: next } })
    );
    window.setTimeout(() => window.cmsResizeTinyMCE && window.cmsResizeTinyMCE(), 40);
  };

  const resizeTiny = () => {
    if (!window.tinymce) return;
    window.tinymce.editors.forEach((editor) => {
      try {
        editor.fire("ResizeEditor");
        if (typeof editor.execCommand === "function") {
          editor.execCommand("mceAutoResize");
        }
      } catch (_err) {
        /* ignore */
      }
    });
  };

  window.cmsResizeTinyMCE = resizeTiny;

  const boot = () => {
    applyLang(getLang());
    document.querySelectorAll(TAB_SELECTOR).forEach((btn) => {
      btn.addEventListener("click", (event) => {
        event.preventDefault();
        applyLang(btn.getAttribute("data-cms-lang"));
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  document.addEventListener("alpine:init", () => {
    const Alpine = window.Alpine;
    if (!Alpine || Alpine.store("cmsLang")) return;
    Alpine.store("cmsLang", {
      current: getLang(),
      set(lang) {
        applyLang(lang);
        this.current = getLang();
      },
    });
  });
})();
