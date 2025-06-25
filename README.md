# SafeBot – Personal Finance & Life Coach Chatbot

SafeBot is an AI-powered personal finance and lifestyle coach designed for Australians. It helps users manage their weekly budgets, track expenses (including Google Pay, Apple Pay, and credit cards), and get personalized, motivational advice for daily life—all through a friendly chat interface.

---

## ✨ Features

- **Conversational AI:** Proactive, supportive, and sometimes strict advice tailored to your lifestyle and spending habits.
- **No-Code Prompt Editor:** Easily update the bot’s personality and instructions from a web admin UI—no coding required!
- **Expense Tracking:** Log expenses by category and payment method (Google Pay, Apple Pay, Credit Card, etc.).
- **Budget Management:** Set and update your weekly budgets for meals, travel, clothes, and more.
- **Modern Responsive UI:** Built with React (Vite) for a smooth experience on any device.
- **FastAPI Backend:** Secure, scalable backend with OpenAI GPT-4/4o integration.

---

## 🚀 Screenshots

*(Add screenshots of your UI and prompt editor here!)*

---

## 🛠️ Getting Started

### Prerequisites

- Node.js & npm
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Saykat-Source/SafeBot.git
   cd SafeBot

   2.Backend setup:
bash
Copy Code
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3.Frontend setup:
bash
Copy Code
cd ../frontend
npm install
Start the servers:
Backend:
bash
Copy Code
uvicorn main:app --reload
Frontend:
bash
Copy Code
npm run dev
💡 Usage
Visit http://localhost:5173/ for the main app.
Visit http://localhost:5173/admin to edit the chatbot’s prompt (admin only).
🧰 Tech Stack
Frontend: React (Vite)
Backend: FastAPI (Python)
AI: OpenAI GPT-4/4o
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

📄 License
MIT

📬 Contact
Saykat Ghosh – [saykatkumar97@gmail.com]
