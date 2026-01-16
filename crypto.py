from cryptography.fernet import Fernet
import os

# Generate or load encryption key
KEY_FILE = "vault.key"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)

def encrypt(data: bytes) -> bytes:
    return cipher.encrypt(data)

def decrypt(data: bytes) -> bytes:
    return cipher.decrypt(data)
