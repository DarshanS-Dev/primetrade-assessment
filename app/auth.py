from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.config import settings

pwd_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(hashed: str, password: str):
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    to_encode = data.copy() 
    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expiry})
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)

def verify_token(token: str):
    try: 
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        return payload
    except JWTError:
        raise ValueError("Invalid token")