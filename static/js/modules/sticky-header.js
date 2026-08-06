export function initStickyHeader() {
  const header = document.querySelector("[data-sticky-header]");
  const sentinel = document.getElementById("scroll-sentinel");
  if (!header || !sentinel) return;

  const observer = new IntersectionObserver(
    ([entry]) => {
      header.classList.toggle("is-scrolled", !entry.isIntersecting);
    },
    { threshold: [0, 1] }
  );
  observer.observe(sentinel);
}
