(() => {
  const root = (window.SelfBrand = window.SelfBrand || {});
  if (root.bindFormsetAdd) return;

  /**
   * Shared Django formset "add row" binder.
   * @param {{
   *   addBtn: Element,
   *   list: Element,
   *   template: HTMLElement,
   *   totalInput: HTMLInputElement,
   *   focusSelector?: string
   * }} opts
   */
  root.bindFormsetAdd = ({ addBtn, list, template, totalInput, focusSelector }) => {
    if (!addBtn || !list || !template || !totalInput) return;
    if (addBtn.dataset.bound === "1") return;
    addBtn.dataset.bound = "1";

    addBtn.addEventListener("click", () => {
      const index = Number(totalInput.value || "0");
      const html = template.innerHTML.replaceAll("__prefix__", String(index));
      const wrap = document.createElement("div");
      wrap.innerHTML = html.trim();
      const node = wrap.firstElementChild;
      if (!node) return;

      node.querySelectorAll("[name], [id], [for]").forEach((el) => {
        ["name", "id", "for"].forEach((attr) => {
          const value = el.getAttribute(attr);
          if (value && value.includes("__prefix__")) {
            el.setAttribute(attr, value.replaceAll("__prefix__", String(index)));
          }
        });
      });

      list.appendChild(node);
      totalInput.value = String(index + 1);

      const focusEl = focusSelector
        ? node.querySelector(focusSelector)
        : node.querySelector("input:not([type=hidden]), textarea");
      if (focusEl) focusEl.focus();
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  };
})();
