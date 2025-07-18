#!/bin/bash
echo "🐍 Creating Flask app basic structure in app.py..."

cat << 'PY' > app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///verifyme.sqlite'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    id_image = db.Column(db.String(300))
    status = db.Column(db.String(50), default='Pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

@app.route('/')
def home():
    return "Welcome to VerifyMe app! Use /admin/login for admin panel."

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=5002, debug=True)
PY

echo "✅ Flask app.py created."
