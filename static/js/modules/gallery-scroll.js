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

    // .gallery має position: relative, тож offsetLeft уже рахується від треку
    const offsetOf = (card) => card.offsetLeft - cards[0].offsetLeft;
    const maxScroll = () => track.scrollWidth - track.clientWidth;

    const nearestIndex = () =>
      cards.reduce(
        (best, card, i) =>
          Math.abs(offsetOf(card) - track.scrollLeft) <
          Math.abs(offsetOf(cards[best]) - track.scrollLeft)
            ? i
            : best,
        0
      );

    const sync = () => {
      const max = maxScroll();
      root.classList.toggle("is-static", max <= 1);
      if (prev) prev.disabled = track.scrollLeft <= 1;
      if (next) next.disabled = track.scrollLeft >= max - 1;
    };

    const targetLeft = () => Math.min(offsetOf(cards[index]), maxScroll());

    // власний індекс, а не поточний scrollLeft: інакше швидкі кліки
    // під час плавної анімації дають крок на місці
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
        // серія кліків перериває плавну анімацію — доводимо трек до цілі
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
      index = nearestIndex();
      sync();
    });

    // після довантаження лінивих фото ширина треку змінюється
    track.querySelectorAll("img").forEach((img) => {
      if (!img.complete) img.addEventListener("load", sync, { once: true });
    });

    sync();
  });
}
