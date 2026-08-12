/**
 * Sync TinyMCE with Unfold admin light/dark theme.
 * Loads before django_tinymce/init_tinymce.js via TINYMCE_EXTRA_MEDIA.
 */
(function () {
  var DARK_BODY_BG = "#1c1416";
  var DARK_BODY_FG = "#e8e0d8";
  var LIGHT_BODY_BG = "#ffffff";
  var LIGHT_BODY_FG = "#111827";

  function isAdminDark() {
    if (document.documentElement.classList.contains("dark")) {
      return true;
    }
    try {
      var theme = JSON.parse(localStorage.getItem("adminTheme") || '"light"');
      if (theme === "dark") return true;
      if (theme === "auto") {
        return window.matchMedia("(prefers-color-scheme: dark)").matches;
      }
    } catch (_err) {
      /* ignore */
    }
    return false;
  }

  function applyThemeToConfig(conf) {
    var next = Object.assign({}, conf);
    if (isAdminDark()) {
      next.skin = "oxide-dark";
      next.content_css = "dark";
      next.content_style = [
        next.content_style || "",
        "body{background-color:" + DARK_BODY_BG + ";color:" + DARK_BODY_FG + ";",
        "margin:0.85rem;line-height:1.55;}",
      ].join("");
    } else {
      next.skin = "oxide";
      next.content_css = false;
      next.content_style = [
        next.content_style || "",
        "body{background-color:" + LIGHT_BODY_BG + ";color:" + LIGHT_BODY_FG + ";",
        "margin:0.85rem;line-height:1.55;}",
      ].join("");
    }
    return next;
  }

  function styleEditorBody(editor) {
    var body = editor.getBody && editor.getBody();
    if (!body) return;
    var dark = isAdminDark();
    body.style.backgroundColor = dark ? DARK_BODY_BG : LIGHT_BODY_BG;
    body.style.color = dark ? DARK_BODY_FG : LIGHT_BODY_FG;
    var container = editor.getContainer && editor.getContainer();
    if (container) {
      container.classList.toggle("tox-tinymce--admin-dark", dark);
    }
  }

  function patchTinyMCEInit() {
    if (!window.tinyMCE || window.tinyMCE.__cmsThemePatched) return;
    var originalInit = window.tinyMCE.init.bind(window.tinyMCE);
    window.tinyMCE.init = function (conf) {
      var themed = applyThemeToConfig(conf || {});
      var userSetup = themed.setup;
      themed.setup = function (editor) {
        editor.on("init", function () {
          styleEditorBody(editor);
        });
        if (typeof userSetup === "function") {
          userSetup(editor);
        }
      };
      return originalInit(themed);
    };
    window.tinyMCE.__cmsThemePatched = true;
  }

  function refreshOpenEditors() {
    if (!window.tinyMCE || !window.tinyMCE.editors || !window.tinyMCE.editors.length) {
      document.documentElement.classList.toggle("tinymce-theme-dark", isAdminDark());
      return;
    }
    var snapshot = [];
    window.tinyMCE.editors.forEach(function (editor) {
      if (!editor || !editor.id) return;
      var el = document.getElementById(editor.id);
      if (!el || !el.dataset.mceConf) return;
      var conf;
      try {
        conf = JSON.parse(el.dataset.mceConf);
      } catch (_err) {
        return;
      }
      snapshot.push({
        id: editor.id,
        conf: conf,
        content: editor.getContent(),
      });
    });

    snapshot.forEach(function (item) {
      var existing = window.tinyMCE.get(item.id);
      if (existing) {
        existing.remove();
      }
    });

    snapshot.forEach(function (item) {
      var el = document.getElementById(item.id);
      if (!el) return;
      el.value = item.content;
      var conf = applyThemeToConfig(
        Object.assign({}, item.conf, { selector: "#" + item.id })
      );
      var userSetup = conf.setup;
      conf.setup = function (editor) {
        editor.on("init", function () {
          editor.setContent(item.content);
          styleEditorBody(editor);
        });
        if (typeof userSetup === "function") {
          userSetup(editor);
        } else if (typeof userSetup === "string" && window[userSetup]) {
          window[userSetup](editor);
        }
      };
      window.tinyMCE.init(conf);
    });

    document.documentElement.classList.toggle("tinymce-theme-dark", isAdminDark());
  }

  function boot() {
    patchTinyMCEInit();
    document.documentElement.classList.toggle("tinymce-theme-dark", isAdminDark());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  // TinyMCE script may load after this file — retry patch.
  var tries = 0;
  var timer = window.setInterval(function () {
    tries += 1;
    if (window.tinyMCE) {
      patchTinyMCEInit();
      window.clearInterval(timer);
    } else if (tries > 40) {
      window.clearInterval(timer);
    }
  }, 50);

  var lastDark = isAdminDark();
  new MutationObserver(function () {
    var next = isAdminDark();
    if (next === lastDark) return;
    lastDark = next;
    refreshOpenEditors();
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });
})();
