from pydantic import BaseModel
from typing import Optional
from src.enums.company_enums import CompanyPlanEnum


class CreateCompany(BaseModel):
    legal_name: str
    trade_name: str
    state_registration: str
    cnpj: str
    cellphone: str
    email: str
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool = True
    signature_date: Optional[str]
    plan: CompanyPlanEnum = CompanyPlanEnum.free 
    trial_start_date: Optional[str]
    trial_end_date: Optional[str]
    trial_used: bool = False
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode: True

class CompanyResponse(BaseModel):
    id: str
    legal_name: str
    trade_name: str
    state_registration: str
    cnpj: str
    cellphone: str
    email: str
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool = True
    signature_date: Optional[str]
    plan: CompanyPlanEnum = CompanyPlanEnum.free 
    trial_start_date: Optional[str]
    trial_end_date: Optional[str]
    trial_used: bool = False
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode: True

class UpdateCompany(BaseModel):
    id: str
    legal_name: Optional[str]
    trade_name: Optional[str]
    state_registration: Optional[str]
    cnpj: Optional[str]
    cellphone: Optional[str]
    email: Optional[str]
    address_street: Optional[str]
    address_number: Optional[str]
    address_info: Optional[str]
    address_neighborhood: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    postal_code: Optional[str]
    active: bool = True
    signature_date: Optional[str]
    plan: CompanyPlanEnum
    trial_start_date: Optional[str]
    trial_end_date: Optional[str]
    trial_used: bool = False
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode: True
