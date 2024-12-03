from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from trie import Trie
from optimize import optimize_codes, generate_short_code
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Create a Trie instance to store short codes and long URLs
trie = Trie()

# Simulating a database with a dictionary (can be replaced with an actual database)
users = {}  # Format: {'username': {'password': hashed_password}}

# Simulating access frequencies (replace with actual data if needed)
access_frequencies = {
    'http://example1.com': 120,
    'http://example2.com': 80,
    'http://example3.com': 200,
    'http://example4.com': 50
}

url_list = ['http://example1.com', 'http://example2.com', 'http://example3.com', 'http://example4.com']

# User Signup Form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])

# User Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if not long_url:
            return "Please enter a valid URL!", 400
        
        # First, check if the URL is in the list for optimization
        if long_url not in url_list:
            url_list.append(long_url)
            access_frequencies[long_url] = 1  # Initially assigning an access frequency

        # Optimize code assignment based on DP
        optimized_codes, total_length = optimize_codes(url_list, access_frequencies)

        # Generate short code for the entered URL using the optimized approach
        short_code = optimized_codes.get(long_url, generate_short_code(long_url))

        # Insert the short code into Trie
        if not trie.search(short_code):
            trie.insert(short_code, long_url)

        # Redirect to the result page with the generated short URL
        return redirect(url_for('result', short_code=short_code))  # Pass short_code in the URL

    return render_template('index.html')

@app.route('/result/<short_code>', methods=['GET'])
def result(short_code):
    # Retrieve the long URL associated with the short code
    long_url = trie.search(short_code)
    if long_url:
        return render_template('result.html', short_url=short_code, long_url=long_url)
    return "URL not found!", 404

# Route to handle the signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if the passwords match
        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('signup'))

        # Hash the password using PBKDF2
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Save the user to the "database"
        users[username] = {'password': hashed_password, 'email': email}
        flash("Signup successful! Please log in.", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

# Route to handle the login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = users.get(username)

        # Check if the user exists and the password is correct
        if user and check_password_hash(user['password'], password):
            session['user'] = username  # Store the username in the session
            flash("Login successful!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", 'danger')

    return render_template('login.html', form=form)

# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    flash("Logged out successfully!", 'info')
    return redirect(url_for('index'))

# Add this route to handle short code redirection
@app.route('/<short_code>', methods=['GET'])
def redirect_to_long_url(short_code):
    # Lookup the short code in the Trie
    long_url = trie.search(short_code)
    if long_url:
        return redirect(long_url)  # Redirect to the long URL
    return "URL not found!", 404  # If the short code is not found, show an error message

if __name__ == '__main__':
    app.run(debug=True)
