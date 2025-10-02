async function sendMessage() {
    const input = document.getElementById('user-input');
    const messagesDiv = document.getElementById('chat-messages');
    const message = input.value.trim();
    if (!message) return;

    // Display user message
    messagesDiv.innerHTML += `<p class="user-message"><strong>You:</strong> ${message}</p>`;
    input.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        messagesDiv.innerHTML += `<p class="bot-message"><strong>Bot:</strong> ${data.response}</p>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        messagesDiv.innerHTML += `<p class="bot-message"><strong>Bot:</strong> Error: Unable to connect.</p>`;
        console.error('Error:', error);
    }
}

// Allow sending message with Enter key
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});