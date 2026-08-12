export function initGalleryScroll() {
  document.querySelectorAll("[data-gallery]").forEach((root) => {
    const track = root.querySelector("[data-gallery-track]");
    if (!track) return;

    const prev = root.querySelector("[data-gallery-prev]");
    const next = root.querySelector("[data-gallery-next]");
    const cards = [...track.querySelectorAll(".gallery__item")];
    if (!cards.length) return;

    let index = 0;
    let byArrow = false;
    let settleTimer = null;
    let offsets = [];
    let max = 0;

    const rebuildMetrics = () => {
      const base = cards[0].offsetLeft;
      offsets = cards.map((card) => card.offsetLeft - base);
      max = track.scrollWidth - track.clientWidth;
    };

    const offsetOf = (i) => offsets[i] ?? 0;

    const nearestIndex = () =>
      cards.reduce(
        (best, _card, i) =>
          Math.abs(offsetOf(i) - track.scrollLeft) < Math.abs(offsetOf(best) - track.scrollLeft)
            ? i
            : best,
        0
      );

    const sync = () => {
      root.classList.toggle("is-static", max <= 1);
      if (prev) prev.disabled = track.scrollLeft <= 1;
      if (next) next.disabled = track.scrollLeft >= max - 1;
    };

    const targetLeft = () => Math.min(offsetOf(index), max);

    const go = (dir) => {
      index = Math.min(Math.max(index + dir, 0), cards.length - 1);
      byArrow = true;
      track.scrollTo({ left: targetLeft(), behavior: "smooth" });
    };

    const onScroll = () => {
      sync();
      window.clearTimeout(settleTimer);
      settleTimer = window.setTimeout(() => {
        if (!byArrow) {
          index = nearestIndex();
          return;
        }
        if (Math.abs(track.scrollLeft - targetLeft()) > 2) {
          track.scrollTo({ left: targetLeft(), behavior: "smooth" });
          return;
        }
        byArrow = false;
      }, 160);
    };

    prev?.addEventListener("click", () => go(-1));
    next?.addEventListener("click", () => go(1));
    track.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", () => {
      rebuildMetrics();
      index = nearestIndex();
      sync();
    });

    track.querySelectorAll("img").forEach((img) => {
      if (!img.complete) {
        img.addEventListener(
          "load",
          () => {
            rebuildMetrics();
            sync();
          },
          { once: true }
        );
      }
    });

    rebuildMetrics();
    sync();
  });
}
