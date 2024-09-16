from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,
            # Pointing to templates directory
            template_folder="../../frontend/templates",
            # Pointing to assets directory (for CSS, JS)
            static_folder="../../frontend/assets")

# Temporary in-memory user data
users = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            return "Email already exists!"
        else:
            users[email] = {'username': username, 'password': password}
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            return f"Welcome {user['username']}!"
        else:
            return "Invalid credentials!"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
