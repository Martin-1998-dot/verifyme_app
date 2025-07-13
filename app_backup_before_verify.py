from flask import Flask, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
            flash('Registration successful!')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Choose another.')
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

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    result = ""
    if request.method == 'POST':
        category = request.form['category']
        search_value = request.form['search_value']

        # Simulated verification logic
        if category == 'property':
            if search_value == '12345B':
                result = "✅ Property Owner Found: Martin Mpande"
            else:
                result = "❌ No Property Found for Stand Number"
        elif category == 'vehicle':
            if search_value == 'ABX1234':
                result = "✅ Vehicle Owner: Thubelihle Moyo"
            else:
                result = "❌ Vehicle Registration Not Found"
        elif category == 'id':
            if search_value == 'ID99887766':
                result = "✅ ID Verified: Martin Mpande"
            else:
                result = "❌ ID Not Found"

    return f'''
        <h2>Verify Ownership / Identity</h2>
        <form method="post">
            <label>Select Category:</label><br/>
            <select name="category" onchange="updatePlaceholder(this.value)">
                <option value="property">Property Ownership</option>
                <option value="vehicle">Vehicle Registration</option>
                <option value="id">ID Verification</option>
            </select><br/><br/>
            
            <label id="inputLabel">Enter Stand Number:</label><br/>
            <input type="text" name="search_value" id="searchInput" placeholder="e.g. 12345B"/><br/><br/>

            <input type="submit" value="Verify" />
        </form>
        <p>{result}</p>

        <script>
        function updatePlaceholder(category) {{
            let label = document.getElementById('inputLabel');
            let input = document.getElementById('searchInput');
            if (category === 'property') {{
                label.innerText = 'Enter Stand Number:';
                input.placeholder = 'e.g. 12345B';
            }} else if (category === 'vehicle') {{
                label.innerText = 'Enter Vehicle Registration Number:';
                input.placeholder = 'e.g. ABX1234';
            }} else if (category === 'id') {{
                label.innerText = 'Enter National ID:';
                input.placeholder = 'e.g. ID99887766';
            }}
        }}
        </script>
    '''

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    result = ""
    if request.method == 'POST':
        category = request.form['category']
        search_value = request.form['search_value']

        # Simulated verification logic
        if category == 'property':
            if search_value == '12345B':
                result = "✅ Property Owner Found: Martin Mpande"
            else:
                result = "❌ No Property Found for Stand Number"
        elif category == 'vehicle':
            if search_value == 'ABX1234':
                result = "✅ Vehicle Owner: Thubelihle Moyo"
            else:
                result = "❌ Vehicle Registration Not Found"
        elif category == 'id':
            if search_value == 'ID99887766':
                result = "✅ ID Verified: Martin Mpande"
            else:
                result = "❌ ID Not Found"

    return f'''
        <h2>Verify Ownership / Identity</h2>
        <form method="post">
            <label>Select Category:</label><br/>
            <select name="category" onchange="updatePlaceholder(this.value)">
                <option value="property">Property Ownership</option>
                <option value="vehicle">Vehicle Registration</option>
                <option value="id">ID Verification</option>
            </select><br/><br/>

            <label id="inputLabel">Enter Stand Number:</label><br/>
            <input type="text" name="search_value" id="searchInput" placeholder="e.g. 12345B"/><br/><br/>

            <input type="submit" value="Verify" />
        </form>
        <p>{result}</p>

        <script>
        function updatePlaceholder(category) {{
            let label = document.getElementById('inputLabel');
            let input = document.getElementById('searchInput');
            if (category === 'property') {{
                label.innerText = 'Enter Stand Number:';
                input.placeholder = 'e.g. 12345B';
            }} else if (category === 'vehicle') {{
                label.innerText = 'Enter Vehicle Registration Number:';
                input.placeholder = 'e.g. ABX1234';
            }} else if (category === 'id') {{
                label.innerText = 'Enter National ID:';
                input.placeholder = 'e.g. ID99887766';
            }}
        }}
        </script>
    '''
