function finished_load() {
  document.body.style.overflow = "auto";
  document.getElementById("loading").classList.add("loading-out");
  setTimeout(function () {
    document.getElementById("loading").style.display = "none";
    document.getElementById("loading").remove();
  }, 500);
  setTimeout(function () {
    document.getElementById("content-div").classList.add("content-in");
  }, 200);
}

document.body.style.overflow = "hidden";
