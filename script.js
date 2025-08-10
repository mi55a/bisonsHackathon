document.getElementById("sendBtn").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});


async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const message = inputField.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, "user");
    inputField.value = "";

    try {
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        addMessage(data.reply, "ai");
    } catch (err) {
        console.error("Error talking to ProfAI:", err);
        addMessage("Can't connect to AI", "ai");
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById("chatMessages");
    const messageEl = document.createElement("div");
    messageEl.classList.add("message", sender);
    messageEl.textContent = text;
    chatMessages.appendChild(messageEl);

    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}