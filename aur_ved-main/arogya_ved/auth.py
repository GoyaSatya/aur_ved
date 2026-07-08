from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import hashlib
import hmac
import random
import string

SECRET_KEY = "healthpulse-ai-secret-key-2024-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def hash_password(password: str) -> str:
    """SHA256-based password hashing (compatible with Python 3.14)"""
    salt = "healthpulse_salt_2024"
    return hashlib.sha256(f"{salt}{password}{salt}".encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))

def get_current_user(token: str, db):
    from models import User
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Handle "Bearer " prefix
    if token.startswith("Bearer "):
        token = token[7:]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_optional(request, db):
    """Try to get user from token, but return None instead of raising if not found"""
    from models import User
    token = request.cookies.get("access_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return None
    try:
        payload = decode_token(token)
        if not payload:
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == int(user_id)).first()
    except:
        return None
