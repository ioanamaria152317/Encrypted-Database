import sqlite3
import os

DB_NAME = r'C:\Users\ioana\OneDrive\Desktop\Encrypted Database\database\encrypted_database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    public_key TEXT,
                    private_key TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    file_path TEXT,
                    encrypted_path TEXT,
                    key_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(key_id) REFERENCES keys(id))''')

    conn.commit()
    conn.close()

def add_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def save_keys(username, e, d, n):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]
    public_key = f"({e}, {n})"
    private_key = f"({d}, {n})"
    c.execute("INSERT INTO keys (user_id, public_key, private_key) VALUES (?, ?, ?)",
              (user_id, public_key, private_key))
    conn.commit()
    conn.close()
    
def save_file_info(username, original_path, encrypted_path, key_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]
    c.execute("INSERT INTO files (user_id, file_path, encrypted_path, key_id) VALUES (?, ?, ?, ?)",
              (user_id, original_path, encrypted_path, key_id))
    conn.commit()
    conn.close()


def get_public_key(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT public_key FROM keys INNER JOIN users ON keys.user_id = users.id WHERE users.username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None
    
    
def get_public_key_by_file(username, file_path):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("""
        SELECT keys.public_key
        FROM keys
        INNER JOIN files ON keys.id = files.key_id
        INNER JOIN users ON keys.user_id = users.id
        WHERE users.username = ? AND files.file_path = ?
    """, (username, file_path))
    
    result = c.fetchone()
    conn.close()
    
    if result:
        return result[0] 
    else:
        return None


def get_key_id_by_public_key(public_key_str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM keys WHERE public_key = ?", (public_key_str,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0] 
    else:
        return None
