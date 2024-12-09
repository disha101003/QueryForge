from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from rag import response_prof, response_vip, response_our, response, response_duri
import os
from werkzeug.utils import secure_filename
import docx
from collections import Counter
import re

ALLOWED_EXTENSIONS = {'docx'}
app = Flask(__name__, 
            template_folder='../../frontend/templates', 
            static_folder='../../frontend')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}
db = SQLAlchemy(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize Database
with app.app_context():
    try:
        db.create_all()
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")


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

# Home Page Route
@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template

# Sign Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('signup'))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        # Add to database
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user in session
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('search'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('login.html')

# Search Page Route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    
    search_result = None  # Initialize search_result
    if request.method == 'POST':
        query = request.form.get('query')  # The user's search query
        active_tab = request.form.get('active_tab')  # Get the active tab from the form
      
        # Determine which function to call based on the active tab
        if active_tab == 'Professor':
                search_result = response_prof(query)
        elif active_tab == 'VIP/EPICS':
                search_result = response_vip(query)
        elif active_tab == 'Other Research Opportunities':
            search_result = response_our(query)
        elif active_tab == 'DURI':
                search_result = response_duri(query)
        else:
            search_result = response_prof(query)

    # Render the search results with the corresponding active tab
    return render_template('search.html', search_result=search_result)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Resume-Parser Route
@app.route('/resume-parser', methods=['GET', 'POST'])
def resume_parser():
    search_result = None  # Initialize the search result as None
    keywords = None  # Initialize the keywords as None

    if request.method == 'POST':
        # Handle the file upload
        if 'resume' in request.files:
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

                # Extract keywords from the text
                keywords = extract_keywords(text)

        # Handle top keywords search
        top_keywords = request.form.get('top_keywords')  # Get top keywords from form
     

        if top_keywords:
            top_keywords_list = top_keywords.split(',')  # Convert string to list
            search_result = response(' '.join(top_keywords_list[:3]))  # Get the search result based on the top keywords

            flash(f'Search results based on keywords: {search_result}', 'success')

    return render_template('resume_parser.html', keywords=keywords, search_result=search_result)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
