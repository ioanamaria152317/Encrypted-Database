import argparse
import os
import getpass
from database.db_handler import init_db, add_user
from encryption.rsa import generate_keys, encrypt_file

def main():
    parser = argparse.ArgumentParser(description="RSA File Encryption Tool")
    subparsers = parser.add_subparsers(dest='command')

    gen_keys_parser = subparsers.add_parser('generate-keys', help="Generate RSA keys")

    encrypt_parser = subparsers.add_parser('encrypt', help="Encrypt a file")
    encrypt_parser.add_argument('file_path', type=str, help="Path to the file to encrypt")
    encrypt_parser.add_argument('public_key', type=str, help="Public key for encryption")

    args = parser.parse_args()
    username = getpass.getuser()

    init_db()
    add_user(username)

    if args.command == 'generate-keys':
        generate_keys(username)

    elif args.command == 'encrypt':
        encrypt_file(username, args.file_path, args.public_key)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
