document.getElementById("save-file").addEventListener("change", function () {
  const file = this.files[0];
  const fileError = document.getElementById("save-file-error");
  if (file && file.name.endsWith(".txt")) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const file_content = e.target.result;
      if (
        file_content.startsWith("**********CLOUDPROFILE0\n") ||
        file_content.startsWith("**********PROFILE0\n")
      ) {
        if (
          file_content.endsWith(
            "--------default3/map/3f43248e5acd441dcb61e402a42e25e6.stuff 2b\n{}\n"
          )
        ) {
          document.getElementById("save-file-name").innerText = file.name;
          fileError.innerText = "Uploading...";
          fileError.style.color = "#000";
          var url = "/api/update";
          var formData = new FormData();
          formData.append(
            "save-file",
            document.getElementById("save-file").files[0]
          );
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
                window.location.href = "/help/onboarding-error";
              }
            });
        } else {
          fileError.innerText = "End of file is not matching";
        }
      } else {
        fileError.innerText = "Beginning of file is not matching";
      }
    };
    reader.readAsText(file);
  } else {
    fileError.innerText = "Invalid file type";
  }
});
