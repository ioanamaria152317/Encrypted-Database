"""
Database Handler Module

This module manages all database operations for user data, RSA keys, and encrypted file information.

"""

import sqlite3
import os

DB_NAME = r'C:\Users\ioana\OneDrive\Desktop\Encrypted Database\database\encrypted_database.db'

def init_db() -> None:
    """
    Initializes the SQLite database and creates necessary tables if they do not exist.

    Tables:
        - users: Stores user information.
        - keys: Stores RSA keys for each user.
        - files: Stores file paths and encryption details.

    Returns:
        None
    """
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

def add_user(username: str) -> None:
    """
    Adds a new user to the database if not already present.

    Args:
        username (str): Username to add to the database.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def save_keys(username: str, e: int, d: int, n: int) -> None:
    """
    Saves the generated RSA public and private keys for a user.

    Args:
        username (str): Username of the key owner.
        e (int): Public exponent.
        d (int): Private exponent.
        n (int): Modulus.

    Returns:
        None
    """
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

def save_file_info(username: str, original_path: str, encrypted_path: str, key_id: int) -> None:
    """
    Saves information about an encrypted file in the database.

    Args:
        username (str): Username of the file owner.
        original_path (str): Path to the original file.
        encrypted_path (str): Path to the encrypted file.
        key_id (int): ID of the key used for encryption.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]
    c.execute("INSERT INTO files (user_id, file_path, encrypted_path, key_id) VALUES (?, ?, ?, ?)",
              (user_id, original_path, encrypted_path, key_id))
    conn.commit()
    conn.close()

def get_public_key(username: str) -> str | None:
    """
    Retrieves the public key of a given user.

    Args:
        username (str): Username of the key owner.

    Returns:
        str | None: Public key if found, otherwise None.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT public_key FROM keys INNER JOIN users ON keys.user_id = users.id WHERE users.username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_public_key_by_file(username: str, file_path: str) -> str | None:
    """
    Retrieves the public key used to encrypt a specific file.

    Args:
        username (str): Username of the key owner.
        file_path (str): Path to the original file.

    Returns:
        str | None: Public key if found, otherwise None.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT keys.public_key FROM keys INNER JOIN files ON keys.id = files.key_id INNER JOIN users ON keys.user_id = users.id WHERE users.username = ? AND files.file_path = ?", (username, file_path))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_key_id_by_public_key(public_key_str: str) -> int | None:
    """
    Retrieves the key ID associated with a given public key.

    Args:
        public_key_str (str): The public key in string format.

    Returns:
        int | None: Key ID if found, otherwise None.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM keys WHERE public_key = ?", (public_key_str,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def list_all_files(username: str) -> None:
    """
    Lists all encrypted files associated with a user.

    Args:
        username (str): Username to list files for.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT encrypted_path, timestamp FROM files INNER JOIN users ON files.user_id = users.id WHERE users.username = ?", (username,))
    files = c.fetchall()
    conn.close()
    if files:
        print("Encrypted files:")
        for file in files:
            encrypted_file_name = os.path.basename(file[0])
            print(f"{encrypted_file_name} | {file[1]}")
    else:
        print("There are no encrypted files!")


def get_encrypted_file(username: str, file_path: str) -> str | None:
    """
    Retrieves the encrypted file path for a given user and file.

    Args:
        username (str): Username of the file owner.
        file_path (str): Path to the original file.

    Returns:
        str | None: Path to the encrypted file if found, otherwise None.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT encrypted_path FROM files INNER JOIN users ON files.user_id = users.id WHERE users.username = ? AND files.file_path = ?", (username, file_path))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def delete_file_from_db(username: str, file_path: str) -> None:
    """
    Deletes the record of a file from the database for a specific user.

    Args:
        username (str): Username of the file owner.
        file_path (str): Path to the original file.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM files WHERE user_id = (SELECT id FROM users WHERE username = ?) AND file_path = ?", (username, file_path))
    conn.commit()
    conn.close()
