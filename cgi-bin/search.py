#!/usr/bin/env python3

import cgi
import os
import sqlite3
import html

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
category = form.getvalue("category", "").strip()
id_number = form.getvalue("id_number", "").strip()

def safe(value):
    return html.escape(str(value))

try:
    conn = sqlite3.connect("../verifyme.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, id_number, file_paths, created_at FROM verifications WHERE category=? AND id_number=?", (category, id_number))
    result = cursor.fetchone()

    print("<html><head><title>Verification Result</title>")
    print(\"\"\"
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        h2 { margin-bottom: 10px; }
        .verified { color: green; }
        .not-found { color: red; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        .file-link {
            background-color: #007BFF;
            color: white;
            padding: 6px 12px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 4px 0;
        }
        .back-link {
            margin-top: 20px;
            display: inline-block;
            color: #444;
            text-decoration: none;
        }
    </style>
    \"\"\")
    print("</head><body>")

    if result:
        name, cat, idnum, file_paths, created_at = result
        files = file_paths.split(",")

        print(f"<h2 class='verified'>✅ Match Found</h2>")
        print("<table>")
        print(f"<tr><th>Name</th><td>{safe(name)}</td></tr>")
        print(f"<tr><th>Category</th><td>{safe(cat)}</td></tr>")
        print(f"<tr><th>ID Number</th><td>{safe(idnum)}</td></tr>")
        print(f"<tr><th>Verified On</th><td>{safe(created_at)}</td></tr>")
        print("<tr><th>Documents</th><td>")

        for f in files:
            fname = os.path.basename(f.strip())
            print(f"<a class='file-link' href='/cgi-bin/serve_file.py?file={safe(fname)}' target='_blank'>📄 {safe(fname)}</a><br>")

        print("</td></tr>")
        print("</table>")
    else:
        print(f"<h2 class='not-found'>❌ No record found for ID: <b>{safe(id_number)}</b> in category: <b>{safe(category)}</b></h2>")

    print("<br><a class='back-link' href='../search.html'>← Back to Search</a>")
    print("</body></html>")

except Exception as e:
    print(f"<h2 class='not-found'>❌ Error: {html.escape(str(e))}</h2>")
    print("<br><a href='../search.html'>← Back to Search</a>")
