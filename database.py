
import sqlite3
import os

def init_db():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(username, date, category, description, amount):
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (username, date, category, description, amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, date, category, description, amount))
    conn.commit()
    conn.close()

def get_transactions(username):
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, category, description, amount FROM transactions
        WHERE username = ?
        ORDER BY date DESC
    ''', (username,))
    data = c.fetchall()
    conn.close()
    return data
