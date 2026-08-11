const STORAGE_SESSION = "chat_session_id";
const STORAGE_USER = "chat_user_identifier";
const POLL_MS = 4000;

function csrfToken() {
  return (
    document.querySelector('meta[name="csrf-token"]')?.getAttribute("content") ||
    document.querySelector("[data-chat-form] input[name=csrfmiddlewaretoken]")?.value ||
    ""
  );
}

function pageLanguage() {
  return (document.documentElement.lang || "ru").slice(0, 2);
}

function langHeaders(extra = {}) {
  const lang = pageLanguage();
  return {
    "Accept-Language": lang,
    "X-Requested-Language": lang,
    ...extra,
  };
}

function getStored(key) {
  try {
    return localStorage.getItem(key) || "";
  } catch {
    return "";
  }
}

function setStored(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    /* private mode / quota */
  }
}

function scrollMessages(el) {
  if (!el) return;
  el.scrollTop = el.scrollHeight;
}

function lastMessageId(container) {
  const nodes = container.querySelectorAll("[data-msg-id]");
  if (!nodes.length) return "";
  return nodes[nodes.length - 1].getAttribute("data-msg-id") || "";
}

export function initChatWidget() {
  const root = document.querySelector("[data-chat-widget]");
  if (!root) return;

  const toggle = root.querySelector("[data-chat-toggle]");
  const panel = root.querySelector("[data-chat-panel]");
  const closeBtn = root.querySelector("[data-chat-close]");
  const backdrop = document.querySelector("[data-chat-backdrop]");
  const form = root.querySelector("[data-chat-form]");
  const input = root.querySelector("[data-chat-input]");
  const messagesEl = root.querySelector("[data-chat-messages]");
  const badge = root.querySelector("[data-chat-badge]");
  const sendBtn = root.querySelector("[data-chat-send]");

  const sessionUrl = root.dataset.sessionUrl;
  const messagesUrl = root.dataset.messagesUrl;
  const sendUrl = root.dataset.sendUrl;

  let sessionId = getStored(STORAGE_SESSION);
  let userIdentifier = getStored(STORAGE_USER);
  let open = false;
  let pollTimer = null;
  let ensuring = null;

  function setOpen(next) {
    open = next;
    if (!panel || !toggle) return;
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) backdrop.hidden = !open;
    document.body.classList.toggle("is-chat-open", open);
    if (open) {
      if (badge) badge.hidden = true;
      ensureSession()
        .then(() => loadMessages(false))
        .then(() => {
          startPoll();
          input?.focus({ preventScroll: true });
          scrollMessages(messagesEl);
        })
        .catch(() => { });
    } else {
      stopPoll();
    }
  }

  function startPoll() {
    stopPoll();
    pollTimer = window.setInterval(() => {
      if (open) loadMessages(true).catch(() => { });
    }, POLL_MS);
  }

  function stopPoll() {
    if (pollTimer) {
      window.clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  async function ensureSession() {
    if (sessionId && userIdentifier) return { sessionId, userIdentifier };
    if (ensuring) return ensuring;

    ensuring = (async () => {
      const body = new URLSearchParams();
      if (sessionId) body.set("session_id", sessionId);
      if (userIdentifier) body.set("user_identifier", userIdentifier);

      const res = await fetch(sessionUrl, {
        method: "POST",
        headers: langHeaders({
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken(),
        }),
        body,
        credentials: "same-origin",
      });
      if (!res.ok) throw new Error("session_failed");
      const data = await res.json();
      sessionId = data.session_id;
      userIdentifier = data.user_identifier;
      setStored(STORAGE_SESSION, sessionId);
      setStored(STORAGE_USER, userIdentifier);
      return { sessionId, userIdentifier };
    })();

    try {
      return await ensuring;
    } finally {
      ensuring = null;
    }
  }

  async function loadMessages(appendOnly) {
    await ensureSession();
    const url = new URL(messagesUrl, window.location.origin);
    url.searchParams.set("session_id", sessionId);
    url.searchParams.set("user_identifier", userIdentifier);
    if (appendOnly) {
      const after = lastMessageId(messagesEl);
      if (after) url.searchParams.set("after_id", after);
    }

    const res = await fetch(url.toString(), {
      headers: langHeaders({ "HX-Request": "true" }),
      credentials: "same-origin",
    });
    if (!res.ok) return;
    const html = await res.text();
    if (!html.trim()) return;

    if (appendOnly && lastMessageId(messagesEl)) {
      const had = messagesEl.querySelectorAll("[data-msg-id]").length;
      messagesEl.querySelector(".chat-widget__empty")?.remove();
      messagesEl.insertAdjacentHTML("beforeend", html);
      const now = messagesEl.querySelectorAll("[data-msg-id]").length;
      if (now > had) {
        scrollMessages(messagesEl);
        if (!open && badge) badge.hidden = false;
      }
    } else {
      messagesEl.innerHTML = html;
      scrollMessages(messagesEl);
    }
  }

  async function sendMessage(text) {
    await ensureSession();
    const body = new URLSearchParams();
    body.set("session_id", sessionId);
    body.set("user_identifier", userIdentifier);
    body.set("text", text);
    body.set("csrfmiddlewaretoken", csrfToken());

    if (sendBtn) sendBtn.disabled = true;
    try {
      const res = await fetch(sendUrl, {
        method: "POST",
        headers: langHeaders({
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken(),
          "HX-Request": "true",
        }),
        body,
        credentials: "same-origin",
      });
      const html = await res.text();
      if (res.ok) {
        messagesEl.innerHTML = html;
        scrollMessages(messagesEl);
      } else if (html) {
        messagesEl.insertAdjacentHTML("beforeend", html);
        scrollMessages(messagesEl);
      }
    } finally {
      if (sendBtn) sendBtn.disabled = false;
    }
  }

  toggle?.addEventListener("click", () => setOpen(!open));
  closeBtn?.addEventListener("click", () => setOpen(false));
  backdrop?.addEventListener("click", () => setOpen(false));

  document.addEventListener("click", (e) => {
    const opener = e.target.closest("[data-open-chat]");
    if (!opener) return;
    e.preventDefault();
    setOpen(true);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && open) setOpen(false);
  });

  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = (input?.value || "").trim();
    if (!text) return;
    if (input) input.value = "";
    autoGrow();
    sendMessage(text).catch(() => { });
  });

  function autoGrow() {
    if (!input) return;
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 96)}px`;
  }

  input?.addEventListener("input", autoGrow);
  input?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form?.requestSubmit();
    }
  });

  if (sessionId && userIdentifier) {
    ensureSession().catch(() => { });
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopPoll();
    else if (open) startPoll();
  });
}
