const stack = [];
let listening = false;

function onKeydown(e) {
  if (e.key !== "Escape" || !stack.length) return;
  const top = stack[stack.length - 1];
  e.preventDefault();
  e.stopImmediatePropagation();
  top.closeFn();
}

function ensureListener() {
  if (listening) return;
  listening = true;
  document.addEventListener("keydown", onKeydown, true);
}

export function registerEscape(id, closeFn) {
  unregisterEscape(id);
  stack.push({ id, closeFn });
  ensureListener();
}

export function unregisterEscape(id) {
  const i = stack.findIndex((entry) => entry.id === id);
  if (i >= 0) stack.splice(i, 1);
}
