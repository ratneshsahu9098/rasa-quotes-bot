// Configuration
const rasaActionServerUrl = 'http://localhost:5005/webhooks/rest/webhook';
const senderId = "user_" + Math.random().toString(36).substring(7);

// DOM Elements
const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-button');
const quickReplies = document.querySelectorAll('.pill');

// Utility to scroll to bottom
const scrollToBottom = () => {
    chatWindow.scrollTop = chatWindow.scrollHeight;
};

// Render Message
const renderMessage = (text, sender) => {
    // Escape HTML to prevent XSS
    const safeText = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");

    // Convert newlines to breaks
    const formattedText = safeText.replace(/\n/g, '<br>');

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerHTML = `<div class="bubble">${formattedText}</div>`;

    // Remove typing indicator if exists
    const typingInd = document.getElementById('typing-indicator');
    if (typingInd) typingInd.remove();

    chatWindow.appendChild(msgDiv);
    scrollToBottom();
};

const renderTypingIndicator = () => {
    const msgDiv = document.createElement('div');
    msgDiv.id = 'typing-indicator';
    msgDiv.classList.add('message', 'bot');
    msgDiv.innerHTML = `<div class="bubble typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
    chatWindow.appendChild(msgDiv);
    scrollToBottom();
};

// Send message to Rasa Core server REST endpoint
const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Is it a payload (starts with /)?
    const isPayload = messageText.startsWith('/');

    // Render on screen (don't render payloads directly, render generic text if it's a payload shortcut)
    if (!isPayload) {
        renderMessage(messageText, 'user');
    }

    userInput.value = '';
    renderTypingIndicator();

    try {
        const response = await fetch(rasaActionServerUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender: senderId,
                message: messageText
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Wait a slight delay for realistic typing effect
        setTimeout(() => {
            if (data && data.length > 0) {
                // Remove typing indicator manually before adding real messages
                const typingInd = document.getElementById('typing-indicator');
                if (typingInd) typingInd.remove();

                data.forEach(msg => {
                    if (msg.text) {
                        renderMessage(msg.text, 'bot');
                    }
                });
            } else {
                renderMessage("Sorry, I could not understand or reach the server.", 'bot');
            }
        }, 600);

    } catch (error) {
        console.error("Error communicating with Rasa:", error);

        // Remove typing indicator
        const typingInd = document.getElementById('typing-indicator');
        if (typingInd) typingInd.remove();

        renderMessage("It seems the bot server is currently offline. Please ensure 'rasa run -m models --enable-api --cors \"*\"' is running.", 'bot');
    }
};

// Event Listeners
sendBtn.addEventListener('click', () => {
    sendMessage(userInput.value);
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage(userInput.value);
    }
});

// Quick Replies Handler
quickReplies.forEach(button => {
    button.addEventListener('click', () => {
        const payload = button.getAttribute('data-payload');
        const displayLabel = button.innerText;

        renderMessage(displayLabel, 'user');
        sendMessage(payload);
    });
});

// Modal Logic
const modal = document.getElementById('help-modal');
const helpBtn = document.getElementById('help-btn');
const closeBtn = document.getElementById('close-modal');

if (helpBtn && modal && closeBtn) {
    helpBtn.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}
