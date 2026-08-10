export function initReveal() {
  const nodes = document.querySelectorAll("[data-reveal]");
  if (!nodes.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  let wave = 0;
  let waveTimer = 0;

  const reveal = (el) => {
    const custom = el.getAttribute("data-reveal-delay");
    let delayMs = custom ? Number.parseInt(custom, 10) : NaN;

    if (Number.isNaN(delayMs)) {
      delayMs = wave * 140;
      wave += 1;
      window.clearTimeout(waveTimer);
      waveTimer = window.setTimeout(() => {
        wave = 0;
      }, 420);
    }

    el.style.setProperty("--reveal-delay", `${delayMs}ms`);
    // Next frame so delay applies before visibility toggle
    window.requestAnimationFrame(() => {
      el.classList.add("is-visible");
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        reveal(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.06, rootMargin: "0px 0px -6% 0px" }
  );

  nodes.forEach((el) => observer.observe(el));
}
