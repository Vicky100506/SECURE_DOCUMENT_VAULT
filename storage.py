import hashlib
import os
from crypto import encrypt, decrypt

STORAGE_DIR = "storage/encrypted"

os.makedirs(STORAGE_DIR, exist_ok=True)

def save_file(file_bytes: bytes):
    # Create file hash (integrity check)
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Encrypt file
    encrypted_data = encrypt(file_bytes)

    # Save encrypted file
    path = os.path.join(STORAGE_DIR, f"{file_hash}.enc")
    with open(path, "wb") as f:
        f.write(encrypted_data)

    return path, file_hash

def load_file(path: str):
    with open(path, "rb") as f:
        encrypted_data = f.read()

    return decrypt(encrypted_data)
