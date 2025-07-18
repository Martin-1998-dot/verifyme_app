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
