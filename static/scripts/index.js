window.addEventListener("beforeunload", function (e) {
  document.getElementById("content").classList.add("fadeOut");
});
