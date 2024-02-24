from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    username:str
    
class UserCreated(BaseModel):
    id : int
    username:str
    email:EmailStr
    
class LoginResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id : Optional[str] = None
    