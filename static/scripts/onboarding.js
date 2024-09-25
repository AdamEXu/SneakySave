function nextStep() {
  // use api to check if the username is valid
  // /api/check_username?username=username (get request is fine)
  var username = document.getElementById("username").value;
  if (username.length < 3) {
    document.getElementById("username-error").innerText =
      "Username must be at least 3 characters long";
  }
  document.getElementById("step-1").classList.add("completed");

  var url = "/api/check_username?username=" + username;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("step-2").classList.remove("upcoming");
        document
          .getElementById("done-text-username")
          .classList.remove("hidden");
        document.getElementById("username-submit-btn").style.opacity = "0";
        document.getElementById("username-error").innerText = "";
        setTimeout(function () {
          document.getElementById("username-submit-btn").remove();
        }, 200);
      } else {
        document.getElementById("username-error").innerText = data.error;
        document.getElementById("step-1").classList.remove("completed");
      }
    });
}

document.getElementById("save-file").addEventListener("change", function () {
  const file = this.files[0];
  const fileError = document.getElementById("save-file-error");

  var url = "/api/check_save";
  var formData = new FormData();
  formData.append("save-file", document.getElementById("save-file").files[0]);
  fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("step-2").classList.add("completed");
        document.getElementById("step-3").classList.remove("upcoming");
      } else {
        fileError.innerText = data.error;
      }
    });
});

function submitForm() {
  // 0. ensure that all the checkboxes are checked (except for public profile), if not, return and display an error message
  if (!document.getElementById("agree-terms").checked) {
    document.getElementById("agree-error").innerText =
      "You must agree to the terms and conditions to continue";
    return;
  }
  if (!document.getElementById("agree-privacy").checked) {
    document.getElementById("agree-error").innerText =
      "You must agree to the privacy policy to continue";
    return;
  }
  if (!document.getElementById("agree-early").checked) {
    document.getElementById("agree-error").innerText =
      "You must agree to the early access terms to continue";
    return;
  }
  // 1. check one more time if the username is valid (if not, redirect to /help/username-error)
  var username = document.getElementById("username").value;
  if (username.length < 3) {
    window.location.href = "/help/username-error";
    return;
  }
  var url = "/api/check_username?username=" + username;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        window.location.href = "/help/username-error";
        return;
      }
    });
  // 3. change the loading text from "Let's let you onboarded..." to "Please wait while we analyze your save... (this may take a while)" and display the loading animation again
  document.getElementById("load-text").innerText =
    "Please wait while we analyze your save... (this may take a while)";
  document.getElementById("gobtn").style.display = "none";
  show_loading();
  // 2. send post request to /api/onboard with the username and save file
  var url = "/api/onboard";
  var formData = new FormData();
  formData.append("username", username);
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
        window.location.href = "/help/onboarding-error";
      }
    });
}
