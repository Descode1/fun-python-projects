import os
import json
import base64
import getpass
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import sys
import pyperclip

VAULT_FILE = "vault.json"
SALT_FILE = "salt.bin"
ITERATIONS = 100000

#generates a random 18 character password 
def get_password():
    NUMS = "0123456789"
    LOWER = "abcdefghijklmnopqrstuvwxyz"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SYMBOLS = "~!@#$%^&*()_-+=}{:;><.,/?"
    CHAR_SETS = [NUMS, LOWER, UPPER, SYMBOLS]

    password = ""
    for _ in range(18):
        char_set = random.choice(CHAR_SETS)
        password += random.choice(char_set)
    return password
#returns the salt if the salt.bin file exists else creates a random 16 bytes write it to the salt.bin file
def ensure_salt():
    if os.path.exists(SALT_FILE):
        return open(SALT_FILE, "rb").read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    os.system(f'attrib +h "{SALT_FILE}"')
    return salt
#returns a fernet object
def get_fernet(master_password):
    salt = ensure_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)

#returns encrypted data whick is then decrypted using the fernet key
def load_vault(fernet):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()
    os.system(f'attrib +h "{VAULT_FILE}"')
    if not encrypted_data:
        return {}
    try:
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    except:
        print("Wrong master password or corrupted vault.")
        return None
    
#saves encrypted data 
def save_vault(vault, fernet):
    data = json.dumps(vault).encode()
    encrypted = fernet.encrypt(data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
    
#generates a password and adds to the vault while keeping existing entries
def add_entry(account_name, fernet):
    vault = load_vault(fernet)
    if vault is None:
        return
    pw = get_password()
    vault[account_name] = pw
    pyperclip.copy(pw)
    save_vault(vault, fernet)
    print(f"Added {account_name}.")
    print("Password copied to clipboard.")
#removes entries
def remove_entry(account_name, fernet):
    vault = load_vault(fernet)
    if vault is None:
        return
    if account_name in vault:
        del vault[account_name]
        save_vault(vault, fernet)
        print(f"Removed {account_name}")
    else:
        print(f"{account_name} not found.")
#lists all entries
def list_entries(fernet):
    vault = load_vault(fernet)
    if vault is None:
        return
    if vault:
        for k in vault.keys():
            print(k)
    else:
        print("Vault is empty.")
#reveals password and copies it to clipboard
def show_entry(account_name, fernet):
    vault = load_vault(fernet)
    if vault is None:
        return
    if account_name in vault:
        print(vault[account_name])
        pyperclip.copy(vault[account_name])
        print("Password copied to clipboard.")
    else:
        print(f"{account_name} not found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python vault.py <command> [account_name]")
        print("Commands: add, remove, list, show")
        return

    command = sys.argv[1].lower()
    account_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    #uses getpass to safely get user password without showing what's typed on the screen
    master_password = getpass.getpass("Enter master password: ")
    fernet = get_fernet(master_password)
    
    if command == "add":
        if not account_name:
            print("Please provide an account name.")
            return
        add_entry(account_name, fernet)
    elif command == "remove":
        if not account_name:
            print("Please provide an account name.")
            return
        remove_entry(account_name, fernet)
    elif command == "list":
        list_entries(fernet)
    elif command == "show":
        if not account_name:
            print("Please provide an account name.")
            return
        show_entry(account_name, fernet)
    else:
        print("Unknown command. Available commands: add, remove, list, show")

if __name__ == "__main__":
    main()




