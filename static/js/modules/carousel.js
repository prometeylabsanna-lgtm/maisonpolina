export function initCarousel() {
  const root = document.querySelector("[data-carousel]");
  if (!root) return;
  const track = root.querySelector("[data-carousel-track]");
  const slides = [...root.querySelectorAll(".carousel__slide")];
  const dotsWrap = document.querySelector("[data-carousel-dots]");
  const dots = dotsWrap ? [...dotsWrap.querySelectorAll("[data-carousel-dot]")] : [];
  if (!track || !slides.length) return;

  let index = 0;
  let timer = null;
  let touchX = null;

  const perView = () =>
    window.matchMedia("(min-width: 768px)").matches && slides.length >= 3 ? 3 : 1;

  const go = (i) => {
    const n = slides.length;
    index = ((i % n) + n) % n;
    const view = perView();

    if (view === 1) {
      track.style.transform = `translate3d(-${index * 100}%, 0, 0)`;
      track.style.minHeight = "";
      slides.forEach((slide, di) => {
        slide.classList.toggle("is-center", di === index);
        slide.classList.toggle("is-side", false);
        slide.style.transform = "";
        slide.style.opacity = "";
        slide.style.pointerEvents = "";
        slide.setAttribute("aria-hidden", di === index ? "false" : "true");
      });
    } else {
      /* три в ряд: активний по центру, сусіди з боків */
      track.style.transform = "";
      slides.forEach((slide, di) => {
        let d = di - index;
        if (d > n / 2) d -= n;
        if (d < -n / 2) d += n;
        const visible = Math.abs(d) <= 1;
        slide.classList.toggle("is-center", d === 0);
        slide.classList.toggle("is-side", visible && d !== 0);
        slide.style.transform = visible ? `translate3d(${d * 100}%, 0, 0)` : "translate3d(0,0,0)";
        slide.style.opacity = visible ? "" : "0";
        slide.style.pointerEvents = visible ? "" : "none";
        slide.setAttribute("aria-hidden", d === 0 ? "false" : "true");
      });
      const center = slides[index];
      if (center) {
        track.style.minHeight = `${center.offsetHeight}px`;
      }
    }

    dots.forEach((dot, di) => dot.classList.toggle("is-active", di === index));
    root.dataset.perView = String(view);
  };

  const start = () => {
    stop();
    if (slides.length < 2) return;
    timer = window.setInterval(() => go(index + 1), 7000);
  };

  const stop = () => {
    if (timer) window.clearInterval(timer);
    timer = null;
  };

  root.querySelector("[data-carousel-prev]")?.addEventListener("click", () => {
    go(index - 1);
    start();
  });
  root.querySelector("[data-carousel-next]")?.addEventListener("click", () => {
    go(index + 1);
    start();
  });
  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      go(Number(dot.dataset.carouselDot) || 0);
      start();
    });
  });

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", start);
  root.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      go(index + 1);
      start();
    }
    if (e.key === "ArrowLeft") {
      go(index - 1);
      start();
    }
  });

  root.addEventListener(
    "touchstart",
    (e) => {
      touchX = e.changedTouches[0].clientX;
      stop();
    },
    { passive: true }
  );
  root.addEventListener(
    "touchend",
    (e) => {
      if (touchX == null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1));
      touchX = null;
      start();
    },
    { passive: true }
  );

  window.addEventListener("resize", () => go(index));

  go(0);
  start();
}
