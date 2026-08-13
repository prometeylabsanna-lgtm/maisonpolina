(() => {
  const normalizeHex = (raw) => {
    const value = (raw || "").trim();
    if (/^#[0-9A-Fa-f]{6}$/.test(value)) return value;
    if (/^#[0-9A-Fa-f]{3}$/.test(value)) {
      const a = value[1];
      const b = value[2];
      const c = value[3];
      return `#${a}${a}${b}${b}${c}${c}`;
    }
    return "";
  };

  const syncPicker = (picker) => {
    const targetId = picker.getAttribute("data-hex-target");
    if (!targetId) return;
    const input = document.getElementById(targetId);
    if (!input) return;
    const hex = normalizeHex(input.value);
    if (hex) picker.value = hex;
  };

  const bindPicker = (picker) => {
    const targetId = picker.getAttribute("data-hex-target");
    if (!targetId) return;
    const input = document.getElementById(targetId);
    if (!input) return;
    picker.addEventListener("input", () => {
      input.value = picker.value;
    });
    input.addEventListener("change", () => syncPicker(picker));
    input.addEventListener("input", () => syncPicker(picker));
    syncPicker(picker);
  };

  const setMode = (row, mode) => {
    row.setAttribute("data-mode", mode);
    const select = row.querySelector(".cms-style-select");
    if (select) select.value = mode;
    row.querySelectorAll("[data-value]").forEach((btn) => {
      const on = btn.getAttribute("data-value") === mode;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  };

  const resetRowDefaults = (row) => {
    const solidInput = row.querySelector('[data-show="solid"] .cms-hex-input');
    const gradInputs = row.querySelectorAll('[data-show="gradient"] .cms-hex-input');
    const angleInput = row.querySelector(".cms-style-angle");
    if (solidInput) {
      solidInput.value = row.getAttribute("data-default-solid") || "";
    }
    if (gradInputs[0]) {
      gradInputs[0].value = row.getAttribute("data-default-start") || "";
    }
    if (gradInputs[1]) {
      gradInputs[1].value = row.getAttribute("data-default-end") || "";
    }
    if (angleInput) {
      angleInput.value = row.getAttribute("data-default-angle") || "180";
    }
    row.querySelectorAll(".cms-color-picker").forEach(syncPicker);
  };

  const bindTypeRow = (row) => {
    const select = row.querySelector(".cms-style-select");
    if (select) {
      setMode(row, select.value || "");
      select.addEventListener("change", () => {
        const mode = select.value || "";
        setMode(row, mode);
        if (!mode) resetRowDefaults(row);
      });
    }
    row.querySelectorAll("[data-value]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.getAttribute("data-value") || "";
        setMode(row, mode);
        if (!mode) resetRowDefaults(row);
      });
    });
  };

  document.querySelectorAll(".cms-color-picker").forEach(bindPicker);
  document.querySelectorAll("[data-style-row]").forEach(bindTypeRow);

  document.querySelectorAll("[data-confirm-reset]").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      const message = btn.getAttribute("data-confirm-reset") || "Вернуть дефолт?";
      if (!window.confirm(message)) event.preventDefault();
    });
  });
})();
