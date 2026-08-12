(function () {
  var key = "adminTheme";
  if (localStorage.getItem(key) === null) {
    localStorage.setItem(key, JSON.stringify("light"));
  }
})();
