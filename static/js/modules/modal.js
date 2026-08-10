export function initModal() {
  const modals = [...document.querySelectorAll("[data-modal]")];
  if (!modals.length) return;

  let activeModal = null;
  let lastFocus = null;
  let scrollY = 0;

  const focusable = (modal) =>
    modal.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

  const trap = (e) => {
    if (!activeModal || e.key !== "Tab") return;
    const items = [...focusable(activeModal)];
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

  const open = (modal) => {
    if (activeModal && activeModal !== modal) close();
    lastFocus = document.activeElement;
    scrollY = window.scrollY;
    document.documentElement.style.setProperty("--scroll-lock-top", `-${scrollY}px`);
    document.body.classList.add("is-locked");
    modal.hidden = false;
    modal.classList.add("is-open");
    activeModal = modal;
    document.addEventListener("keydown", onKey);
    modal.addEventListener("keydown", trap);
    const items = focusable(modal);
    if (items[0]) items[0].focus();
  };

  const close = () => {
    if (!activeModal) return;
    const modal = activeModal;
    modal.classList.remove("is-open");
    modal.hidden = true;
    document.body.classList.remove("is-locked");
    document.documentElement.style.removeProperty("--scroll-lock-top");
    window.scrollTo(0, scrollY);
    document.removeEventListener("keydown", onKey);
    modal.removeEventListener("keydown", trap);
    activeModal = null;
    if (lastFocus) lastFocus.focus();
  };

  const onKey = (e) => {
    if (e.key === "Escape") close();
  };

  const leadModal = document.querySelector("#lead-modal");
  const reviewModal = document.querySelector("#review-modal");

  document.querySelectorAll("[data-open-lead]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!leadModal) return;
      const service = btn.dataset.service || "";
      const source = btn.dataset.source || "contacts";
      leadModal.querySelectorAll("[data-lead-service]").forEach((el) => {
        el.value = service;
      });
      leadModal.querySelectorAll("[data-lead-source]").forEach((el) => {
        el.value = source;
      });
      const hint = leadModal.querySelector(".form__hint strong");
      if (hint) hint.textContent = service || hint.textContent;
      open(leadModal);
    });
  });

  document.querySelectorAll("[data-open-review]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!reviewModal) return;
      open(reviewModal);
    });
  });

  modals.forEach((modal) => {
    modal.querySelectorAll("[data-close-modal]").forEach((btn) => {
      btn.addEventListener("click", close);
    });
    modal.addEventListener("click", (e) => {
      if (e.target === modal) close();
    });
    modal.querySelector("[data-modal-dialog]")?.addEventListener("click", (e) => {
      e.stopPropagation();
    });
  });

  document.body.addEventListener("click", (e) => {
    const t = e.target.closest("[data-close-modal]");
    if (!t || !activeModal || !activeModal.contains(t)) return;
    close();
  });

  document.body.addEventListener("htmx:afterSwap", (e) => {
    const id = e.target?.id;
    if (id === "lead-form-body" || id === "review-form-body" || id === "contacts-form") {
      const closeBtn = e.target.querySelector("[data-close-modal]");
      closeBtn?.addEventListener("click", close);
      if (id === "review-form-body") {
        document.dispatchEvent(new CustomEvent("review-form:ready"));
      }
    }
  });
}
