#!/usr/bin/env python3
import cgi
import cgitb
import os
import sqlite3
from datetime import datetime

cgitb.enable()  # Show errors in browser

UPLOAD_DIR = "../uploads"
DB_PATH = "../verifyme.db"

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
category = form.getvalue("category")
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Generate ID and name from form, fallback to unknown
name = form.getvalue("full_name") or form.getvalue("owner_name") or form.getvalue("company_name") or "Unknown"
id_number = form.getvalue("id_number") or form.getvalue("reg_number") or form.getvalue("stand_number") or form.getvalue("house_number") or "N/A"

# Handle uploaded files
uploaded_files = []
for key in form.keys():
    if form[key].filename:
        raw_file = form[key]
        filename = f"{timestamp}_{os.path.basename(raw_file.filename)}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(raw_file.file.read())
        uploaded_files.append(filepath)

# Save to DB
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            id_number TEXT,
            file_paths TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cursor.execute("""
        INSERT INTO verifications (category, name, id_number, file_paths)
        VALUES (?, ?, ?, ?)
    """, (category, name, id_number, ", ".join(uploaded_files)))
    conn.commit()
    conn.close()

    print("<h2 style='color:green;'>✅ Upload successful!</h2>")
except Exception as e:
    print(f"<h2 style='color:red;'>❌ Error: {e}</h2>")

print('<a href="../upload.html">← Back to Upload</a>')
