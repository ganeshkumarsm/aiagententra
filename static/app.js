const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("msg");
const sendButton = document.getElementById("send-button");
const statusPill = document.getElementById("status-pill");

function appendMessage(role, content) {
    const article = document.createElement("article");
    article.className = `message ${role}`;

    const roleLabel = document.createElement("div");
    roleLabel.className = "message-role";
    roleLabel.textContent = role === "user" ? "You" : "Assistant";

    const text = document.createElement("p");
    text.textContent = content;

    article.append(roleLabel, text);
    chat.appendChild(article);
    chat.scrollTop = chat.scrollHeight;
}

function setBusyState(isBusy) {
    sendButton.disabled = isBusy;
    messageInput.disabled = isBusy;
    statusPill.textContent = isBusy ? "Working" : "Ready";
}

async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        messageInput.focus();
        return;
    }

    appendMessage("user", message);
    messageInput.value = "";
    setBusyState(true);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();
        appendMessage("assistant", data.response || "No response received.");
    } catch (error) {
        appendMessage("assistant", "The assistant could not respond right now. Please try again.");
    } finally {
        setBusyState(false);
        messageInput.focus();
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    await sendMessage();
});

messageInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        await sendMessage();
    }
});
