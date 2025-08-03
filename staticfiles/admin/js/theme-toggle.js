document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const sidebar = document.getElementById("content-related");
    const tables = document.querySelectorAll(".dashboard-table, .result-list");

    // Check local storage for theme preference
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        sidebar.classList.add("dark-mode");
        tables.forEach(table => table.classList.add("dark-mode"));
        themeToggle.textContent = "☀️ Light Mode";
    }

    // Toggle theme on button click
    themeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        sidebar.classList.toggle("dark-mode");
        tables.forEach(table => table.classList.toggle("dark-mode"));

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            themeToggle.textContent = "☀️ Light Mode";
        } else {
            localStorage.setItem("theme", "light");
            themeToggle.textContent = "🌙 Dark Mode";
        }
    });
});
