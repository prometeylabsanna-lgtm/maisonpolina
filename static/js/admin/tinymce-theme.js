/**
 * Sync TinyMCE with Unfold .dark class only.
 * Light = white field. Dark = dark theme surface. Gold border only — no burgundy fill.
 * Does not write classes on <html> (that broke editing via re-init loop).
 */
(function () {
  var DARK_BODY_BG = "#111827";
  var DARK_BODY_FG = "#e5e7eb";
  var LIGHT_BODY_BG = "#ffffff";
  var LIGHT_BODY_FG = "#111827";
  var reinitLock = false;

  function isAdminDark() {
    return document.documentElement.classList.contains("dark");
  }

  function applyThemeToConfig(conf) {
    var next = Object.assign({}, conf);
    if (isAdminDark()) {
      next.skin = "oxide-dark";
      next.content_css = "dark";
      next.content_style =
        "body{background-color:" +
        DARK_BODY_BG +
        ";color:" +
        DARK_BODY_FG +
        ";margin:0.85rem;line-height:1.55;}";
    } else {
      next.skin = "oxide";
      next.content_css = false;
      next.content_style =
        "body{background-color:" +
        LIGHT_BODY_BG +
        ";color:" +
        LIGHT_BODY_FG +
        ";margin:0.85rem;line-height:1.55;}";
    }
    return next;
  }

  function styleEditorBody(editor) {
    var body = editor.getBody && editor.getBody();
    if (!body) return;
    var dark = isAdminDark();
    body.style.backgroundColor = dark ? DARK_BODY_BG : LIGHT_BODY_BG;
    body.style.color = dark ? DARK_BODY_FG : LIGHT_BODY_FG;
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
        } else if (typeof userSetup === "string" && window[userSetup]) {
          window[userSetup](editor);
        }
      };
      return originalInit(themed);
    };
    window.tinyMCE.__cmsThemePatched = true;
  }

  function reinitOpenEditors() {
    if (reinitLock || !window.tinyMCE || !window.tinyMCE.editors) return;
    reinitLock = true;
    try {
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
        if (existing) existing.remove();
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
    } finally {
      window.setTimeout(function () {
        reinitLock = false;
      }, 100);
    }
  }

  function boot() {
    patchTinyMCEInit();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

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
    reinitOpenEditors();
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });
})();
