var text_pool = [
  "explorer",
  "sharer",
  "visualizer",
  "reader",
  "opener",
  "loader",
];
var currentIndex = 0;

function changeText() {
  var text = document.getElementById("save-text-effect");
  var currentWord = text_pool[currentIndex];
  var nextIndex = (currentIndex + 1) % text_pool.length;
  var nextWord = text_pool[nextIndex];

  // Clear the current word
  function clearWord(callback) {
    var length = text.textContent.length;
    var i = length;
    var interval = setInterval(function () {
      text.textContent = text.textContent.slice(0, -1);
      i--;
      if (i === 0) {
        clearInterval(interval);
        callback();
      }
    }, 50);
  }

  // Write the next word
  function writeWord(callback) {
    var i = 0;
    var interval = setInterval(function () {
      text.textContent += nextWord[i];
      i++;
      if (i === nextWord.length) {
        clearInterval(interval);
        callback();
      }
    }, 50);
  }

  // Chain the animations
  clearWord(function () {
    writeWord(function () {
      currentIndex = nextIndex;
      setTimeout(changeText, 1000); // Wait 1 second before starting the next cycle
    });
  });
}

// Initialize with the first word and start the animation
function initializeAndStart() {
  var text = document.getElementById("save-text-effect");
  if (text) {
    text.textContent = text_pool[0];
    setTimeout(changeText, 1000); // Start changing after 1 second
  } else {
    console.error("Element with id 'save-text-effect' not found");
  }
}

// Start the animation when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", initializeAndStart);
