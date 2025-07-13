from typing import Optional
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import shutil
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="uploads"), name="static")
templates = Jinja2Templates(directory="templates")

DB_PATH = "verifyme.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        full_name TEXT,
        id_number TEXT,
        phone TEXT,
        email TEXT,
        proof1 TEXT,
        proof2 TEXT,
        proof3 TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_upload(
    request: Request,
    category: str = Form(...),
    full_name: str = Form(...),
    id_number: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    proof1: UploadFile = File(...),
    proof2: UploadFile = File(None),
    proof3: UploadFile = File(None),
):
    # Validate fields (basic check, can expand)
    if not category or not full_name or not id_number or not phone or not email or not proof1:
        return templates.TemplateResponse("main.html", {
            "request": request,
            "message": "Error: Please fill in all required fields and upload at least one proof document."
        })

    # Save uploaded files
    proof1_path = os.path.join(UPLOAD_DIR, proof1.filename)
    with open(proof1_path, "wb") as f:
        shutil.copyfileobj(proof1.file, f)

    proof2_path = None
    if proof2:
        proof2_path = os.path.join(UPLOAD_DIR, proof2.filename)
        with open(proof2_path, "wb") as f:
            shutil.copyfileobj(proof2.file, f)

    proof3_path = None
    if proof3:
        proof3_path = os.path.join(UPLOAD_DIR, proof3.filename)
        with open(proof3_path, "wb") as f:
            shutil.copyfileobj(proof3.file, f)

    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO verifications (category, full_name, id_number, phone, email, proof1, proof2, proof3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (category, full_name, id_number, phone, email, proof1_path, proof2_path, proof3_path))
    conn.commit()
    conn.close()

    return templates.TemplateResponse("main.html", {
        "request": request,
        "message": "Verification documents uploaded successfully!"
    })

@app.post("/search", response_class=HTMLResponse)
async def post_search(
    request: Request,
    category: str = Form(...),
    full_name: str = Form(None),
    id_number: str = Form(None),
    plate: str = Form(None),
    property_id: str = Form(None),
):
    # Basic validation depending on category
    if category == "car":
        if not full_name or not id_number or not plate:
            return templates.TemplateResponse("main.html", {
                "request": request,
                "message": "Error: For car verification, please provide full name, ID number, and license plate."
            })
    elif category == "profession":
        if not full_name or not id_number:
            return templates.TemplateResponse("main.html", {
                "request": request,
                "message": "Error: For profession verification, please provide full name and ID number."
            })
    elif category == "house":
        if not full_name or not id_number or not property_id:
            return templates.TemplateResponse("main.html", {
                "request": request,
                "message": "Error: For house verification, please provide full name, ID number, and stand/property number."
            })

    # Query DB to find matching record
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = "SELECT * FROM verifications WHERE category=? AND full_name=? AND id_number=?"
    params = [category, full_name, id_number]

    if category == "car":
        query += " AND proof2 LIKE ?"
        params.append(f"%{plate}%")
    elif category == "house":
        query += " AND proof3 LIKE ?"
        params.append(f"%{property_id}%")

    c.execute(query, params)
    record = c.fetchone()
    conn.close()

    if record:
        message = "✅ Verification successful: record found."
    else:
        message = "❌ No matching record found."

    return templates.TemplateResponse("main.html", {
        "request": request,
        "message": message
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_view(request: Request):
    conn = sqlite3.connect("verifyme.db")
    c = conn.cursor()
    c.execute("SELECT * FROM verifications ORDER BY id DESC")
    records = c.fetchall()
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "records": records})

@app.get("/export")
def export_csv():
    conn = sqlite3.connect("verifyme.db")
    c = conn.cursor()
    c.execute("SELECT * FROM verifications")
    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Category", "Full Name", "ID Number", "Phone", "Email", "File 1", "File 2", "File 3", "Timestamp"])
    for row in rows:
        writer.writerow(row)

    output.seek(0)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=verifications.csv"})

from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_303_SEE_OTHER

app.add_middleware(SessionMiddleware, secret_key="your-very-secure-secret-key")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"  # Change to your preferred password!

