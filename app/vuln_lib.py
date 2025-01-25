import sqlite3
import os
import hashlib
from flask import escape


# 1. Broken Authentication: Hardcoded credentials
def authenticate(username, password):
    if username == "admin" and password == "password123":  # Hardcoded credentials
        return True
    return False


# 2. Sensitive Data Exposure: Weak hashing mechanism for storing passwords
def store_password_weak(password):
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # MD5 is insecure
    return hashed_password


# 3. SQL Injection
def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # Vulnerable to SQL injection
    cursor.execute(query)
    user_data = cursor.fetchall()
    conn.close()
    return user_data


# 4. Security Misconfiguration: Debug mode enabled
def start_flask_app(app):
    app.run(debug=True)  # Debug mode exposes sensitive stack traces


# 5. Cross-Site Scripting (XSS): Reflecting user input
def render_user_input(input_data):
    return f"Hello, {input_data}"  # Unescaped user input


# 6. Insecure Deserialization
def insecure_deserialization(data):
    return eval(data)  # `eval` executes arbitrary Python code


# 7. Using Components with Known Vulnerabilities: Vulnerable package usage
def parse_xml(xml_string):
    from xml.etree.ElementTree import XMLParser
    parser = XMLParser()  # Vulnerable to XML External Entity (XXE) attacks
    parser.feed(xml_string)
    return parser.close()


# 8. Insufficient Logging and Monitoring: No logging on errors
def transfer_money(amount, account_from, account_to):
    # No logging of transfer details or errors
    if amount <= 0:
        raise ValueError("Amount must be positive")
    # Simulate money transfer logic
    return f"Transferred {amount} from {account_from} to {account_to}"


# 9. Broken Access Control: Lack of role validation
def view_admin_panel(user_role):
    if user_role == "user":  # No proper access control
        return "Welcome to the admin panel"
    return "Access denied"


# 10. Server-Side Request Forgery (SSRF)
def fetch_external_data(url):
    import requests
    response = requests.get(url)  # Allows unvalidated user input as URL
    return response.text
