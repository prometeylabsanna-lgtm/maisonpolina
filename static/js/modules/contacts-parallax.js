export function initContactsParallax() {
  const section = document.querySelector("#contact.contacts");
  const img = section?.querySelector(".contacts__bg-img");
  if (!section || !img) return;

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduce.matches) return;

  let ticking = false;
  const maxShift = 48; // px — м’який зсув

  const update = () => {
    ticking = false;
    const rect = section.getBoundingClientRect();
    const view = window.innerHeight || 1;
    // 0 — секція ще під екраном, 1 — уже вийшла вгору
    const progress = 1 - (rect.bottom / (view + rect.height));
    const clamped = Math.min(1, Math.max(0, progress));
    const y = (clamped - 0.5) * 2 * maxShift;
    img.style.transform = `translate3d(0, ${y.toFixed(2)}px, 0) scale(1.08)`;
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(update);
  };

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
}
