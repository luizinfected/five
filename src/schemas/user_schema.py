from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    company_id: Optional[int] = None
    email: str 
    hashed_password: str
    role: Optional[str] = "user"
    name: str
    active: bool = True
    last_login: Optional[datetime]
    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    email: str 
    password: str
    class Config:
        from_attributes = True