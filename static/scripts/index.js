window.addEventListener("beforeunload", function (e) {
  document.getElementById("content").classList.add("fadeOut");
});

function toggleProfileMenu() {
  dropdown(
    // '[{"name": "Profile", "action": "/profile"}, {"name": "Item 1", "action": "/item1"}, {"name": "Item 2", "action": "/item_2/more"}, {"name": "Item 3", "action": "item_three_func()"}]',
    '[{"name": "Profile", "action": "/profile"}, {"name": "Logout", "action": "/logout"}]',
    30,
    70,
    true
  );
}

// function closeProfileMenu(event) {
//   if (!event.target.matches(".profile-menu-button")) {
//     document.getElementById("profile-menu").classList.add("hidden");
//   }
// }

// document.body.addEventListener("mouseup", closeProfileMenu, true);

// alert("hello");
