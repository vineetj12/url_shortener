// Toggle theme and persist in localStorage
function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");

    // Save the current theme to localStorage
    const currentTheme = document.body.classList.contains("dark-mode") ? "dark" : "light";
    localStorage.setItem("theme", currentTheme);
}

// Initialize theme on page load
function initializeTheme() {
    const savedTheme = localStorage.getItem("theme") || "light"; // Default to light if no theme is saved
    document.body.classList.add(savedTheme + "-mode");  // Apply the saved theme to the body
}

// Initialize the theme on page load
initializeTheme();
