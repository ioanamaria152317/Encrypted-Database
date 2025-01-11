"""
Main Entry Point for RSA File Encryption Tool

This script handles command-line interactions for generating keys, encrypting, decrypting, deleting, and listing files.

"""

import argparse
import os
import getpass
from database.db_handler import init_db, add_user, list_all_files
from encryption.rsa import generate_keys, encrypt_file
from file_handler.file_ops import read_file, delete_file

def main() -> None:
    """
    Entry point for the RSA File Encryption Tool.
    Handles commands for key generation, encryption, decryption, deletion, and listing files.

    Args:
        None

    Returns:
        None
    """
    #creating a parser for arguments 
    #description appears when --help command is used 
    parser = argparse.ArgumentParser(description="RSA File Encryption Tool")
    
    #subcommands, as git clone 
    subparsers = parser.add_subparsers(dest='command')

    gen_keys_parser = subparsers.add_parser('generate-keys', help="Generate RSA keys")

    encrypt_parser = subparsers.add_parser('encrypt', help="Encrypt a file")
    encrypt_parser.add_argument('file_path', type=str, help="Path to the file to encrypt")
    encrypt_parser.add_argument('public_key', type=str, help="Public key for encryption")

    read_parser = subparsers.add_parser('read', help="Read and decrypt a file")
    read_parser.add_argument('file_path', type=str, help="Path to the encrypted file")
    read_parser.add_argument('private_key', type=str, help="Private key for decryption")

    delete_parser = subparsers.add_parser('delete', help="Delete a file")
    delete_parser.add_argument('file_path', type=str, help="Path to the file to delete")

    list_parser = subparsers.add_parser('list', help="List all encrypted files")

    args = parser.parse_args()
    username = getpass.getuser()

    init_db()
    add_user(username)

    if args.command == 'generate-keys':
        generate_keys(username)

    elif args.command == 'encrypt':
        encrypt_file(username, args.file_path, args.public_key)

    elif args.command == 'read':
        read_file(username, args.file_path, args.private_key)

    elif args.command == 'delete':
        delete_file(username, args.file_path)

    elif args.command == 'list':
        list_all_files(username)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
