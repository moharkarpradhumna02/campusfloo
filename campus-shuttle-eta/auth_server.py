#!/usr/bin/env python3
"""
Standalone Campus Flow Auth & Wallet Micro-Server.
Run directly:  python3 auth_server.py
Listens on http://localhost:8090
Provides: POST /api/auth/register, POST /api/auth/login, GET /api/auth/users
No external dependencies beyond Python 3.9+ stdlib.
"""
import json, os, hashlib, secrets, http.server, socketserver, urllib.parse
from datetime import datetime

PORT = 8090
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_db.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)

def hash_pw(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed

class AuthHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(200, {"ok": True})

    def do_GET(self):
        if self.path == "/api/auth/users":
            users = load_users()
            safe = [{"id": u["id"], "name": u["name"], "email": u["email"],
                     "student_id": u["student_id"], "wallet_balance": u["wallet_balance"],
                     "total_rides": u["total_rides"], "created_at": u["created_at"]} for u in users]
            self._send_json(200, safe)
        elif self.path == "/":
            self._send_json(200, {"service": "Campus Flow Auth Server", "status": "online", "port": PORT})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        if self.path == "/api/auth/register":
            self._handle_register(data)
        elif self.path == "/api/auth/login":
            self._handle_login(data)
        else:
            self._send_json(404, {"error": "Not found"})

    def _handle_register(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        student_id = data.get("student_id", "")
        commute_mode = data.get("commute_mode", "bus")

        if not name or not email or not password:
            self._send_json(400, {"error": "Name, email, and password are required."})
            return

        users = load_users()
        for u in users:
            if u["email"] == email:
                self._send_json(409, {"error": "Email already registered. Please login."})
                return

        salt, hashed_pw = hash_pw(password)
        user = {
            "id": f"USR-{secrets.token_hex(4).upper()}",
            "name": name,
            "email": email,
            "student_id": student_id or f"STU-{secrets.token_hex(3).upper()}",
            "password_hash": hashed_pw,
            "password_salt": salt,
            "commute_mode": commute_mode,
            "wallet_balance": 240.00,
            "created_at": datetime.now().isoformat(),
            "total_rides": 0,
            "payment_history": []
        }
        users.append(user)
        save_users(users)

        profile = {k: v for k, v in user.items() if "password" not in k}
        self._send_json(201, {"status": "success", "message": f"Welcome to Campus Flow, {name}!", "user": profile})

    def _handle_login(self, data):
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            self._send_json(400, {"error": "Email and password are required."})
            return

        users = load_users()
        for u in users:
            if u["email"] == email:
                salt = u["password_salt"]
                _, check_hash = hash_pw(password, salt)
                if check_hash == u["password_hash"]:
                    profile = {k: v for k, v in u.items() if "password" not in k}
                    self._send_json(200, {"status": "success", "message": f"Welcome back, {u['name']}!", "user": profile})
                    return
                else:
                    self._send_json(401, {"error": "Incorrect password."})
                    return

        self._send_json(404, {"error": "No account found with this email. Please sign up first."})

    def log_message(self, format, *args):
        print(f"[Campus Flow Auth] {args[0]}")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        print(f"🔐 Campus Flow Auth Server running on http://localhost:{PORT}")
        print(f"   POST /api/auth/register  — Create new account")
        print(f"   POST /api/auth/login     — Login with email + password")
        print(f"   GET  /api/auth/users     — List all users")
        print(f"   Users saved to: {USERS_FILE}")
        httpd.serve_forever()
