import { initStickyHeader } from "./modules/sticky-header.js";
import { initMobileNav } from "./modules/mobile-nav.js";
import { initScrollspy } from "./modules/scrollspy.js";
import { initAccordion } from "./modules/accordion.js";
import { initModal } from "./modules/modal.js";
import { initReveal } from "./modules/reveal.js";
import { initLeadForm } from "./modules/lead-form.js";
import { initReviewForm } from "./modules/review-form.js";
import { initFormValidation } from "./modules/form-validation.js";

function whenIdle(fn, timeout = 2000) {
  if (typeof window.requestIdleCallback === "function") {
    window.requestIdleCallback(fn, { timeout });
  } else {
    window.setTimeout(fn, 1);
  }
}

function loadModule(path, init) {
  return import(path)
    .then((m) => init(m))
    .catch((err) => {
      console.warn(`[main] failed to load ${path}`, err);
    });
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
  initFormValidation();

  whenIdle(() => {
    loadModule("./modules/lightbox.js", (m) => m.initLightbox());
    Promise.all([
      import("./modules/review-clamp.js"),
      import("./modules/carousel.js"),
    ])
      .then(([clamp, carousel]) => {
        clamp.initReviewClamp();
        carousel.initCarousel();
      })
      .catch((err) => {
        console.warn("[main] failed to load carousel modules", err);
      });
    loadModule("./modules/gallery-scroll.js", (m) => m.initGalleryScroll());
    loadModule("./modules/contacts-parallax.js", (m) => m.initContactsParallax());
  });

  whenIdle(() => {
    loadModule("./modules/chat-widget.js", (m) => m.initChatWidget());
  }, 3500);
});
