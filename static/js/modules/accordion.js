export function initAccordion() {
  const root = document.querySelector("[data-accordion]");
  if (!root) return;
  const items = [...root.querySelectorAll(".accordion__item")];

  items.forEach((item) => {
    const trigger = item.querySelector("[data-accordion-trigger]");
    if (!trigger) return;
    trigger.addEventListener("click", () => {
      const willOpen = !item.classList.contains("is-open");
      items.forEach((other) => {
        other.classList.remove("is-open");
        other
          .querySelector("[data-accordion-trigger]")
          ?.setAttribute("aria-expanded", "false");
      });
      if (willOpen) {
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });
  });
}
