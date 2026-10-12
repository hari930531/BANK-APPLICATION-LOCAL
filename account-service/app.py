import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Admin@123',
    'database': 'bankdb',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/api/accounts', methods=['GET'])
def list_accounts():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT account_id, holder_name, balance FROM accounts ORDER BY account_id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200

@app.route('/api/accounts/<acc_id>', methods=['GET'])
def get_account(acc_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT account_id, holder_name, balance FROM accounts WHERE account_id = %s;", (acc_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(row), 200

@app.route('/api/accounts/update-balance', methods=['POST'])
def update_balance():
    data = request.json or {}
    acc_id = data.get("account_id")
    amount = float(data.get("amount", 0))

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT balance FROM accounts WHERE account_id = %s;", (acc_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Account not found"}), 404

        current_balance = float(row[0])
        new_balance = current_balance + amount

        if new_balance < 0:
            return jsonify({"error": "Insufficient balance"}), 400

        cur.execute("UPDATE accounts SET balance = %s WHERE account_id = %s;", (new_balance, acc_id))
        conn.commit()
        return jsonify({"account_id": acc_id, "new_balance": new_balance}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)