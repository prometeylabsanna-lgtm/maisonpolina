export function initReviewClamp() {
  const texts = [...document.querySelectorAll("[data-review-text]")];
  if (!texts.length) return;

  const apply = (el) => {
    const btn = el.parentElement?.querySelector("[data-review-more]");
    if (!btn) return;
    el.classList.remove("is-clamped", "is-expanded");
    btn.hidden = true;
    const natural = el.scrollHeight;
    el.classList.add("is-clamped");
    const overflowing = el.scrollHeight + 1 < natural;
    if (!overflowing) {
      el.classList.remove("is-clamped");
      return;
    }
    btn.hidden = false;
    btn.textContent = btn.dataset.labelMore || btn.textContent;
    btn.setAttribute("aria-expanded", "false");
  };

  texts.forEach((el) => apply(el));

  document.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-review-more]");
    if (!btn) return;
    const wrap = btn.closest(".carousel__text-wrap");
    const el = wrap?.querySelector("[data-review-text]");
    if (!el) return;
    const expanded = el.classList.toggle("is-expanded");
    el.classList.toggle("is-clamped", !expanded);
    btn.setAttribute("aria-expanded", expanded ? "true" : "false");
    btn.textContent = expanded
      ? btn.dataset.labelLess || btn.textContent
      : btn.dataset.labelMore || btn.textContent;
    el.dispatchEvent(new CustomEvent("review-clamp-change", { bubbles: true }));
  });
}
