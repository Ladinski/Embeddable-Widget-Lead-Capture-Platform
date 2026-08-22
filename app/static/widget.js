(function () {
    const script = document.currentScript;

    if (!script) {
        return;
    }

    const scriptUrl = new URL(script.src);
    const widgetId = scriptUrl.searchParams.get("id");

    if (!widgetId) {
        console.error("Widget ID is missing");
        return;
    }

    const apiBaseUrl = scriptUrl.origin;

    async function loadWidget() {
        try {
            const response = await fetch(
                `${apiBaseUrl}/public/widgets/${widgetId}/config`
            );

            if (!response.ok) {
                throw new Error("Failed to load widget configuration");
            }

            const config = await response.json();

            renderWidget(config);
        } catch (error) {
            console.error("Widget failed to load:", error);
        }
    }

    function renderWidget(config) {
        const container = document.createElement("div");

        const title = document.createElement("h3");
        title.textContent = config.title;
        container.appendChild(title);

        if (config.description) {
            const description = document.createElement("p");
            description.textContent = config.description;
            container.appendChild(description);
        }

        const form = document.createElement("form");

        const honeypot = document.createElement("input");
        honeypot.type = "text";
        honeypot.name = "form_check";
        honeypot.value = "";
        honeypot.tabIndex = -1;
        honeypot.autocomplete = "new-password";
        honeypot.setAttribute("aria-hidden", "true");
        honeypot.style.position = "absolute";
        honeypot.style.left = "-9999px";
        honeypot.style.width = "1px";
        honeypot.style.height = "1px";

        form.appendChild(honeypot);

        config.fields.forEach((field) => {
            const wrapper = document.createElement("div");

            const label = document.createElement("label");
            label.textContent = field.name;

            const input = document.createElement("input");
            input.name = field.name;
            input.type = field.type === "email" ? "email" : "text";
            input.required = field.required;

            wrapper.appendChild(label);
            wrapper.appendChild(input);
            form.appendChild(wrapper);
        });

        const button = document.createElement("button");
        button.type = "submit";
        button.textContent = config.button_text;

        form.appendChild(button);

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const rawFormData = Object.fromEntries(
                new FormData(form)
            );

            const honeypotValue = rawFormData.form_check || "";
            delete rawFormData.form_check;

            try {
                const response = await fetch(
                    `${apiBaseUrl}/public/widgets/${widgetId}/submissions`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            data: rawFormData,
                            form_check: honeypotValue,
                        }),
                    }
                );

                if (!response.ok) {
                    const error = await response.json();

                    throw new Error(
                        error.detail || "Submission failed"
                    );
                }

                form.reset();

                const oldMessage = form.querySelector(
                    "[data-widget-message]"
                );

                if (oldMessage) {
                    oldMessage.remove();
                }

                const success = document.createElement("p");
                success.dataset.widgetMessage = "true";
                success.textContent = "Submitted successfully.";

                form.appendChild(success);
            } catch (error) {
                console.error("Submission failed:", error);
            }
        });

        container.appendChild(form);

        script.insertAdjacentElement("afterend", container);
    }

    loadWidget();
})();