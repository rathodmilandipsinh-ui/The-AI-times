
document.addEventListener("click", async function (event) {
    const button = event.target.closest(".save-article-btn");

    if (!button || button.disabled) return;

    button.disabled = true;

    try {
        const response = await fetch(button.dataset.saveUrl, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const contentType = response.headers.get("content-type") || "";

        if (!contentType.includes("application/json")) {
            console.error("Expected JSON but received:", await response.text());
            const newdiv = document.createElement('div')
            newdiv.classList = "flash-con flash-container"
            newdiv.innerHTML = `
        <div class="flash flash-error">
            <span>Please log in to save articles.</span>
            <button class="flash-close">&times;</button>
        </div>`
            document.body.appendChild(newdiv)
            setTimeout(() => {
                document.querySelector(".flash-con").remove()
            }, 3000);
            // alert("Your session may have expired. Please log in to save articles.");

            return;
        }

        const data = await response.json();

        if (response.status === 401 && data.login_required) {
            alert("Login is required to save articles.");
            return;
        }

        if (!response.ok || !data.success) {
            throw new Error(data.message || "Unable to save article.");
        }

        button.classList.add("saved");
        button.title = "Article saved";

    } catch (error) {
        console.error("Save article error:", error);
        alert(error.message || "Something went wrong.");
    } finally {
        button.disabled = false;
    }
});