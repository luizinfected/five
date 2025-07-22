
from fastapi import HTTPException
from src.models.company_model import Company
from src.schemas.company_schema import CreateCompany, CompanyResponse, UpdateCompany
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

class CompanyService:

    async def create_company(
        self, 
        db: Session,
        schema: CreateCompany
    ):
        
        company_data = schema.model_dump()

        company = Company(**company_data)

        db.add(company)
        db.commit()
        db.refresh(company)

        

        return company_data
    
    async def list_companies(
        self, 
        db: Session,
    ):
        
        companies = db.query(Company).all()

        return companies

    async def detail_company(
        self, 
        db: Session,
        id: int
    ):
        
        company = db.query(Company).filter(Company.id == id).first()

        return company

    async def update_company(
        self, 
        db: Session,
        schema: UpdateCompany
    ):
        
        company = db.query(Company).filter(Company.id == schema.id).first()

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        company_data = schema.model_dump(exclude_unset=True)

        for key, value in company_data.items():
            setattr(company, key, value)

        db.add(company)
        db.commit()
        db.refresh(company)

        return company
    
    async def delete_company(
        self, 
        db: Session,
        id: int
    ):
        
        company = db.query(Company).filter(Company.id == id).first()

        db.delete(company)
        db.commit()

        return {"message": "Company deleted"}