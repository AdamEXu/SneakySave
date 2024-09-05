var currentStep = 0;

function nextStep() {
  var coversheets = document.getElementsByClassName("coversheet");
  var holder = document.querySelector(".coversheet-holder");
  currentStep = Math.min(currentStep + 1, coversheets.length - 1); // Ensure we don't go beyond the last card

  var cardWidth = coversheets[currentStep].offsetWidth; // Get the width of each card
  var holderWidth = holder.offsetWidth; // Get the width of the container

  // Calculate the scroll position to center the current card
  var scrollPosition =
    coversheets[currentStep].offsetLeft - (holderWidth - cardWidth) / 2;

  // Scroll the container smoothly to the new position
  holder.scrollTo({
    left: scrollPosition,
    behavior: "smooth",
  });

  // Hide or show next/previous buttons based on the current position
  document
    .getElementById("next-button")
    .classList.toggle("hidden", currentStep >= coversheets.length - 1);
  document
    .getElementById("prev-button")
    .classList.toggle("hidden", currentStep <= 0);
}

function previousStep() {
  var coversheets = document.getElementsByClassName("coversheet");
  var holder = document.querySelector(".coversheet-holder");
  currentStep = Math.max(currentStep - 1, 0); // Ensure we don't go before the first card

  var cardWidth = coversheets[currentStep].offsetWidth; // Get the width of each card
  var holderWidth = holder.offsetWidth; // Get the width of the container

  // Calculate the scroll position to center the current card
  var scrollPosition =
    coversheets[currentStep].offsetLeft - (holderWidth - cardWidth) / 2;

  // Scroll the container smoothly to the new position
  holder.scrollTo({
    left: scrollPosition,
    behavior: "smooth",
  });

  // Hide or show next/previous buttons based on the current position
  document
    .getElementById("next-button")
    .classList.toggle("hidden", currentStep >= coversheets.length - 1);
  document
    .getElementById("prev-button")
    .classList.toggle("hidden", currentStep <= 0);
}
