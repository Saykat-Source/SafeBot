import { useState } from 'react';
import styles from '../styles/ChatArea.module.css';

export default function ChatArea() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: "Hi! How can I help you with your money today?" }
  ]);
  const [input, setInput] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((msgs) => [...msgs, { sender: 'user', text: input }]);

    try {
      const res = await fetch('http://localhost:8000/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      setMessages((msgs) => [...msgs, { sender: 'bot', text: data.reply || "No reply from AI." }]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', text: "Sorry, I couldn't connect to the server." }
      ]);
    }
    setInput('');
  };

  return (
    <section className={styles.chatSection}>
      <div className={styles.chatHistory}>
        {messages.map((msg, idx) =>
          msg.sender === 'user' ? (
            <div key={idx} className={styles.userBubble}>{msg.text}</div>
          ) : (
            <div key={idx} className={styles.botBubble}>{msg.text}</div>
          )
        )}
      </div>
      <form className={styles.inputBar} onSubmit={sendMessage}>
        <input
          className={styles.input}
          type="text"
          placeholder="Ask me anything about your money..."
          value={input}
          onChange={e => setInput(e.target.value)}
          style={{
            color: '#222',           // Makes text dark and visible
            background: '#fff',      // White background for contrast
            caretColor: '#222'       // Makes the cursor visible
          }}
        />
        <button
          className={styles.send}
          type="submit"
          title="Send"
          disabled={!input.trim()}
        >
          ➤
        </button>
      </form>
    </section>
  );
}
