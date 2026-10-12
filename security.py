import os
import time
from typing import Dict, Any, Tuple
import jwt

SECRET_KEY = os.getenv("SECRET_KEY") # os.getenv(KEY, DEFAULT)
ALGORITHM = os.getenv("ALGORITHM") # Algo is optional to put on .env, easier to change

def create_access_token(subject: str, role: str = "member") -> str:
    """Generates a signed JWT"""
    payload: Dict = {
        "sub": subject, # Identifier
        "role": role,
        "iat": int(time.time()), # Issued at
        "exp": int(time.time()) + 3600 # Expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)
    # Inside the PyJWT library:
    # def encode(payload, key, algorithm="HS256", headers=None, json_encoder=None):
    # result: HEADER (algo and type[jwt]).PAYLOAD (holds the data).SIGNATURE (Hash)
    # Signature = ALGORTIHM(HEADER+PAYLOAD, SECRET_KEY)

def verify_access_token(token: str) -> Tuple[bool, Dict[str, Any] | None, str]:
    """
    Validates token signature and expiration.
    Returns: (is_valid, decoded_claims, error_message)
    """
    try:
        decode_payload = jwt.decode(token, SECRET_KEY, ALGORITHM) 
        # Splices back into header, payload, and signature
        # It takes the header and payload and mix it with the stored SECRET_KEY 
        # and compares the calculated signature with the provided signature.
        # It also checks the expiration of the token
        return True, decode_payload, "Signature verified successfully"
    except jwt.ExpiredSignatureError:
        return False, None, "Token signature has expired"
    except jwt.InvalidTokenError as err:
        return False, None, f"Cryptographic verification failed: {str(err)}"