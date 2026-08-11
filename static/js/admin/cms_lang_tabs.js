(() => {
  const resizeTiny = () => {
    if (!window.tinymce) return;
    window.tinymce.editors.forEach((editor) => {
      try {
        editor.fire("ResizeEditor");
        if (typeof editor.execCommand === "function") {
          editor.execCommand("mceAutoResize");
        }
      } catch (_err) {
        /* ignore editors not ready */
      }
    });
  };

  window.cmsResizeTinyMCE = resizeTiny;

  document.addEventListener("alpine:init", () => {
    const Alpine = window.Alpine;
    if (!Alpine || Alpine.store("cmsLang")) return;
    Alpine.store("cmsLang", {
      current: "ru",
      set(lang) {
        if (lang !== "ru" && lang !== "en") return;
        this.current = lang;
        window.dispatchEvent(
          new CustomEvent("cms-lang-changed", { detail: { lang } })
        );
        window.setTimeout(resizeTiny, 50);
        window.setTimeout(resizeTiny, 250);
      },
    });
  });
})();