@app.get("/admin-login", response_class=HTMLResponse)
async def get_admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin-login")
async def post_admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["admin_logged_in"] = True
        return RedirectResponse(url="/admin", status_code=HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin-logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

    conn = sqlite3.connect("verifyme.db")
    c = conn.cursor()
    c.execute("SELECT * FROM verifications ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    return templates.TemplateResponse("admin.html", {"request": request, "verifications": rows})

from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

@app.post("/search", response_class=HTMLResponse)
async def handle_search(request: Request,
                        category: str = Form(...),
                        full_name: str = Form(""),
                        id_number: str = Form(""),
                        plate: str = Form(""),
                        property_id: str = Form("")):
    db = SessionLocal()
    result = None

    if category == "car":
        result = db.query(User).filter_by(category="cars", full_name=full_name.strip(), id_number=id_number.strip()).first()
    elif category == "profession":
        result = db.query(User).filter_by(category="profession", full_name=full_name.strip(), id_number=id_number.strip()).first()
    elif category == "house":
        result = db.query(User).filter_by(category="houses", full_name=full_name.strip(), id_number=id_number.strip()).first()

    message = "✅ Verification Successful." if result else "❌ No record found."
    return templates.TemplateResponse("search.html", {"request": request, "message": message})

import os
from fastapi import UploadFile
from uuid import uuid4

def save_uploaded_file(file: UploadFile, folder: str) -> str:
    if file.filename == "":
        return ""
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    upload_dir = f"uploads/{folder}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path

@app.post("/submit")
async def submit_verification(
    request: Request,
    category: str = Form(...),
    full_name: str = Form(...),
    id_number: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    proof1: UploadFile = File(...),
    proof2: UploadFile = File(...),
    face_file: UploadFile = File(None)
):
    # Save the uploaded files
    file1_path = save_uploaded_file(proof1, category)
    file2_path = save_uploaded_file(proof2, category)
    face_path = save_uploaded_file(face_file, category) if face_file else ""

    # Save entry (you can also push this to a database later)
    data = {
        "category": category,
        "full_name": full_name,
        "id_number": id_number,
        "phone": phone,
        "email": email,
        "proof1": file1_path,
        "proof2": file2_path,
        "face_file": face_path,
    }

    db.append(data)
    return RedirectResponse("/", status_code=303)

# Helper function to save data to JSON
def save_submission(data, filename="submissions.json"):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            submissions = json.load(f)
    else:
        submissions = []
    submissions.append(data)
    with open(file_path, "w") as f:
        json.dump(submissions, f, indent=4)

# Modify existing route or define new one if needed
@app.post("/submit")
async def submit_verification(
    request: Request,
    category: str = Form(...),
    full_name: str = Form(...),
    id_number: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    proof1: UploadFile = File(...),
    proof2: UploadFile = File(...),
    face_file: UploadFile = File(None)
):
    # Store submission data without files (simplified)
    submission = {
        "category": category,
        "full_name": full_name,
        "id_number": id_number,
        "phone": phone,
        "email": email,
        "proof1": proof1.filename,
        "proof2": proof2.filename,
        "face_file": face_file.filename if face_file else None
    }

    save_submission(submission)
    return RedirectResponse(url="/", status_code=303)

@app.get("/admin/submissions", response_class=HTMLResponse)
async def view_submissions(request: Request):
    file_path = os.path.join(os.path.dirname(__file__), "submissions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    return templates.TemplateResponse("admin_submissions.html", {"request": request, "submissions": data})

from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

app.add_middleware(SessionMiddleware, secret_key="verifyme_secret_key")

templates = Jinja2Templates(directory="templates")

@app.get("/admin/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin/login", response_class=HTMLResponse)
async def post_login(request: Request, password: str = Form(...)):
    if password == "admin123":
        request.session["is_admin"] = True
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect password"})

@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect(request: Request):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login", status_code=303)
    return RedirectResponse(url="/admin/submissions", status_code=303)

@app.get("/admin/submissions", response_class=HTMLResponse)
async def view_admin_submissions(request: Request):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login", status_code=303)
    submissions = list(data_store.values())
    return templates.TemplateResponse("admin_submissions.html", {"request": request, "submissions": submissions})

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

@app.get("/admin/submissions", response_class=HTMLResponse)
async def admin_submissions(request: Request):
    # Fetch all submissions from DB - replace with your actual DB code
    submissions = []  # Example placeholder list
    # TODO: Query your database here to get submissions

    return templates.TemplateResponse("admin_submissions.html", {"request": request, "submissions": submissions})


@app.get("/admin/submissions")
async def view_submissions(request: Request, status: Optional[str] = None, category: Optional[str] = None):
    query = "SELECT * FROM submissions WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if category:
        query += " AND category = ?"
        params.append(category)

    rows = db.execute(query, params).fetchall()
    return templates.TemplateResponse("submissions.html", {"request": request, "rows": rows, "status": status or "", "category": category or ""})

@app.get("/admin/approve/{submission_id}")
def approve_submission(submission_id: int):
    db.execute("UPDATE submissions SET status = 'approved' WHERE id = ?", (submission_id,))
    db.commit()
    return RedirectResponse(url="/admin/submissions", status_code=303)

@app.get("/admin/reject/{submission_id}")
def reject_submission(submission_id: int):
    db.execute("UPDATE submissions SET status = 'rejected' WHERE id = ?", (submission_id,))
    db.commit()
    return RedirectResponse(url="/admin/submissions", status_code=303)
