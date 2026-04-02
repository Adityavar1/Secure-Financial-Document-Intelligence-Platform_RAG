import json
import bcrypt
import os
from datetime import datetime, timedelta
from jose import jwt

from config import USERS_FILE, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def authenticate(username, password):
    users = load_users()
    if username in users:
        if verify_password(password, users[username]['password']):
            return users[username]
    return None


# 🔥 JWT FUNCTIONS

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None

def create_user(username, password, department, email):
    users = load_users()

    if username in users:
        return False, "Username already exists"

    users[username] = {
        "password": hash_password(password),
        "department": department,
        "email": email
    }

    save_users(users)
    return True, "User created successfully"

# Default admin
if not os.path.exists(USERS_FILE):
    users = {
        "admin": {
            "password": hash_password("admin123"),
            "department": "admin",
            "email": "admin@company.com"
        }
    }
    save_users(users)