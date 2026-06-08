(function () {
    const form = document.getElementById("assistantForm");
    const messages = document.getElementById("assistantMessages");
    const question = document.getElementById("assistantQuestion");
    const city = document.getElementById("assistantCity");
    const crop = document.getElementById("assistantCrop");
    const disease = document.getElementById("assistantDisease");

    function addMessage(text, type) {
        const bubble = document.createElement("div");
        bubble.className = `message ${type}`;
        bubble.textContent = text;
        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;
    }

    function buildFormBody(message) {
        const body = new URLSearchParams();
        body.set("message", message);
        body.set("city", city.value.trim());
        body.set("crop", crop.value.trim());
        body.set("disease", disease.value.trim());
        return body;
    }

    function buildJsonBody(message) {
        return {
            message,
            city: city.value.trim(),
            crop: crop.value.trim(),
            disease: disease.value.trim(),
        };
    }

    async function askFastApi(message) {
        const apiUrl = window.KRISHI_CHAT_API_URL || "http://127.0.0.1:8001/chat";
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(buildJsonBody(message)),
        });

        if (!response.ok) {
            throw new Error("FastAPI chat request failed");
        }

        return response.json();
    }

    async function askDjangoFallback(message) {
        const response = await fetch("/farmer-chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: buildFormBody(message),
        });

        if (!response.ok) {
            throw new Error("Django fallback chat request failed");
        }

        return response.json();
    }

    async function askAssistant(message) {
        try {
            return await askFastApi(message);
        } catch (error) {
            return askDjangoFallback(message);
        }
    }

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        const message = question.value.trim();
        if (!message) {
            return;
        }

        addMessage(message, "user");
        question.value = "";
        addMessage("Checking crop knowledge and weather...", "bot");
        const loadingBubble = messages.lastElementChild;

        try {
            const result = await askAssistant(message);
            const provider = result.provider ? `\n\nSource: ${result.provider}` : "";
            loadingBubble.textContent = `${result.answer || "I could not prepare an answer."}${provider}`;
        } catch (error) {
            loadingBubble.textContent = "I could not reach the assistant endpoint. Please try again.";
        }
    });
})();
