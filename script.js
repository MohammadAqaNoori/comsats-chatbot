function formatTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function autoResizeTextarea() {
    const textarea = document.getElementById("userInput");
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 80)}px`;
}

function scrollToBottom() {
    const chatBody = document.getElementById("chatBody");
    chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: "smooth"
    });
}

async function typeMessage(element, text) {
    element.classList.add("typing");
    const words = text.split(" ");
    element.textContent = "";
    for (let i = 0; i < words.length; i++) {
        element.textContent += words[i] + " ";
        await new Promise(resolve => setTimeout(resolve, 35));
    }
    element.classList.remove("typing");
}

async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatBody = document.getElementById("chatBody");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const message = userInput.value.trim();

    if (!message) return;

    // Display user message (aligned right)
    const userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerHTML = `
        <div class="message-content">${message}</div>
        <span class="timestamp">${formatTimestamp()}</span>
    `;
    chatBody.appendChild(userMessage);

    // Clear input and reset height
    userInput.value = "";
    autoResizeTextarea();
    loadingIndicator.style.display = "flex";
    scrollToBottom();

    // Send message to backend
    try {
        const response = await fetch("http://localhost:5000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        // Display bot response (aligned left) with typing effect
        const botMessage = document.createElement("div");
        botMessage.className = "message bot-message";
        botMessage.innerHTML = `
            <div class="message-content"></div>
            <span class="timestamp">${formatTimestamp()}</span>
        `;
        chatBody.appendChild(botMessage);
        await typeMessage(botMessage.querySelector(".message-content"), data.response || data.error);
        scrollToBottom();
    } catch (error) {
        console.error("Error:", error);
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot-message";
        errorMessage.innerHTML = `
            <div class="message-content"></div>
            <span class="timestamp">${formatTimestamp()}</span>
        `;
        chatBody.appendChild(errorMessage);
        await typeMessage(errorMessage.querySelector(".message-content"), "Sorry, something went wrong. Please try again.");
        scrollToBottom();
    } finally {
        loadingIndicator.style.display = "none";
    }
}

// Initialize timestamp for initial message
document.querySelector(".bot-message .timestamp").textContent = formatTimestamp();

// Auto-resize textarea on input
document.getElementById("userInput").addEventListener("input", autoResizeTextarea);

// Send message on Enter (without Shift)
document.getElementById("userInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize textarea height and scroll to bottom
autoResizeTextarea();
scrollToBottom();