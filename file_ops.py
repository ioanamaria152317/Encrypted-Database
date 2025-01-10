from database.db_handler import get_encrypted_file, delete_file_from_db
from encryption.rsa import decrypt_file
import os

def read_file(username, file_path, private_key_str):
    encrypted_file = get_encrypted_file(username, file_path)
    if not encrypted_file or not private_key_str:
        print("Fisierul criptat sau cheia privata nu au fost gasite.")
        return

    d, n = map(int, private_key_str.strip("() ").split(","))
    decrypted_output = "temp_decrypted.txt"

    decrypt_file(encrypted_file, decrypted_output, d, n)

    with open(decrypted_output, 'r') as f:
        content = f.read()
    os.remove(decrypted_output) 
    print(f"\n Continutul fisierului decriptat:\n{content}")


def delete_file(username, file_path):
    encrypted_file = get_encrypted_file(username, file_path)
    if not encrypted_file:
        print("Fisierul criptat nu a fost gasit in baza de date.")
        return

    if os.path.exists(encrypted_file):
        os.remove(encrypted_file)
        print(f"Fisierul '{encrypted_file}' a fost sters de pe disc.")
    else:
        print("Fisierul nu exista pe disc.")
    
    delete_file_from_db(username, file_path)

