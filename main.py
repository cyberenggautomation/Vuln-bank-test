"""
VulnBank-Test — intentionally vulnerable Flask app for scanner validation.
DO NOT deploy. Test fixture only. See findings.yaml for the answer key.
"""
import hashlib
import os
import sqlite3
import subprocess

import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULN-001 (Gitleaks: generic-api-key / jwt-secret pattern)
JWT_SECRET = "sk_live_51NxT3stB4nk1ngS3cr3tKeyDoNotUse0000"

DB_PATH = os.path.join(os.path.dirname(__file__), "bank.db")

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route("/api/accounts/<account_id>", methods=["GET"])
def get_account(account_id):
    # VULN-002 (Semgrep: python.sql-injection / CWE-89)
    # String-formatted query, no parameterization.
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id, owner, balance FROM accounts WHERE id = ?"
    cursor.execute(query, (account_id,))
    row = cursor.fetchone()
    conn.close()

    # VULN-003 (business-logic / IDOR — no ownership check against session user)
    # Any authenticated caller can fetch any account_id, not just their own.
    if row:
        return jsonify({"id": row[0], "owner": row[1], "balance": row[2]})
    return jsonify({"error": "not found"}), 404

@app.route("/api/transfer", methods=["POST"])
def transfer_funds():
    data = request.get_json()
    from_acct = data.get("from")
    to_acct = data.get("to")
    amount = data.get("amount")

    # VULN-004 (Semgrep: python.sql-injection, second instance — f-string)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = '{from_acct}'")
    cursor.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = '{to_acct}'")
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/api/statement/export", methods=["POST"])
def export_statement():
    account_id = request.form.get("account_id")
    fmt = request.form.get("format", "pdf")

    # VULN-005 (Semgrep: python.command-injection / CWE-78)
    # User-controlled input passed straight to shell=True.
    cmd = f"statement-exporter --account {account_id} --format {fmt}"
    result = subprocess.run(cmd, shell=True, capture_output=True)

    return jsonify({"output": result.stdout.decode(errors="ignore")})

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # VULN-006 (Semgrep: python.weak-hash / CWE-327)
    # MD5 for password hashing.
    hashed = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        (username, hashed),
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    # VULN-007 (Semgrep: jwt-none-alg risk — algorithm not pinned server-side elsewhere,
    # and JWT_SECRET is hardcoded/weak per VULN-001)
    token = jwt.encode({"user_id": user[0], "username": user[1]}, JWT_SECRET, algorithm="HS256")
    return jsonify({"token": token})

@app.route("/api/auth/verify", methods=["POST"])
def verify_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    # VULN-008 (Semgrep: jwt-decode-verify-false / CWE-347)
    # Signature verification disabled — anyone can forge a token.
    decoded = jwt.decode(token, options={"verify_signature": False})
    return jsonify(decoded)

@app.route("/api/debug/eval", methods=["POST"])
def debug_eval():
    # VULN-009 (Semgrep: python.eval-injection / CWE-95)
    # Left-over debug endpoint, evaluates arbitrary user input.
    expr = request.json.get("expr")
    result = eval(expr)
    return jsonify({"result": result})

if __name__ == "__main__":
    # VULN-010 (Semgrep: flask-debug-true / CWE-489)
    # Debug mode + binds all interfaces.
    app.run(host="0.0.0.0", port=5000, debug=True)