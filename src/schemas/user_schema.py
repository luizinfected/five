from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    email: str 
    hashed_password: str
    role: str
    name: str
    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    email: str 
    password: str
    class Config:
        from_attributes = True