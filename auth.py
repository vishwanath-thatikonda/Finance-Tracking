
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    if c.fetchone():
        conn.close()
        return False
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
              (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def authenticate_user(username, password):
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False
