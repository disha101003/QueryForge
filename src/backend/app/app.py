from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
import docx
from PyPDF2 import PdfReader
from collections import Counter
import re
ALLOWED_EXTENSIONS = {'docx'}

app = Flask(__name__,
            template_folder="../../frontend/templates",
            static_folder="../../frontend/")
app.config['SECRET_KEY'] = 'some_random_secret_key' 
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}
DATABASE = 'users.db'


# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def create_table():
    """Create the users table if it doesn't exist."""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')


create_table()

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_docx(file_path):
    """Extract text from a .docx file."""
    doc = docx.Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def extract_keywords(text):
    """Extract important keywords and phrases from the text."""
    # Predefined list of common skills (single words and multi-word phrases)
    common_keywords = [
        'python', 'java', 'c++', 'machine learning', 'data analysis', 'teamwork', 
        'project management', 'artificial intelligence', 'software development', 
        'deep learning', 'cloud', 'agile', 'scrum', 'big data', 'data science', 
        'sql', 'react', 'nodejs', 'devops', 'github', 'docker', 'kubernetes', 
        'html', 'css', 'javascript', 'api', 'typescript', 'automation', 
        'cloud computing', 'aws', 'azure', 'saas', 'data visualization', 'etl', 
        'data engineer', 'problem-solving', 'leadership', 'communication'
    ]
    
    # Preprocess text: normalize case, remove special characters
    normalized_text = text.lower()
    
    # Use regex to find both words and phrases
    found_keywords = []
    for keyword in common_keywords:
        # Escape keywords for regex and search as whole words/phrases
        if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_text):
            found_keywords.append(keyword)

    # Count occurrences of keywords/phrases
    if not found_keywords:
        return ["No keywords found"]
    
    return dict(Counter(found_keywords))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        
        with get_db() as conn:
            existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if existing_user:
            flash('Email already exists! Try logging in.', 'danger')
        else:
            
            with get_db() as conn:
                conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                             (username, email, password))
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

       
        with get_db() as conn:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and user['password'] == password:
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('queryforge'))  
        else:
            flash('Invalid credentials! Please try again.', 'danger')

    return render_template('index.html')

@app.route('/search')
def queryforge():
    return render_template('search.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/resume-parser', methods=['GET', 'POST'])
def resume_parser():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text based on file type
            if filename.endswith('.docx'):
                text = extract_text_from_docx(file_path)
        
            else:
                flash('Unsupported file format!', 'danger')
                return redirect(request.url)

            # Extract keywords
            keywords = extract_keywords(text)
            flash(f'Keywords extracted: {keywords}', 'success')
            return render_template('resume_parser.html', keywords=keywords)

        flash('Invalid file type! Only DOCX are allowed.', 'danger')

    return render_template('resume_parser.html')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
