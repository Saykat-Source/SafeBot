import sqlite3
from passlib.context import CryptContext

DB_PATH = "biasguard_logs.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = "Saykat"  # Your admin username
new_password = "password321"  # Set your new password here

new_hash = pwd_context.hash(new_password)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('UPDATE users SET password_hash = ? WHERE username = ?', (new_hash, username))
conn.commit()
conn.close()
print(f"Password for user '{username}' has been reset!")
