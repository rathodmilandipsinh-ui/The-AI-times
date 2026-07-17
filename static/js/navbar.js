// Toggles the mobile navbar menu open/closed.
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("navbar-toggle");
    const nav = document.getElementById("navbar-nav");

    if (!toggleBtn || !nav) return;

    toggleBtn.addEventListener("click", function () {
        const isOpen = nav.classList.toggle("is-open");
        toggleBtn.setAttribute("aria-expanded", isOpen);
    });





    document.querySelectorAll(".flash").forEach(alert => {

        const close = alert.querySelector(".flash-close");

        close.addEventListener("click", () => {

            alert.remove();

        });

        setTimeout(() => {

            alert.style.opacity = "0";
            alert.style.transform = "translateX(100%)";

            setTimeout(() => {

                alert.remove();

            }, 300);

        }, 5000);

    });

});