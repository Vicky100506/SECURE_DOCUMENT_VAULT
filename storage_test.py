from storage import save_file, load_file

data = b"my secret document"

path, file_hash = save_file(data)
print("Saved at:", path)

original = load_file(path)
print("Recovered:", original)
