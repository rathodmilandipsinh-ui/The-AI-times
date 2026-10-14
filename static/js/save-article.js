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

        const contentType =
            response.headers.get("content-type") || "";

        if (!contentType.includes("application/json")) {
            console.error(
                "Expected JSON but received:",
                await response.text()
            );

            showSaveFlash("Please log in to save articles.", "error");
            return;
        }

        const data = await response.json();

        if (response.status === 401 && data.login_required) {
            showSaveFlash("Please log in to save articles.", "error");
            return;
        }

        if (!response.ok || !data.success) {
            throw new Error(
                data.message || "Unable to update saved article."
            );
        }

        const icon = button.querySelector("img");

        // Use the actual state returned by Flask.
        const isSaved = data.saved;

        icon.src = isSaved
            ? button.dataset.savedIcon
            : button.dataset.unsavedIcon;

        button.classList.toggle("saved", isSaved);

        button.title = isSaved
            ? "Remove saved article"
            : "Save article";

        button.setAttribute(
            "aria-label",
            button.title
        );

        showSaveFlash(
            data.message || (isSaved
                ? "Article saved successfully."
                : "Article removed from saved articles."),
            "success"
        );

    } catch (error) {
        console.error("Save article error:", error);
        showSaveFlash(error.message || "Something went wrong.", "error");

    } finally {
        button.disabled = false;
    }
});


function showSaveFlash(message, type = "success") {
    // Remove an existing save notification.
    document.querySelectorAll(".save-flash-container")
        .forEach(element => element.remove());

    const container = document.createElement("div");
    container.className = "flash-con flash-container save-flash-container";

    const flash = document.createElement("div");
    flash.className = `flash flash-${type}`;

    const text = document.createElement("span");
    text.textContent = message;

    const close = document.createElement("button");
    close.type = "button";
    close.className = "flash-close";
    close.setAttribute("aria-label", "Close notification");
    close.textContent = "×";

    close.addEventListener("click", () => container.remove());

    flash.append(text, close);
    container.appendChild(flash);
    document.body.appendChild(container);

    setTimeout(() => container.remove(), 3000);
}