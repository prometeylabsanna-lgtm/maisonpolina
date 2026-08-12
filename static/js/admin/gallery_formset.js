(() => {
  const boot = () => {
    const bind = window.SelfBrand?.bindFormsetAdd;
    if (!bind) return;
    bind({
      addBtn: document.querySelector("[data-gallery-add]"),
      list: document.querySelector("[data-gallery-list]"),
      template: document.getElementById("gallery-empty-form-template"),
      totalInput: document.querySelector("#id_gallery-TOTAL_FORMS"),
      focusSelector: 'input[type="file"]',
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
