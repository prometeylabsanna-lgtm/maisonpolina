(() => {
  const boot = () => {
    const addBtn = document.querySelector("[data-gallery-add]");
    const list = document.querySelector("[data-gallery-list]");
    const template = document.getElementById("gallery-empty-form-template");
    const totalInput = document.querySelector("#id_gallery-TOTAL_FORMS");
    if (!addBtn || !list || !template || !totalInput) return;

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
      const fileInput = node.querySelector('input[type="file"]');
      if (fileInput) fileInput.focus();
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
