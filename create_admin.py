import sqlite3
from passlib.context import CryptContext

DB_PATH = "biasguard_logs.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = "Saykat"  # Set your admin username
password = "password"  # Set your desired admin password

password_hash = pwd_context.hash(password)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)', (username, password_hash, 1))
conn.commit()
conn.close()
print(f"Admin user '{username}' created with admin rights!")
