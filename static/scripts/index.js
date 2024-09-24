window.addEventListener("beforeunload", function (e) {
  document.getElementById("content").classList.add("fadeOut");
});

function toggleProfileMenu() {
  dropdown(
    // '[{"name": "Profile", "action": "/profile"}, {"name": "Item 1", "action": "/item1"}, {"name": "Item 2", "action": "/item_2/more"}, {"name": "Item 3", "action": "item_three_func()"}]',
    '[{"name": "Profile", "action": "/profile"}, {"name": "Help Center", "action": "/help"}, {"name": "Copy Save Link", "action": "copy_link()"}, {"name": "Logout", "action": "/logout"}]',
    30,
    70,
    true
  );
}

function copy_link() {
  // send request to /api/get_username with token
  var url = "/api/get_username";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: getCookie("token"),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        var short_url = "https://ssave.co/" + data.username;
        navigator.clipboard.writeText(short_url);
        alert(
          "The link was successfully copied to your clipboard: " + short_url
        );
      } else {
        alert("Error copying link");
      }
    });
}

function toggleShareMenu() {
  // create dropdown at current mouse position
  var mouseX = event.clientX;
  var mouseY = event.clientY;
  dropdown(
    '[{"name": "Copy Link", "action": "copy_link()"}]',
    mouseX,
    mouseY,
    false
  );
}

// function closeProfileMenu(event) {
//   if (!event.target.matches(".profile-menu-button")) {
//     document.getElementById("profile-menu").classList.add("hidden");
//   }
// }

// document.body.addEventListener("mouseup", closeProfileMenu, true);

// alert("hello");
