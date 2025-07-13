from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///verifyme.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@verifyme.com').first():
            admin = User(
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables if they don't exist

        # Create default admin if not already present
        if not User.query.filter_by(email='admin@verifyme.com').first():
            admin = User(
                fullname='Admin',
                email='admin@verifyme.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
                fullname='Admin',
                email='admin@verifyme.com',
                password_hash=generate_password_hash('adminpass'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables from models

        # Create default admin user if it doesn't exist
        if not User.query.filter_by(email='admin@verifyme.com').first():
            admin = User(
                fullname='Admin',
                email='admin@verifyme.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from werkzeug.security import generate_password_hash

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create default admin user if it doesn't exist
        if not User.query.filter_by(email='admin@verifyme.com').first():
            admin = User(
                fullname='Admin',
                email='admin@verifyme.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create default admin user if not exists
        if not User.query.filter_by(email='admin@verifyme.com').first():
            admin = User(
                fullname='Admin',
                email='admin@verifyme.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)

