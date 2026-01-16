from crypto import encrypt, decrypt

msg = b"secure document vault"
encrypted = encrypt(msg)
decrypted = decrypt(encrypted)

print(decrypted)
