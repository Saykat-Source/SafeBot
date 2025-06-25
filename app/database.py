import sqlite3
from datetime import datetime

DB_PATH = "biasguard_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    # Logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            prompt TEXT,
            response TEXT,
            issues TEXT,
            model TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(prompt, response, issues, model, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs (timestamp, prompt, response, issues, model, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        prompt,
        response,
        "; ".join(issues) if isinstance(issues, list) else str(issues),
        model,
        user_id
    ))
    conn.commit()
    conn.close()

def get_user_message_count_today(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().date().isoformat()
    c.execute('''
        SELECT COUNT(*) FROM logs
        WHERE user_id = ? AND DATE(timestamp) = ?
    ''', (user_id, today))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT logs.timestamp, users.username, logs.prompt, logs.response, logs.issues, logs.model
        FROM logs
        LEFT JOIN users ON logs.user_id = users.id
        ORDER BY logs.timestamp DESC
    ''')
    logs = c.fetchall()
    conn.close()
    return logs

def get_user_count():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    conn.close()
    return count

def create_user(username, password_hash, is_admin=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)', (username, password_hash, is_admin))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, password_hash, is_admin FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user
