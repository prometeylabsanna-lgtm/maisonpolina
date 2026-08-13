(() => {
  const bootRoot = (root) => {
    const bind = window.SelfBrand?.bindFormsetAdd;
    if (!bind) return;
    const prefix = root.getAttribute("data-cms-list-prefix");
    if (!prefix) return;
    bind({
      addBtn: root.querySelector("[data-cms-list-add]"),
      list: root.querySelector("[data-cms-list]"),
      template: document.getElementById(`${prefix}-empty-form-template`),
      totalInput: document.querySelector(`#id_${prefix}-TOTAL_FORMS`),
    });
  };

  const boot = () => {
    document.querySelectorAll("[data-cms-list-root]").forEach(bootRoot);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
