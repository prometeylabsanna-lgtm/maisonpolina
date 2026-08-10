import { initStickyHeader } from "./modules/sticky-header.js";
import { initMobileNav } from "./modules/mobile-nav.js";
import { initScrollspy } from "./modules/scrollspy.js";
import { initLightbox } from "./modules/lightbox.js";
import { initCarousel } from "./modules/carousel.js";
import { initGalleryScroll } from "./modules/gallery-scroll.js";
import { initAccordion } from "./modules/accordion.js";
import { initModal } from "./modules/modal.js";
import { initReveal } from "./modules/reveal.js";
import { initLeadForm } from "./modules/lead-form.js";
import { initReviewForm } from "./modules/review-form.js";
import { initContactsParallax } from "./modules/contacts-parallax.js";
import { initChatWidget } from "./modules/chat-widget.js";

document.addEventListener("DOMContentLoaded", () => {
  initStickyHeader();
  initMobileNav();
  initScrollspy();
  initLightbox();
  initCarousel();
  initGalleryScroll();
  initAccordion();
  initModal();
  initReveal();
  initLeadForm();
  initReviewForm();
  initContactsParallax();
  initChatWidget();
});
