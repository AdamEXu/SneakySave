function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "not_found";
}

// dropdown.js

function dropdown(jsonStr, loc_x, loc_y, right_align) {
  // Check if the dropdown is already open
  var existingDropdown = document.getElementById("custom-dropdown-menu");
  if (existingDropdown) {
    var existingContent = existingDropdown.getAttribute(
      "data-dropdown-content"
    );
    if (existingContent === jsonStr) {
      // If the content is the same, remove the dropdown and return
      existingDropdown.parentNode.removeChild(existingDropdown);
      return;
    } else {
      // If the content is different, remove the existing dropdown
      existingDropdown.parentNode.removeChild(existingDropdown);
    }
  }

  // Parse the JSON string
  var items;
  try {
    items = JSON.parse(jsonStr);
  } catch (e) {
    console.error("Invalid JSON string provided to dropdown function.");
    return;
  }

  // Create the dropdown container
  var dropdownDiv = document.createElement("div");
  dropdownDiv.id = "custom-dropdown-menu";
  dropdownDiv.className = "dropdown-menu";

  // Store the JSON string as a data attribute
  dropdownDiv.setAttribute("data-dropdown-content", jsonStr);

  // Position the dropdown
  dropdownDiv.style.position = "absolute";
  dropdownDiv.style.top = loc_y + "px";
  if (right_align) {
    dropdownDiv.style.right = loc_x + "px";
  } else {
    dropdownDiv.style.left = loc_x + "px";
  }

  // Create the list of items
  items.forEach(function (item) {
    var listItem = document.createElement("div");
    listItem.className = "dropdown-item";

    var action = item.action;
    var element;
    if (action.trim().endsWith(")")) {
      // Create an element with onclick
      element = document.createElement("a");
      element.href = "#";
      element.onclick = function (e) {
        e.stopPropagation();
        // Evaluate the function
        try {
          eval(action);
        } catch (err) {
          console.error("Error executing action:", err);
        }
        // Remove dropdown after action
        if (dropdownDiv.parentNode) {
          dropdownDiv.parentNode.removeChild(dropdownDiv);
        }
      };
    } else {
      // Create an anchor element with href
      element = document.createElement("a");
      element.href = action;
      element.onclick = function (e) {
        // Let the default action happen
        e.stopPropagation();
        // Remove dropdown after action
        if (dropdownDiv.parentNode) {
          dropdownDiv.parentNode.removeChild(dropdownDiv);
        }
      };
    }

    element.innerText = item.name;

    listItem.appendChild(element);
    dropdownDiv.appendChild(listItem);
  });

  // Append the dropdown to the body
  document.body.appendChild(dropdownDiv);

  // Remove dropdown when clicking elsewhere
  var removeDropdown = function (e) {
    if (dropdownDiv && !dropdownDiv.contains(e.target)) {
      if (dropdownDiv.parentNode) {
        dropdownDiv.parentNode.removeChild(dropdownDiv);
      }
      document.removeEventListener("click", removeDropdown);
    }
  };

  // Delay adding the event listener to avoid immediate removal
  setTimeout(function () {
    document.addEventListener("click", removeDropdown);
  }, 0);
}
