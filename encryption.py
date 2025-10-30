import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("key.key", "wb") as f:
    f.write(key)

key = open("key.key", "rb").read()
fernet = Fernet(key)

data = {
    "gmail": "myGmailPassword123!",
    "github": "myGithubPassword456#"
}

json_bytes = json.dumps(data).encode()
encrypted = fernet.encrypt(json_bytes)

with open("vault.json", "wb") as f:
    f.write(encrypted)

print("Encrypted vault.json created!")

with open("vault.json", "rb") as f:
    encrypted_data = f.read()
decrypted_bytes = fernet.decrypt(encrypted_data)
decrypted_data = json.loads(decrypted_bytes.decode())

print("Descrypted data: ", decrypted_bytes)