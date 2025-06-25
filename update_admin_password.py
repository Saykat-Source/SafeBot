# update_admin_password.py
from app.database import get_user_by_username
import sqlite3
from passlib.context import CryptContext

DB_PATH = "biasguard_logs.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = "admin"  # Change if your admin username is different
new_password = "Chatbot"  # Set your new password here
new_hash = pwd_context.hash(new_password)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('UPDATE users SET password_hash = ?, is_admin = 1 WHERE username = ?', (new_hash, username))
conn.commit()
conn.close()
print("Admin password updated!")
