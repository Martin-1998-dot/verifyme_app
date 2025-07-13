from flask import Flask, request, redirect, url_for, flash, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    required_files = ['id_doc', 'ownership_doc', 'utility_bill', 'declaration']
    for file_key in required_files:
        file = request.files.get(file_key)
        if not file or not allowed_file(file.filename):
            flash(f"Missing or invalid file: {file_key}")
            return redirect(url_for('index'))
        filename = secure_filename(f"{file_key}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash("All files uploaded successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import hashlib
from typing import Optional
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database setup and initialization
def get_db_connection():
    conn = sqlite3.connect('verifyme.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
    conn.close()

init_db()

# Password hashing helpers
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# Session cookie helpers
SECRET_KEY = "supersecretkey123"

def create_signature(username: str) -> str:
    return hashlib.sha256((username + SECRET_KEY).encode()).hexdigest()

def verify_signature(username: str, signature: str) -> bool:
    return create_signature(username) == signature

async def get_current_username(session: Optional[str] = Cookie(None)):
    if not session:
        return None
    try:
        username, signature = session.split("|")
        if verify_signature(username, signature):
            return username
    except Exception:
        pass
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, username: Optional[str] = Depends(get_current_username)):
    return templates.TemplateResponse("home.html", {"request": request, "username": username})

from fastapi import Form
from starlette.responses import RedirectResponse

@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "message": ""})

@app.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    hashed_pw = hash_password(password)
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        message = "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        message = "Username already exists."
    finally:
        conn.close()
    return templates.TemplateResponse("register.html", {"request": request, "message": message})

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and verify_password(password, user["password"]):
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        signature = create_signature(username)
        response.set_cookie(key="session", value=f"{username}|{signature}", httponly=True)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials."})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session")
    return response


@app.get("/verify", response_class=HTMLResponse)
async def verify_get(request: Request, username: Optional[str] = Depends(get_current_username)):
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("verify.html", {"request": request, "result": None, "username": username})

@app.post("/verify", response_class=HTMLResponse)
async def verify_post(
    request: Request,
    category: str = Form(...),
    value: str = Form(...),
    username: Optional[str] = Depends(get_current_username)
):
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # MOCK VERIFICATION LOGIC
    result = ""
    if category == "property":
        if value == "12345B":
            result = "✅ Owner Found: Martin Mpande"
        else:
            result = "❌ No Match Found for Stand Number"
    elif category == "vehicle":
        if value == "ABZ1234":
            result = "✅ Vehicle Registered to: Martin Mpande"
        else:
            result = "❌ No Vehicle Record Found"
    elif category == "id":
        if value == "99-1234567X00":
            result = "✅ ID Verified: Martin Mpande"
        else:
            result = "❌ ID Not Found"

    return templates.TemplateResponse("verify.html", {
        "request": request,
        "result": result,
        "username": username
    })
