"""
Backend auth module: user registration & login with JSON file storage.
Endpoints:
  POST /api/auth/register  — create a new user (name, email, studentId, password)
  POST /api/auth/login     — login (email, password) → returns user profile
  GET  /api/auth/users     — list all registered users (admin/debug)
"""
import json
import os
import hashlib
import secrets
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Simple JSON file-based user store
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def _load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)

def _hash_password(password: str, salt: str = None):
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed


class RegisterRequest(BaseModel):
    name: str
    email: str
    student_id: str = ""
    password: str
    commute_mode: str = "bus"

class LoginRequest(BaseModel):
    email: str
    password: str


@auth_router.post("/register")
def register_user(req: RegisterRequest):
    users = _load_users()

    # Check if email already exists
    for u in users:
        if u["email"].lower() == req.email.lower():
            raise HTTPException(status_code=409, detail="Email already registered. Please login.")

    salt, hashed_pw = _hash_password(req.password)
    user = {
        "id": f"USR-{secrets.token_hex(4).upper()}",
        "name": req.name,
        "email": req.email.lower(),
        "student_id": req.student_id or f"STU-{secrets.token_hex(3).upper()}",
        "password_hash": hashed_pw,
        "password_salt": salt,
        "commute_mode": req.commute_mode,
        "wallet_balance": 240.00,
        "created_at": datetime.now().isoformat(),
        "total_rides": 0,
        "payment_history": []
    }

    users.append(user)
    _save_users(users)

    # Return profile without password
    profile = {k: v for k, v in user.items() if "password" not in k}
    return {"status": "success", "message": f"Welcome to Campus Flow, {req.name}!", "user": profile}


@auth_router.post("/login")
def login_user(req: LoginRequest):
    users = _load_users()

    for u in users:
        if u["email"].lower() == req.email.lower():
            salt = u["password_salt"]
            _, check_hash = _hash_password(req.password, salt)
            if check_hash == u["password_hash"]:
                profile = {k: v for k, v in u.items() if "password" not in k}
                return {"status": "success", "message": f"Welcome back, {u['name']}!", "user": profile}
            else:
                raise HTTPException(status_code=401, detail="Incorrect password.")

    raise HTTPException(status_code=404, detail="No account found with this email. Please sign up first.")


@auth_router.get("/users")
def list_users():
    users = _load_users()
    return [
        {"id": u["id"], "name": u["name"], "email": u["email"], "student_id": u["student_id"],
         "wallet_balance": u["wallet_balance"], "total_rides": u["total_rides"], "created_at": u["created_at"]}
        for u in users
    ]
