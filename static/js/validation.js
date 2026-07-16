
document.addEventListener("DOMContentLoaded", () => {

    const forms = document.querySelectorAll(".auth-form");

    forms.forEach(form => {

        form.addEventListener("submit", event => {

            if (!validateForm(form)) {
                event.preventDefault();
            }

        });

    });

    function validateForm(form) {

        let isValid = true;

        const requiredFields = form.querySelectorAll("[required]");

        requiredFields.forEach(field => {

            clearError(field);

            const value = field.value.trim();

            if (value === "") {
                showError(field, "This field is required.");
                isValid = false;
                return;
            }

            if (field.type === "email") {

                if (!isValidEmail(value)) {
                    showError(field, "Please enter a valid email address.");
                    isValid = false;
                }

            }

        });

        const password = form.querySelector("#password");
        const confirmPassword = form.querySelector("#confirm-password");

        if (password && confirmPassword) {

            clearError(password);
            clearError(confirmPassword);

            if (password.value.length < 8) {

                showError(password, "Password must be at least 8 characters.");
                isValid = false;

            }

            if (password.value !== confirmPassword.value) {

                showError(confirmPassword, "Passwords do not match.");
                isValid = false;

            }

        }

        return isValid;

    }

    function isValidEmail(email) {

        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        return pattern.test(email);

    }

    function showError(input, message) {

        input.classList.add("error");

        const existingError = input.parentElement.querySelector(".error-message");

        if (existingError) {
            existingError.remove();
        }

        const error = document.createElement("small");

        error.className = "error-message";
        error.textContent = message;

        input.parentElement.appendChild(error);

    }

    function clearError(input) {

        input.classList.remove("error");

        const error = input.parentElement.querySelector(".error-message");

        if (error) {
            error.remove();
        }

    }

});
