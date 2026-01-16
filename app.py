from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from database import get_db
from auth import hash_password, verify_password, create_token, decode_token
from storage import save_file, load_file
import io

app = FastAPI(docs_url=None, redoc_url=None)

# Serve UI
@app.get("/", response_class=HTMLResponse)
def ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Register
@app.post("/register")
def register(username: str, password: str):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s,%s)",
            (username, hash_password(password))
        )
        db.commit()
    except:
        raise HTTPException(400, "User already exists")
    finally:
        cur.close()
        db.close()
    return {"message": "User registered"}

# Login
@app.post("/login")
def login(username: str, password: str):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, password_hash FROM users WHERE username=%s",
        (username,)
    )
    user = cur.fetchone()
    cur.close()
    db.close()

    if not user or not verify_password(password, user[1]):
        raise HTTPException(401, "Invalid credentials")

    return {"token": create_token(user[0])}

# Upload
@app.post("/upload")
def upload(file: UploadFile = File(...), token: str = Header(...)):
    payload = decode_token(token)
    user_id = payload["user_id"]

    data = file.file.read()
    path, file_hash = save_file(data)

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO documents (user_id, filename, encrypted_path, file_hash) VALUES (%s,%s,%s,%s)",
        (user_id, file.filename, path, file_hash)
    )
    db.commit()
    cur.close()
    db.close()

    return {"message": "File uploaded"}

# List files
@app.get("/files")
def files(token: str = Header(...)):
    payload = decode_token(token)
    user_id = payload["user_id"]

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, filename FROM documents WHERE user_id=%s",
        (user_id,)
    )
    files = cur.fetchall()
    cur.close()
    db.close()

    return [{"id": f[0], "name": f[1]} for f in files]

# Download
@app.get("/download/{doc_id}")
def download(doc_id: int, token: str = Header(...)):
    payload = decode_token(token)
    user_id = payload["user_id"]

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT encrypted_path, filename FROM documents WHERE id=%s AND user_id=%s",
        (doc_id, user_id)
    )
    row = cur.fetchone()
    cur.close()
    db.close()

    if not row:
        raise HTTPException(403, "Access denied")

    data = load_file(row[0])
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={row[1]}"}
    )
