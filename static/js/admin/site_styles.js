(() => {
  document.querySelectorAll(".cms-color-picker").forEach((picker) => {
    const targetId = picker.getAttribute("data-hex-target");
    if (!targetId) return;
    const input = document.getElementById(targetId);
    if (!input) return;

    const syncPicker = () => {
      const raw = (input.value || "").trim();
      if (/^#[0-9A-Fa-f]{6}$/.test(raw)) {
        picker.value = raw;
      } else if (/^#[0-9A-Fa-f]{3}$/.test(raw)) {
        const [, a, b, c] = raw;
        picker.value = `#${a}${a}${b}${b}${c}${c}`;
      }
    };

    picker.addEventListener("input", () => {
      input.value = picker.value;
    });
    input.addEventListener("change", syncPicker);
    syncPicker();
  });
})();
