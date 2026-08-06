export function initMobileNav() {
  const nav = document.querySelector("[data-mobile-nav]");
  const openBtn = document.querySelector("[data-mobile-nav-open]");
  const closeBtn = document.querySelector("[data-mobile-nav-close]");
  if (!nav || !openBtn) return;

  let scrollY = 0;
  let lastFocus = null;

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
    lastFocus = document.activeElement;
    scrollY = window.scrollY;
    document.documentElement.style.setProperty("--scroll-lock-top", `-${scrollY}px`);
    document.body.classList.add("is-locked");
    nav.hidden = false;
    nav.classList.add("is-open");
    openBtn.setAttribute("aria-expanded", "true");
    document.addEventListener("keydown", onKey);
    nav.addEventListener("keydown", trap);
    const items = focusable();
    if (items[0]) items[0].focus();
  };

  const close = () => {
    nav.classList.remove("is-open");
    nav.hidden = true;
    openBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("is-locked");
    document.documentElement.style.removeProperty("--scroll-lock-top");
    window.scrollTo(0, scrollY);
    document.removeEventListener("keydown", onKey);
    nav.removeEventListener("keydown", trap);
    if (lastFocus) lastFocus.focus();
  };

  const onKey = (e) => {
    if (e.key === "Escape") close();
  };

  openBtn.addEventListener("click", open);
  if (closeBtn) closeBtn.addEventListener("click", close);
  nav.querySelectorAll("[data-mobile-nav-link]").forEach((el) => {
    el.addEventListener("click", () => {
      if (el.matches("[data-open-lead]")) {
        // close after lead modal opens
        setTimeout(close, 0);
      } else {
        close();
      }
    });
  });
}
