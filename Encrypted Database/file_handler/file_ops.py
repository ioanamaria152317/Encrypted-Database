"""
File Operations Module

This module handles reading and deleting encrypted files for a secure file management system.

"""

from database.db_handler import get_encrypted_file, delete_file_from_db
from encryption.rsa import decrypt_file
import os

def read_file(username: str, file_path: str, private_key_str: str) -> None:
    """
    Decrypts and displays the content of an encrypted file.

    Args:
        username (str): The username associated with the encrypted file.
        file_path (str): The path to the original file.
        private_key_str (str): The private key used for decryption in the format '(d, n)'.

    Returns:
        None
    """
    encrypted_file = get_encrypted_file(username, file_path)
    if not encrypted_file or not private_key_str:
        print("Encrypted file or private key not found!")
        return

    d, n = map(int, private_key_str.strip("() ").split(","))
    decrypted_output = "temp_decrypted.txt"

    decrypt_file(encrypted_file, decrypted_output, d, n)

    with open(decrypted_output, 'r') as f:
        content = f.read()
    os.remove(decrypted_output)
    print(f"\n Content of the decrypted file: \n{content}")

def delete_file(username: str, file_path: str) -> None:
    """
    Deletes an encrypted file from disk and removes its entry from the database.

    Args:
        username (str): The username associated with the encrypted file.
        file_path (str): The path to the original file.

    Returns:
        None
    """
    encrypted_file = get_encrypted_file(username, file_path)
    if not encrypted_file:
        print("The encrypted file was not found in the database!")
        return

    if os.path.exists(encrypted_file):
        os.remove(encrypted_file)
        print(f"File '{encrypted_file}' was removed.")
    else:
        print("This file doesn't exist.")

    delete_file_from_db(username, file_path)
    print("The information about this file was removed from the database.")
