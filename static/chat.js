const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const limitMessage = document.getElementById('limit-message');
const typingIndicator = document.getElementById('typing-indicator');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const modelSelector = document.getElementById('model');

// Avatars (use emoji or image URLs)
const userAvatar = "🧑";
const botAvatar = "🤖";

function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + sender;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.textContent = sender === 'user' ? userAvatar : botAvatar;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;

    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(bubble);

    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    userInput.value = '';
    typingIndicator.style.display = 'block';
    const formData = new FormData();
    formData.append('prompt', text);
    formData.append('model', modelSelector.value);
    const response = await fetch('/chat/send', {
        method: 'POST',
        body: formData
    });
    let data;
    try {
        data = await response.json();
    } catch (e) {
        const text = await response.text();
        addMessage("Error: " + text, 'bot');
        typingIndicator.style.display = 'none';
        return;
    }
    typingIndicator.style.display = 'none';
    if (data.error) {
        limitMessage.textContent = data.error;
        limitMessage.style.display = 'block';
        userInput.disabled = true;
        chatForm.querySelector('button').disabled = true;
    } else {
        addMessage(data.response, 'bot');
    }
});

// Dark mode toggle
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    darkModeToggle.textContent = document.body.classList.contains('dark-mode') ? "☀️" : "🌙";
});
