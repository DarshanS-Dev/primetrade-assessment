from pydantic import BaseModel
import uuid

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
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