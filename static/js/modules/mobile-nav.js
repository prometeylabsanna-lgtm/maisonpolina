import { lockScroll, unlockScroll } from "./scroll-lock.js";
import { registerEscape, unregisterEscape } from "./escape-stack.js";

export function initMobileNav() {
  const nav = document.querySelector("[data-mobile-nav]");
  const openBtn = document.querySelector("[data-mobile-nav-open]");
  const closeBtn = document.querySelector("[data-mobile-nav-close]");
  if (!nav || !openBtn) return;

  let lastFocus = null;
  let isOpen = false;

  const focusable = () =>
    nav.querySelectorAll(
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
    if (isOpen) return;
    lastFocus = document.activeElement;
    lockScroll();
    nav.hidden = false;
    nav.classList.add("is-open");
    openBtn.setAttribute("aria-expanded", "true");
    isOpen = true;
    registerEscape("mobile-nav", close);
    nav.addEventListener("keydown", trap);
    const items = focusable();
    if (items[0]) items[0].focus();
  };

  const close = () => {
    if (!isOpen) return;
    nav.classList.remove("is-open");
    nav.hidden = true;
    openBtn.setAttribute("aria-expanded", "false");
    unlockScroll();
    unregisterEscape("mobile-nav");
    isOpen = false;
    nav.removeEventListener("keydown", trap);
    if (lastFocus) lastFocus.focus();
  };

  openBtn.addEventListener("click", open);
  if (closeBtn) closeBtn.addEventListener("click", close);
  nav.querySelectorAll("[data-mobile-nav-link]").forEach((el) => {
    el.addEventListener("click", () => {
      if (el.matches("[data-open-lead]")) {
        // Lead modal opens first (lock), then mobile unlocks once — modal lock remains.
        setTimeout(close, 0);
      } else {
        close();
      }
    });
  });
}
