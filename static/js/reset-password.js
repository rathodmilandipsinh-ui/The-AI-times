document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("resetForm");

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");

    const matchText = document.getElementById("matchText");

    // ==========================
    // Show / Hide Password
    // ==========================

    document.querySelectorAll(".toggle-password").forEach(button => {

        button.addEventListener("click", () => {

            const target = document.getElementById(button.dataset.target);
            const icon = button.querySelector("i");

            if (target.type === "password") {

                target.type = "text";

                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");

            } else {

                target.type = "password";

                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");

            }

        });

    });

    // ==========================
    // Password Match Check
    // ==========================

    function checkPasswordMatch() {

        const pass = password.value.trim();
        const confirm = confirmPassword.value.trim();

        if (confirm === "") {

            matchText.textContent = "";
            matchText.className = "";
            return;

        }

        if (pass === confirm) {

            matchText.textContent = "✓ Passwords match";
            matchText.className = "match";

        } else {

            matchText.textContent = "✗ Passwords do not match";
            matchText.className = "not-match";

        }

    }

    password.addEventListener("input", checkPasswordMatch);
    confirmPassword.addEventListener("input", checkPasswordMatch);

    // ==========================
    // Form Validation
    // ==========================

    form.addEventListener("submit", (e) => {

        const pass = password.value.trim();
        const confirm = confirmPassword.value.trim();

        if (pass.length < 8) {

            e.preventDefault();

            alert("Password must be at least 8 characters long.");

            password.focus();

            return;

        }

        if (pass !== confirm) {

            e.preventDefault();

            alert("Passwords do not match.");

            confirmPassword.focus();

            return;

        }

    });

});