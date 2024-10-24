from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__,
            template_folder="../../frontend/templates",
            static_folder="../../frontend/")
app.config['SECRET_KEY'] = 'some_random_secret_key'  # For flash messages
DATABASE = 'users.db'

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
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

# Create the users table when the application starts
create_table()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists in the database
        with get_db() as conn:
            existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if existing_user:
            flash('Email already exists! Try logging in.', 'danger')
        else:
            # Add the new user to the database
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

        # Retrieve the user from the database
        with get_db() as conn:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and user['password'] == password:
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('queryforge'))  # Redirect to the front page
        else:
            flash('Invalid credentials! Please try again.', 'danger')

    return render_template('index.html')

@app.route('/search')
def queryforge():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
