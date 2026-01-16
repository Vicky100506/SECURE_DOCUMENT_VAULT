from database import get_db

db = get_db()
print("Connected to MySQL successfully!")
db.close()
