import sqlite3
from datetime import datetime

DB_PATH = "biasguard_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            prompt TEXT,
            response TEXT,
            issues TEXT,
            model TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(prompt, response, issues, model):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs (timestamp, prompt, response, issues, model)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), prompt, response, "; ".join(issues), model))
    conn.commit()
    conn.close()
