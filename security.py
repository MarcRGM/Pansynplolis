import os
import time
from typing import Dict, Any
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") # Optional to put on .env, easier to change

def create_access_token(subject: str, role: str = "member") -> str:
    """Generates a signed JWT"""
    payload: Dict = {
        "sub": subject,
        "role": role,
        "iat": int(time.time()), # Issued at
        "exp": int(time.time()) + 3600 # Expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)
    # Inside the PyJWT library:
    # def encode(payload, key, algorithm="HS256", headers=None, json_encoder=None):