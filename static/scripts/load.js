function show_loading() {
  const loading = document.getElementById("loading");
  const contentDiv = document.getElementById("content-div");
  
  // Immediately hide content and show loading
  contentDiv.classList.remove("content-in");
  contentDiv.style.opacity = "0";
  
  loading.style.display = "flex";
  loading.classList.remove("loading-out");
  
  // Force a reflow to ensure the display change is applied
  void loading.offsetWidth;
  
  // Apply styles that will trigger animations
  document.body.style.overflow = "hidden";
  loading.style.opacity = "1";
  loading.style.visibility = "visible";
}

function finished_load() {
  const loading = document.getElementById("loading");
  const contentDiv = document.getElementById("content-div");
  
  // Start the loading out animation
  loading.classList.add("loading-out");
  
  // Wait for the loading out animation to finish
  setTimeout(() => {
    loading.style.display = "none";
    document.body.style.overflow = "auto";
    
    // Start bringing in the content
    contentDiv.classList.add("content-in");
    contentDiv.style.opacity = "1";
  }, 500); // This matches your loading-out animation duration
}