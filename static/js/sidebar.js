// Toggles the mobile navbar menu open/closed.
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("navbar-toggle");
    const nav = document.getElementById("navbar-nav");

    if (!toggleBtn || !nav) return;

    toggleBtn.addEventListener("click", function () {
        const isOpen = nav.classList.toggle("is-open");
        toggleBtn.setAttribute("aria-expanded", isOpen);
    });
});