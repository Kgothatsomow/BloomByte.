import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_user_table():
    conn = sqlite3.connect('bloombyte.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_feedback_table():
    conn = sqlite3.connect('bloombyte.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_feedback(message):
    conn = sqlite3.connect('bloombyte.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()