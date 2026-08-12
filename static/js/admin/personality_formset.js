(() => {
  const bootRoot = (root) => {
    const prefix = root.getAttribute("data-personality-prefix");
    if (!prefix) return;
    const addBtn = root.querySelector("[data-personality-add]");
    const list = root.querySelector("[data-personality-list]");
    const template = document.getElementById(`${prefix}-empty-form-template`);
    const totalInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
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
      const firstInput = node.querySelector("input:not([type=hidden]), textarea");
      if (firstInput) firstInput.focus();
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  };

  const boot = () => {
    document.querySelectorAll("[data-personality-root]").forEach(bootRoot);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
