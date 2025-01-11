"""
RSA Encryption and Decryption Module

This module handles RSA key generation, file encryption, and decryption for secure file storage.

"""

import os
from database.db_handler import save_keys, save_file_info, get_key_id_by_public_key

def modInverse(e: int, phi: int) -> int:
    """
    Calculate the modular inverse of e modulo phi.

    Args:
        e (int): Public exponent.
        phi (int): Euler's Totient function of n.

    Returns:
        int: The modular inverse of e modulo phi.
    """
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1

def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor (GCD) of two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: GCD of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a

def generate_keys(username: str) -> None:
    """
    Generate RSA public and private keys and save them in the database.

    Args:
        username (str): Username for whom the keys are generated.

    Returns:
        None
    """
    p = 7919
    q = 1009
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break
    d = modInverse(e, phi)
    save_keys(username, e, d, n)
    print(f"Keys generated for user {username}:\nPublic Key (e, n): ({e}, {n})\nPrivate Key (d, n): ({d}, {n})")

def encrypt_block(block: int, e: int, n: int) -> int:
    """
    Encrypt a single data block using RSA encryption.

    Args:
        block (int): Data block to encrypt.
        e (int): Public exponent.
        n (int): Modulus.

    Returns:
        int: Encrypted data block.
    """
    return pow(block, e, n)

def decrypt_block(block: int, d: int, n: int) -> int:
    """
    Decrypt a single data block using RSA decryption.

    Args:
        block (int): Encrypted data block.
        d (int): Private exponent.
        n (int): Modulus.

    Returns:
        int: Decrypted data block.
    """
    return pow(block, d, n)

def encrypt_file(username: str, input_file: str, public_key_str: str) -> None:
    """
    Encrypt a file using the RSA algorithm.

    Args:
        username (str): Username of the file owner.
        input_file (str): Path to the file to encrypt.
        public_key_str (str): Public key in string format.

    Returns:
        None
    """
    e, n = map(int, public_key_str.strip("() ").split(","))
    encrypted_dir = r'C:\Users\ioana\OneDrive\Desktop\Encrypted Database\encrypted_files'
    
    output_file = os.path.join(encrypted_dir, os.path.basename(input_file) + '.enc')

    block_size = (n.bit_length() - 1) // 8
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(block_size):
            block = int.from_bytes(chunk, byteorder='big')
            encrypted_block = encrypt_block(block, e, n)
            f_out.write(encrypted_block.to_bytes((n.bit_length() + 7) // 8, byteorder='big'))
    
    key_id = get_key_id_by_public_key(public_key_str)
    save_file_info(username, input_file, output_file, key_id)
    print(f"File '{os.path.basename(input_file)}' encrypted and saved as '{os.path.basename(output_file)}'")

def decrypt_file(input_file: str, output_file: str, d: int, n: int) -> None:
    """
    Decrypt a file using the RSA algorithm.

    Args:
        input_file (str): Path to the encrypted file.
        output_file (str): Path to save the decrypted file.
        d (int): Private exponent.
        n (int): Modulus.

    Returns:
        None
    """
    block_size = (n.bit_length() + 7) // 8
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(block_size):
            block = int.from_bytes(chunk, byteorder='big')
            decrypted_block = decrypt_block(block, d, n)
            f_out.write(decrypted_block.to_bytes((block.bit_length() + 7) // 8, byteorder='big').rstrip(b'\x00'))
