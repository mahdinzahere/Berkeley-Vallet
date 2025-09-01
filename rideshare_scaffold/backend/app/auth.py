import jwt
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .config import settings

security = HTTPBearer()

# In-memory storage for verification codes (in production, use Redis)
verification_codes = {}

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def send_magic_link(email: str, phone: str, role: str) -> str:
    """Send magic link and return verification code"""
    code = generate_verification_code()
    key = f"{email}:{phone}"
    verification_codes[key] = {
        "code": code,
        "role": role,
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.MAGIC_LINK_EXPIRE_MINUTES)
    }
    
    # In production, send SMS/email with code
    # For now, just return the code for testing
    return code

def verify_magic_link_code(email: str, phone: str, code: str) -> Optional[dict]:
    """Verify magic link code and return user data if valid"""
    key = f"{email}:{phone}"
    stored_data = verification_codes.get(key)
    
    if not stored_data:
        return None
    
    if stored_data["code"] != code:
        return None
    
    if datetime.utcnow() > stored_data["expires_at"]:
        del verification_codes[key]
        return None
    
    # Remove used code
    del verification_codes[key]
    
    return {
        "email": email,
        "phone": phone,
        "role": stored_data["role"]
    }
