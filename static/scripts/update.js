document.getElementById("save-file").addEventListener("change", function () {
  const file = this.files[0];
  const fileError = document.getElementById("save-file-error");

  var url = "/api/check_save";
  var formData = new FormData();
  formData.append("save-file", document.getElementById("save-file").files[0]);
  formData.append("token", getCookie("token"));
  fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.href = "/";
      } else {
        fileError.innerText = data.error;
      }
    });
});
