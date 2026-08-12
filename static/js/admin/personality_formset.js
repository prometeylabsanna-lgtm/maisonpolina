(() => {
  const bootRoot = (root) => {
    const bind = window.SelfBrand?.bindFormsetAdd;
    if (!bind) return;
    const prefix = root.getAttribute("data-personality-prefix");
    if (!prefix) return;
    bind({
      addBtn: root.querySelector("[data-personality-add]"),
      list: root.querySelector("[data-personality-list]"),
      template: document.getElementById(`${prefix}-empty-form-template`),
      totalInput: document.querySelector(`#id_${prefix}-TOTAL_FORMS`),
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
