from database_connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from src.models.company_model import Company
from src.schemas.company_schema import CreateCompany, CompanyResponse, UpdateCompany
from sqlalchemy.orm import Session
from src.services.company_service import CompanyService
from auth import get_current_user
from starlette import status


company_routes = APIRouter(dependencies=[Depends(get_current_user)])
company_service = CompanyService()

@company_routes.post("/register")
async def create_company(
    schema: CreateCompany,
    db: Session = Depends(get_db)
):
    
    company_exist = db.query(Company).filter(Company.cnpj == schema.cnpj).first()

    if company_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This CNPJ already exists"
        )

    return await company_service.create_company(db, schema)

@company_routes.get("/list")
async def list_companies(
    db: Session = Depends(get_db)
):  
    
    if not db.query(Company).all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companies not found"
        )
    
    return await company_service.list_companies(db)

@company_routes.get("/detail")
async def detail_company(
    id: int,
    db: Session = Depends(get_db)
):
    
    if not db.query(Company).filter(Company.id == id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return await company_service.detail_company(db, id)

@company_routes.patch("/update")
async def update_company(
    schema: UpdateCompany,
    db: Session = Depends(get_db)
):
    
    if not db.query(Company).filter(Company.id == schema.id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return await company_service.update_company(db, schema)

@company_routes.delete("/delete")
async def delete_company(
    id: int,
    db: Session = Depends(get_db)
):  
    if not db.query(Company).filter(Company.id == id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return await company_service.delete_company(db, id)
    