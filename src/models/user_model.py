from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime
from src.enums.company_enums import CompanyPlanEnum

class User(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    name: str
    role: str
    active: bool
    last_login: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # TODO: Need to be inmplemented
    # company_id
    # fiscal_invoices

    class Settings:
        name = "users" 