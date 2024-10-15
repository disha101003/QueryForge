from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from rag import response

app = Flask(__name__, 
            template_folder='../../frontend/templates', 
            static_folder='../../frontend')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template


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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    
    search_result = None  # Initialize search_result
    if request.method == 'POST':
        query = request.form.get('query')
        search_result = response(query)  # Call your search function with the query

    return render_template('search.html', search_result=search_result)  # Pass the result to the template


if __name__ == '__main__':
    app.run(debug=True)
