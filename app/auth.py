from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
import uuid

from app.config import settings
from app.database import get_db
from app import models

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
    
async def get_user(
    token: str = Depends(oauth2),
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = verify_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["sub"]
    result = await db.execute(select(models.User).where(models.User.id == uuid.UUID(user_id)))
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return current_user