(() => {
  const boot = () => {
    const addBtn = document.querySelector("[data-gallery-add]");
    const list = document.querySelector("[data-gallery-list]");
    const template = document.getElementById("gallery-empty-form-template");
    const totalInput = document.querySelector("#id_gallery-TOTAL_FORMS");
    if (!addBtn || !list || !template || !totalInput) return;

    addBtn.addEventListener("click", () => {
      const index = Number(totalInput.value || "0");
      let html = template.innerHTML.replaceAll("__prefix__", String(index));
      // Django empty_form uses __prefix__ in name/id attributes
      const wrap = document.createElement("div");
      wrap.innerHTML = html.trim();
      const node = wrap.firstElementChild;
      if (!node) return;
      list.appendChild(node);
      totalInput.value = String(index + 1);
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
