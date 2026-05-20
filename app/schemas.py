from pydantic import BaseModel, EmailStr
import uuid

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class WatchlistCreate(BaseModel):
    symbol: str

class WatchlistUpdate(BaseModel):
    item_id: uuid.UUID
    symbol: str

class WatchlistDelete(BaseModel):
    item_id: uuid.UUID

class WatchlistOut(BaseModel):
    id: uuid.UUID
    symbol: str

class WatchlistAdminOut(BaseModel):
    id: uuid.UUID
    symbol: str
    user_email: str