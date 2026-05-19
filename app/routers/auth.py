from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app import models, schemas, auth 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.TokenResponse)
async def register(user: schemas.UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    exists = result.scalar_one_or_none()

    if exists:
        raise HTTPException(400, "Email already exists")
    
    hashed_password = auth.hash_password(user.password)

    new_user = models.User(email= user.email, hashed_password= hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    data = {"sub": str(new_user.id), "is_admin": new_user.is_admin}

    return {"access_token": auth.create_token(data), "token_type": "bearer"}

@router.post("/token", response_model=schemas.TokenResponse)
async def login_json(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    curr_user = result.scalar_one_or_none()

    if not curr_user:
        raise HTTPException(401, "Invalid email")
    
    if not auth.verify_password(curr_user.hashed_password, user.password):
        raise HTTPException(401, "Invalid password")
    
    data = {"sub": str(curr_user.id), "is_admin": curr_user.is_admin}

    return {"access_token": auth.create_token(data), "token_type": "bearer"}

@router.post("/login", response_model=schemas.TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == form.username))
    curr_user = result.scalar_one_or_none()

    if not curr_user:
        raise HTTPException(401, "Invalid email")
    
    if not auth.verify_password(curr_user.hashed_password, form.password):
        raise HTTPException(401, "Invalid password")
    
    data = {"sub": str(curr_user.id), "is_admin": curr_user.is_admin}
    return {"access_token": auth.create_token(data), "token_type": "bearer"}