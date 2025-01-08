// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const formWrapper = document.getElementById("form-wrapper");
  const resultText = document.getElementById("result-text");

  // Hide form dynamically if result exists
  if (resultText) {
    formWrapper.style.display = "none";
  }
});
