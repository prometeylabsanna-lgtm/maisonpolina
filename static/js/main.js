import { initStickyHeader } from "./modules/sticky-header.js";
import { initMobileNav } from "./modules/mobile-nav.js";
import { initScrollspy } from "./modules/scrollspy.js";
import { initAccordion } from "./modules/accordion.js";
import { initModal } from "./modules/modal.js";
import { initReveal } from "./modules/reveal.js";
import { initLeadForm } from "./modules/lead-form.js";
import { initReviewForm } from "./modules/review-form.js";

function whenIdle(fn, timeout = 2000) {
  if (typeof window.requestIdleCallback === "function") {
    window.requestIdleCallback(fn, { timeout });
  } else {
    window.setTimeout(fn, 1);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initStickyHeader();
  initMobileNav();
  initScrollspy();
  initAccordion();
  initModal();
  initReveal();
  initLeadForm();
  initReviewForm();

  whenIdle(() => {
    import("./modules/lightbox.js").then((m) => m.initLightbox());
    Promise.all([
      import("./modules/review-clamp.js"),
      import("./modules/carousel.js"),
    ]).then(([clamp, carousel]) => {
      clamp.initReviewClamp();
      carousel.initCarousel();
    });
    import("./modules/gallery-scroll.js").then((m) => m.initGalleryScroll());
    import("./modules/contacts-parallax.js").then((m) => m.initContactsParallax());
  });

  whenIdle(() => {
    import("./modules/chat-widget.js").then((m) => m.initChatWidget());
  }, 3500);
});
