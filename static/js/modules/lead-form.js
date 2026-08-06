export function initLeadForm() {
  const stamp = () => String(Date.now() / 1000);
  document.querySelectorAll("[data-lead-ts]").forEach((el) => {
    if (!el.value) el.value = stamp();
  });

  document.body.addEventListener("htmx:configRequest", (event) => {
    const token =
      document.querySelector('meta[name="csrf-token"]')?.getAttribute("content") ||
      "";
    if (token) event.detail.headers["X-CSRFToken"] = token;
  });

  // Preserve scroll anchor when switching language
  document.querySelectorAll("[data-lang-switch]").forEach((link) => {
    link.addEventListener("click", (e) => {
      const sections = [...document.querySelectorAll("[data-section]")];
      let current = "";
      const mid = window.scrollY + window.innerHeight * 0.3;
      sections.forEach((sec) => {
        if (sec.offsetTop <= mid) current = sec.id;
      });
      if (!current) return;
      const url = new URL(link.href, window.location.origin);
      url.hash = current;
      e.preventDefault();
      window.location.href = url.toString();
    });
  });

  if (window.location.hash) {
    const el = document.querySelector(window.location.hash);
    if (el) {
      window.setTimeout(() => {
        el.scrollIntoView({ behavior: "auto", block: "start" });
      }, 0);
    }
  }
}
