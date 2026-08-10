function stamp() {
  return String(Date.now() / 1000);
}

function bindRating(root = document) {
  root.querySelectorAll("[data-rating]").forEach((group) => {
    if (group.dataset.bound === "1") return;
    group.dataset.bound = "1";
    const form = group.closest("form");
    const input = form?.querySelector("[data-rating-input]");
    const stars = [...group.querySelectorAll("[data-rating-value]")];
    let selected = Number(input?.value || 5);

    const paint = (value) => {
      stars.forEach((star) => {
        const n = Number(star.dataset.ratingValue);
        const on = n <= value;
        star.classList.toggle("is-on", on);
        star.setAttribute("aria-checked", n === selected ? "true" : "false");
      });
    };

    const commit = (value) => {
      selected = value;
      if (input) input.value = String(value);
      paint(value);
    };

    stars.forEach((star) => {
      star.addEventListener("click", () => {
        commit(Number(star.dataset.ratingValue));
      });
      star.addEventListener("mouseenter", () => {
        paint(Number(star.dataset.ratingValue));
      });
    });

    group.addEventListener("mouseleave", () => {
      paint(selected);
    });

    commit(selected);
  });
}

export function initReviewForm() {
  const stampFields = (root = document) => {
    root.querySelectorAll("[data-review-ts]").forEach((el) => {
      if (!el.value) el.value = stamp();
    });
  };

  stampFields();
  bindRating();

  document.addEventListener("review-form:ready", () => {
    stampFields();
    bindRating(document);
  });
}
