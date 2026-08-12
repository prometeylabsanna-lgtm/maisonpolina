let locks = 0;
let scrollY = 0;

export function lockScroll() {
  if (locks === 0) {
    scrollY = window.scrollY;
    document.documentElement.style.setProperty("--scroll-lock-top", `-${scrollY}px`);
    document.body.classList.add("is-locked");
  }
  locks += 1;
}

export function unlockScroll() {
  if (locks <= 0) {
    locks = 0;
    return;
  }
  locks -= 1;
  if (locks > 0) return;
  document.body.classList.remove("is-locked");
  document.documentElement.style.removeProperty("--scroll-lock-top");
  window.scrollTo(0, scrollY);
}
