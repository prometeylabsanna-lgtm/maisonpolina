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

  const bindTypeRow = (row) => {
    const select = row.querySelector(".cms-style-select");
    if (select) {
      setMode(row, select.value || "");
      select.addEventListener("change", () => setMode(row, select.value || ""));
    }
    row.querySelectorAll("[data-value]").forEach((btn) => {
      btn.addEventListener("click", () => {
        setMode(row, btn.getAttribute("data-value") || "");
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
