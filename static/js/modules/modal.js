export function initModal() {
  const modal = document.querySelector("[data-modal]");
  if (!modal) return;
  const dialog = modal.querySelector("[data-modal-dialog]");
  let lastFocus = null;
  let scrollY = 0;

  const focusable = () =>
    modal.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

  const trap = (e) => {
    if (e.key !== "Tab") return;
    const items = [...focusable()];
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  const open = () => {
    lastFocus = document.activeElement;
    scrollY = window.scrollY;
    document.documentElement.style.setProperty("--scroll-lock-top", `-${scrollY}px`);
    document.body.classList.add("is-locked");
    modal.hidden = false;
    modal.classList.add("is-open");
    document.addEventListener("keydown", onKey);
    modal.addEventListener("keydown", trap);
    const items = focusable();
    if (items[0]) items[0].focus();
  };

  const close = () => {
    modal.classList.remove("is-open");
    modal.hidden = true;
    document.body.classList.remove("is-locked");
    document.documentElement.style.removeProperty("--scroll-lock-top");
    window.scrollTo(0, scrollY);
    document.removeEventListener("keydown", onKey);
    modal.removeEventListener("keydown", trap);
    if (lastFocus) lastFocus.focus();
  };

  const onKey = (e) => {
    if (e.key === "Escape") close();
  };

  document.querySelectorAll("[data-open-lead]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const service = btn.dataset.service || "";
      const source = btn.dataset.source || "contacts";
      document.querySelectorAll("[data-lead-service]").forEach((el) => {
        el.value = service;
      });
      document.querySelectorAll("[data-lead-source]").forEach((el) => {
        el.value = source;
      });
      const hint = modal.querySelector(".form__hint strong");
      if (hint) hint.textContent = service || hint.textContent;
      open();
    });
  });

  modal.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", close);
  });
  modal.addEventListener("click", (e) => {
    if (e.target === modal) close();
  });
  dialog?.addEventListener("click", (e) => e.stopPropagation());

  document.body.addEventListener("click", (e) => {
    const t = e.target.closest("[data-close-modal]");
    if (t && modal.contains(t)) close();
  });

  document.body.addEventListener("htmx:afterSwap", (e) => {
    if (e.target?.id === "lead-form-body") {
      const closeBtn = e.target.querySelector("[data-close-modal]");
      closeBtn?.addEventListener("click", close);
    }
  });
}
