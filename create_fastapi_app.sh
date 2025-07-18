#!/bin/bash

cat << 'PY' > main.py
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(
    id_doc: UploadFile = File(...),
    ownership_doc: UploadFile = File(...),
    utility_bill: UploadFile = File(...),
    declaration: UploadFile = File(...),
):
    files = {
        "id_doc": id_doc,
        "ownership_doc": ownership_doc,
        "utility_bill": utility_bill,
        "declaration": declaration,
    }
    for key, file in files.items():
        filename = f"{key}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/", status_code=303)
PY

echo "✅ main.py FastAPI server created successfully."
