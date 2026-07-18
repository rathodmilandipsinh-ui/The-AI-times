document.addEventListener("DOMContentLoaded", () => {

    const otpBoxes = document.querySelectorAll(".otp-box");
    const otpInput = document.getElementById("otp");
    const form = document.querySelector("form");

    // Allow only numbers
    otpBoxes.forEach((box, index) => {

        box.addEventListener("input", (e) => {

            let value = e.target.value.replace(/\D/g, "");

            e.target.value = value;

            if (value && index < otpBoxes.length - 1) {
                otpBoxes[index + 1].focus();
            }

        });

        box.addEventListener("keydown", (e) => {

            // Move back on Backspace
            if (e.key === "Backspace" && box.value === "" && index > 0) {
                otpBoxes[index - 1].focus();
            }

            // Arrow navigation
            if (e.key === "ArrowLeft" && index > 0) {
                otpBoxes[index - 1].focus();
            }

            if (e.key === "ArrowRight" && index < otpBoxes.length - 1) {
                otpBoxes[index + 1].focus();
            }

        });

    });

    // Paste OTP
    otpBoxes[0].addEventListener("paste", (e) => {

        e.preventDefault();

        const pasted = e.clipboardData
            .getData("text")
            .replace(/\D/g, "")
            .slice(0, otpBoxes.length);

        pasted.split("").forEach((digit, index) => {
            otpBoxes[index].value = digit;
        });

        if (pasted.length > 0) {
            otpBoxes[Math.min(pasted.length - 1, otpBoxes.length - 1)].focus();
        }

    });

    // Before submit
    form.addEventListener("submit", (e) => {

        let otp = "";

        otpBoxes.forEach(box => {
            otp += box.value;
        });

        if (otp.length !== otpBoxes.length) {
            e.preventDefault();
            alert("Please enter the complete OTP.");
            return;
        }

        otpInput.value = otp;

    });

});