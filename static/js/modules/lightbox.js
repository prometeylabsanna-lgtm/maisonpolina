export function initLightbox() {
  const root = document.querySelector("[data-lightbox-root]");
  const box = document.querySelector("[data-lightbox]");
  if (!root || !box) return;

  const img = box.querySelector("[data-lightbox-img]");
  const buttons = [...root.querySelectorAll("[data-lightbox-open]")];
  let index = 0;
  let lastFocus = null;
  let touchX = null;

  const show = (i) => {
    index = (i + buttons.length) % buttons.length;
    const btn = buttons[index];
    img.src = btn.dataset.full || "";
    img.alt = btn.dataset.alt || "";
    const next = buttons[(index + 1) % buttons.length];
    if (next?.dataset.full) {
      const preload = new Image();
      preload.src = next.dataset.full;
    }
  };

  const open = (i) => {
    lastFocus = document.activeElement;
    show(i);
    box.hidden = false;
    box.classList.add("is-open");
    document.addEventListener("keydown", onKey);
  };

  const close = () => {
    box.classList.remove("is-open");
    box.hidden = true;
    img.src = "";
    document.removeEventListener("keydown", onKey);
    if (lastFocus) lastFocus.focus();
  };

  const onKey = (e) => {
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") show(index + 1);
    if (e.key === "ArrowLeft") show(index - 1);
  };

  buttons.forEach((btn, i) => btn.addEventListener("click", () => open(i)));
  box.querySelector("[data-lightbox-close]")?.addEventListener("click", close);
  box.querySelector("[data-lightbox-prev]")?.addEventListener("click", () => show(index - 1));
  box.querySelector("[data-lightbox-next]")?.addEventListener("click", () => show(index + 1));
  box.addEventListener("click", (e) => {
    if (e.target === box) close();
  });

  box.addEventListener(
    "touchstart",
    (e) => {
      touchX = e.changedTouches[0].clientX;
    },
    { passive: true }
  );
  box.addEventListener(
    "touchend",
    (e) => {
      if (touchX == null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
      touchX = null;
    },
    { passive: true }
  );
}
