# ==============================================================================
# File: auth-service/app.py
# Description: Authentication Microservice for Hari's Bank of Tamil Nadu.
# Handles user registration, credentials verification, and JWT session generation.
# ==============================================================================

import mysql.connector
import jwt
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from the frontend
CORS(app)

# Secret key used for signing and verifying JWT tokens
SECRET_KEY = "my_banking_secret_jwt_key"

# Database connection credentials for local MySQL server
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Admin@123',  # MySQL root password
    'database': 'bankdb',
    'port': 3306
}

def get_db():
    """
    Helper function to establish and return a new MySQL connection.
    """
    return mysql.connector.connect(**DB_CONFIG)


# ------------------------------------------------------------------------------
# ENDPOINT: User Login
# Method: POST
# Path: /api/auth/login
# Payload: {"username": "<str>", "password": "<str>"}
# ------------------------------------------------------------------------------
@app.route('/api/auth/login', methods=['POST'])
def login():
    # Extract request payload safely
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    # Validate that mandatory fields are present
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # Query the users table to match username and password credentials
    cur.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s", 
        (username, password)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    # Return HTTP 401 Unauthorized if user record is not found
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate a signed JSON Web Token (valid for 2 hours)
    token = jwt.encode({
        "username": user["username"],
        "account_id": user["account_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    # Return success response along with generated token and session payload
    return jsonify({
        "status": "Success",
        "message": f"Welcome {user['username']}!",
        "token": token,
        "user": {
            "username": user["username"],
            "account_id": user["account_id"]
        }
    }), 200


# ------------------------------------------------------------------------------
# ENDPOINT: Register New Customer / Open Account
# Method: POST
# Path: /api/auth/register
# Payload: {
#   "holder_name": "<str>",
#   "username": "<str>",
#   "password": "<str>",
#   "email": "<str>",
#   "phone": "<str>",
#   "address": "<str>",
#   "initial_balance": <float>
# }
# ------------------------------------------------------------------------------
@app.route('/api/auth/register', methods=['POST'])
def register():
    # Parse incoming customer registration data
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    holder_name = data.get('holder_name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    
    # Parse initial opening balance; fallback to default minimum deposit (1000.0)
    try:
        initial_balance = float(data.get('initial_balance', 1000.0))
    except (ValueError, TypeError):
        initial_balance = 1000.0

    # Ensure all required profile details are provided
    if not username or not password or not holder_name or not email or not phone or not address:
        return jsonify({"error": "All fields including Email, Phone, and Address are required"}), 400

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    try:
        # Check if the requested username already exists in the database
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({"error": "Username already exists. Choose another."}), 400

        # Auto-increment Account ID sequence (e.g., ACC101 -> ACC102 -> ACC103)
        cur.execute("SELECT account_id FROM accounts ORDER BY account_id DESC LIMIT 1")
        last_acc = cur.fetchone()
        if last_acc and last_acc['account_id'].startswith('ACC'):
            num = int(last_acc['account_id'].replace('ACC', '')) + 1
            new_acc_id = f"ACC{num}"
        else:
            new_acc_id = "ACC101"

        # 1. Insert bank balance record into the accounts table
        cur.execute(
            "INSERT INTO accounts (account_id, holder_name, balance) VALUES (%s, %s, %s)",
            (new_acc_id, holder_name, initial_balance)
        )

        # 2. Insert user login credentials and profile details into the users table
        cur.execute(
            "INSERT INTO users (username, password, account_id, email, phone, address) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (username, password, new_acc_id, email, phone, address)
        )

        # Commit transaction to ensure both inserts succeed atomically
        conn.commit()

        return jsonify({
            "status": "Success",
            "message": f"Account created successfully! Your Account ID is {new_acc_id}",
            "account_id": new_acc_id
        }), 201

    except Exception as e:
        # Rollback both operations if any step encounters a database error
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up database resources
        cur.close()
        conn.close()


# ------------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Start Auth Service on local port 5003
    app.run(host='127.0.0.1', port=5003, debug=True)