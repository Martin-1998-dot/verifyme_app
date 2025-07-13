from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # CHANGE THIS TO A SECURE RANDOM STRING

# Database setup
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
    conn.close()

init_db()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please fill out both fields.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            with conn:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                             (username, hashed_password))
            flash('Registration successful! Please log in.')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Choose a different one.')
            return redirect(url_for('register'))
        finally:
            conn.close()

    return '''
        <h2>Register</h2>
        <form method="post">
            Username: <input type="text" name="username" /><br/>
            Password: <input type="password" name="password" /><br/>
            <input type="submit" value="Register" />
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

from flask import g

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None:
            flash('Incorrect username.')
        elif not check_password_hash(user['password'], password):
            flash('Incorrect password.')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('welcome'))

    return '''
        <h2>Login</h2>
        <form method="post">
            Username: <input type="text" name="username"><br/>
            Password: <input type="password" name="password"><br/>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/welcome')
def welcome():
    if g.user is None:
        return redirect(url_for('login'))
    return f"<h2>Welcome, {g.user['username']}!</h2><p><a href='/logout'>Logout</a></p>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

from flask import g

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None:
            flash('Incorrect username.')
        elif not check_password_hash(user['password'], password):
            flash('Incorrect password.')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('welcome'))

    return '''
        <h2>Login</h2>
        <form method="post">
            Username: <input type="text" name="username"><br/>
            Password: <input type="password" name="password"><br/>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/welcome')
def welcome():
    if g.user is None:
        return redirect(url_for('login'))
    return f"<h2>Welcome, {g.user['username']}!</h2><p><a href='/logout'>Logout</a></p>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
