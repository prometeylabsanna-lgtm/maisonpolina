const FORM_SEL = "[data-lead-form], [data-review-form]";
const FIELD_SEL = "[data-validate]";
const ERROR_CLASS = "form__input--error";
const FIELD_ERROR_CLASS = "form__field--error";

const FALLBACK = {
  nameDigits: "Имя не должно содержать цифр.",
  phone: "Номер телефона не может содержать буквы и должен содержать от 7 до 14 цифр.",
  messageMin: "Текст отзыва должен содержать минимум 2 символа.",
};

const PHONE_ALLOWED = /^[0-9+\-()\s]*$/;
const NAME_DIGIT = /[0-9]/;
const MIN_PHONE_DIGITS = 7;
const MAX_PHONE_DIGITS = 14;
const MIN_MESSAGE = 2;

function digitCount(value) {
  return (value.match(/[0-9]/g) || []).length;
}

function messagesFor(form) {
  return {
    nameDigits: form?.dataset?.msgNameDigits || FALLBACK.nameDigits,
    phone: form?.dataset?.msgPhone || FALLBACK.phone,
    messageMin: form?.dataset?.msgMessageMin || FALLBACK.messageMin,
  };
}

export function nameError(value, messages = FALLBACK) {
  return NAME_DIGIT.test(value) ? messages.nameDigits : "";
}

export function phoneError(value, messages = FALLBACK) {
  const digits = digitCount(value);
  if (
    !value.trim() ||
    !PHONE_ALLOWED.test(value) ||
    digits < MIN_PHONE_DIGITS ||
    digits > MAX_PHONE_DIGITS
  ) {
    return messages.phone;
  }
  return "";
}

export function messageError(value, required, messages = FALLBACK) {
  const len = value.trim().length;
  if (len === 0) {
    return required ? messages.messageMin : "";
  }
  return len < MIN_MESSAGE ? messages.messageMin : "";
}

function errorFor(field) {
  const form = field.closest(FORM_SEL);
  const messages = messagesFor(form);
  const type = field.dataset.validate;
  const value = field.value || "";
  if (type === "name") return nameError(value, messages);
  if (type === "phone") return phoneError(value, messages);
  if (type === "message") return messageError(value, false, messages);
  if (type === "review") return messageError(value, true, messages);
  return "";
}

function fieldWrap(field) {
  return field.closest(".form__field");
}

function errorEl(field) {
  const wrap = fieldWrap(field);
  if (!wrap) return null;
  let el = wrap.querySelector("[data-field-error]");
  if (!el) {
    el = document.createElement("span");
    el.className = "form__field-error";
    el.dataset.fieldError = "";
    el.setAttribute("role", "alert");
    el.setAttribute("aria-live", "polite");
    wrap.appendChild(el);
  }
  return el;
}

export function setFieldError(field, message) {
  const wrap = fieldWrap(field);
  const el = errorEl(field);
  if (message) {
    field.classList.add(ERROR_CLASS);
    field.setAttribute("aria-invalid", "true");
    wrap?.classList.add(FIELD_ERROR_CLASS);
    if (el) {
      el.textContent = message;
      el.hidden = false;
    }
    return;
  }
  field.classList.remove(ERROR_CLASS);
  field.removeAttribute("aria-invalid");
  wrap?.classList.remove(FIELD_ERROR_CLASS);
  if (el) {
    el.textContent = "";
    el.hidden = true;
  }
}

function validateField(field) {
  const message = errorFor(field);
  setFieldError(field, message);
  return message;
}

function formFields(form) {
  return [...form.querySelectorAll(FIELD_SEL)];
}

export function validateForm(form) {
  let firstInvalid = null;
  formFields(form).forEach((field) => {
    const message = validateField(field);
    if (message && !firstInvalid) firstInvalid = field;
  });
  return firstInvalid;
}

function firstNativeInvalid(form) {
  return form.querySelector(":invalid");
}

function markEmptyRequired(form) {
  [...form.querySelectorAll(":invalid")].forEach((field) => {
    if (!(field instanceof HTMLElement)) return;
    if (field.matches(FIELD_SEL) && errorFor(field)) return;
    field.classList.add(ERROR_CLASS);
    field.setAttribute("aria-invalid", "true");
    fieldWrap(field)?.classList.add(FIELD_ERROR_CLASS);
  });
}

function focusInvalid(field) {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isIOS =
    /iP(hone|ad|od)/.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

  window.requestAnimationFrame(() => {
    try {
      field.focus({ preventScroll: true });
    } catch {
      field.focus();
    }
    field.scrollIntoView({
      block: "center",
      inline: "nearest",
      behavior: reduceMotion || isIOS ? "auto" : "smooth",
    });
  });
}

function isPublicForm(form) {
  return form instanceof HTMLFormElement && form.matches(FORM_SEL);
}

function onSubmit(event) {
  const form = event.target;
  if (!isPublicForm(form)) return;
  const firstCustomInvalid = validateForm(form);
  markEmptyRequired(form);
  const firstInvalid = firstCustomInvalid || firstNativeInvalid(form);
  if (!firstInvalid) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  focusInvalid(firstInvalid);
}

function onBeforeRequest(event) {
  const elt = event.detail?.elt;
  const form = elt instanceof HTMLFormElement ? elt : elt?.closest?.("form");
  if (!isPublicForm(form)) return;
  const firstCustomInvalid = validateForm(form);
  markEmptyRequired(form);
  const firstInvalid = firstCustomInvalid || firstNativeInvalid(form);
  if (!firstInvalid) return;
  event.preventDefault();
  focusInvalid(firstInvalid);
}

function onFieldEvent(event) {
  const field = event.target;
  if (!(field instanceof HTMLElement) || !field.closest(FORM_SEL)) return;
  if (field.matches(FIELD_SEL)) {
    validateField(field);
    return;
  }
  if (field instanceof HTMLInputElement && field.type === "checkbox" && field.checkValidity()) {
    field.classList.remove(ERROR_CLASS);
    field.removeAttribute("aria-invalid");
  }
}

let bound = false;

export function initFormValidation() {
  if (bound) return;
  bound = true;
  document.addEventListener("submit", onSubmit, true);
  document.body.addEventListener("htmx:beforeRequest", onBeforeRequest);
  document.addEventListener("input", onFieldEvent);
  document.addEventListener("change", onFieldEvent);
  document.addEventListener("blur", onFieldEvent, true);
}
