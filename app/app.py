from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import escape

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

# Model for User (SQL Injection vulnerability)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Vulnerable Form with no CSRF protection (Cross-Site Request Forgery)
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

@app.route('/')
def home():
    return render_template('index.html')

# Login route (Sensitive Data Exposure vulnerability)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials", 400
    return render_template('login.html', form=form)

# Vulnerable Dashboard route
@app.route('/dashboard')
def dashboard():
    # Security Misconfiguration vulnerability (showing sensitive data)
    users = escape(User.query.all())
    return render_template('dashboard.html', users=users)

# Insecure Direct Object References (IDOR) vulnerability in the route
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = escape(User.query.get(user_id))
    if not user:
        return "User Not Found", 404
    return jsonify({'username': user.username, 'id': user.id})

# Endpoint vulnerable to Cross-Site Scripting (XSS)
@app.route('/comment', methods=['POST'])
def comment():
    comment = request.form['comment']
    # Reflected XSS vulnerability
    return f"Comment received: {comment}"

# Unrestricted File Upload vulnerability
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # File extension check is missing (this is an example of unrestricted file upload)
        file.save(os.path.join('uploads', file.filename))
        return "File uploaded successfully"
    return render_template('upload.html')

# Broken Authentication vulnerability (No logout feature implemented)
@app.route('/logout')
def logout():
    return "Logout functionality not implemented"

if __name__ == '__main__':
    app.run(debug=True)
