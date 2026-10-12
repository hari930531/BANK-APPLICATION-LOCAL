# ==============================================================================
# File: transfer-service/app.py
# Description: Fund Transfer Microservice for Hari's Bank of Tamil Nadu.
# Facilitates inter-account balance transactions with debit, credit,
# balance checks, and rollback safety.
# ==============================================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Initialize Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) across all origins and headers
# to prevent browser preflight (OPTIONS) fetch errors
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Endpoint of the Account Service (runs on local port 5001)
ACCOUNT_SERVICE_URL = "http://127.0.0.1:5001/api/accounts"


# ------------------------------------------------------------------------------
# ENDPOINT: Transfer Funds
# Method: POST, OPTIONS
# Path: /api/transfer
# Payload: {
#   "from_account": "<str>",
#   "to_account": "<str>",
#   "amount": <float>
# }
# ------------------------------------------------------------------------------
@app.route('/api/transfer', methods=['POST', 'OPTIONS'])
def transfer():
    # Handle preflight CORS handshake from browser
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # Parse JSON request payload safely
    data = request.json or {}
    from_acc = data.get('from_account')
    to_acc = data.get('to_account')

    # Validate that transaction amount is a positive number
    try:
        amount = float(data.get('amount', 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount provided."}), 400

    # Validation rules
    if not from_acc or not to_acc or amount <= 0:
        return jsonify({"error": "Invalid transfer parameters."}), 400

    if from_acc == to_acc:
        return jsonify({"error": "Cannot transfer funds to the same account."}), 400

    # 1. Verify existence and retrieve balance of the sender account
    r_from = requests.get(f"{ACCOUNT_SERVICE_URL}/{from_acc}")
    if r_from.status_code != 200:
        return jsonify({"error": f"Sender account {from_acc} not found."}), 404

    sender_data = r_from.json()
    sender_bal = float(sender_data.get('balance', 0))

    # Check for sufficient balance
    if sender_bal < amount:
        return jsonify({"error": "Insufficient funds to complete this transfer."}), 400

    # 2. Verify existence of the recipient account
    r_to = requests.get(f"{ACCOUNT_SERVICE_URL}/{to_acc}")
    if r_to.status_code != 200:
        return jsonify({"error": f"Recipient account {to_acc} not found."}), 404

    # 3. Debit the requested amount from the sender account
    debit_res = requests.post(f"{ACCOUNT_SERVICE_URL}/update-balance", json={
        "account_id": from_acc,
        "amount": -amount
    })

    if debit_res.status_code != 200:
        return jsonify({"error": "Debit operation failed on sender account."}), 500

    # 4. Credit the amount to the recipient account
    credit_res = requests.post(f"{ACCOUNT_SERVICE_URL}/update-balance", json={
        "account_id": to_acc,
        "amount": amount
    })

    # 5. Compensating transaction (Rollback) if credit operation fails
    if credit_res.status_code != 200:
        requests.post(f"{ACCOUNT_SERVICE_URL}/update-balance", json={
            "account_id": from_acc,
            "amount": amount
        })
        return jsonify({"error": "Credit operation failed; transaction was rolled back."}), 500

    # Transfer completed successfully
    return jsonify({
        "status": "Success",
        "message": f"Successfully transferred ₹{amount:.2f} to {to_acc}!"
    }), 200


# ------------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Start Transfer Service on local port 5002
    app.run(host='127.0.0.1', port=5002, debug=True)