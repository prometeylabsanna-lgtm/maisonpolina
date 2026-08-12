import { lockScroll, unlockScroll } from "./scroll-lock.js";
import { registerEscape, unregisterEscape } from "./escape-stack.js";

export function initModal() {
  const modals = [...document.querySelectorAll("[data-modal]")];
  if (!modals.length) return;

  let activeModal = null;
  let lastFocus = null;

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
    if (activeModal === modal) return;
    if (activeModal && activeModal !== modal) close();
    lastFocus = document.activeElement;
    lockScroll();
    modal.hidden = false;
    modal.classList.add("is-open");
    activeModal = modal;
    registerEscape("modal", close);
    modal.addEventListener("keydown", trap);
    const items = focusable(modal);
    if (items[0]) items[0].focus();
  };

  const close = () => {
    if (!activeModal) return;
    const modal = activeModal;
    modal.classList.remove("is-open");
    modal.hidden = true;
    unlockScroll();
    unregisterEscape("modal");
    modal.removeEventListener("keydown", trap);
    activeModal = null;
    if (lastFocus) lastFocus.focus();
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
      const hint = leadModal.querySelector(".form__hint");
      const hintLabel = leadModal.querySelector("[data-lead-service-label]");
      if (hintLabel) hintLabel.textContent = service;
      if (hint) hint.hidden = !service;
      if (activeModal === leadModal) return;
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
      if (id === "lead-form-body" || id === "contacts-form") {
        document.dispatchEvent(new CustomEvent("lead-form:ready", { detail: { root: e.target } }));
      }
      if (id === "review-form-body") {
        document.dispatchEvent(new CustomEvent("review-form:ready"));
      }
    }
  });
}
