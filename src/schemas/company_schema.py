from datetime import datetime
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.enums.company_enums import CompanyPlanEnum

class CreateCompany(BaseModel):
    legal_name: str
    trade_name: Optional[str]
    state_registration: Optional[str]
    cnpj: str
    cellphone: Optional[str]
    email: EmailStr
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool = True
    plan: CompanyPlanEnum = CompanyPlanEnum.free 
    trial_used: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # signature_date: Optional[datetime] = None
    # trial_start_date: Optional[datetime] = None
    # trial_end_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class CompanyResponse(BaseModel):
    id: PydanticObjectId
    legal_name: Optional[str]
    trade_name: Optional[str]
    state_registration: Optional[str]
    cnpj: Optional[str]
    cellphone: Optional[str]
    email: str
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool
    plan: CompanyPlanEnum = CompanyPlanEnum.free 
    signature_date: Optional[str] = None
    trial_start_date: Optional[str] = None
    trial_end_date: Optional[str] = None
    trial_used: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes: True

class UpdateCompany(BaseModel):
    id: PydanticObjectId
    legal_name: Optional[str]
    trade_name: Optional[str]
    state_registration: Optional[str]
    cnpj: Optional[str]
    cellphone: Optional[str]
    email: Optional[EmailStr]
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool = True
    plan: CompanyPlanEnum
    signature_date: Optional[datetime] = None
    trial_start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    trial_used: bool = False
    updated_at: Optional[datetime] = datetime

    class Config:
        from_attributes: True
