from auth import hash_password, verify_password, create_token, decode_token

pw = "mypassword"
hashed = hash_password(pw)

print(verify_password(pw, hashed))

token = create_token(1)
print(decode_token(token))
