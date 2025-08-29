
from beanie import PydanticObjectId
from fastapi import HTTPException
from src.models.company_model import Company
from src.schemas.company_schema import CreateCompany, CompanyResponse, UpdateCompany
from starlette import status
from starlette.responses import JSONResponse

class CompanyService:

    async def create_company(
        self, 
        schema: CreateCompany
    ):  
        company_exist = await Company.find_one(Company.cnpj == schema.cnpj)

        if company_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This CNPJ already exists"
            )
        
        company_data = schema.model_dump()

        company = Company(**company_data)
        await company.insert()

        return company
    
    async def list_companies(
        self, 
        limit,
        skip
    ):
        companies = await Company.find_all().skip(skip).limit(limit).to_list()

        return companies

    async def detail_company(
        self, 
        id: str
    ):

        company = await Company.get(PydanticObjectId(id))

        if not company: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        return company

    async def update_company(
        self, 
        schema: UpdateCompany
    ):  
        company:Company = await Company.find_one(Company.id == schema.id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Company not found"}
            )
        
        if schema.cnpj != company.cnpj:
            return JSONResponse(status_code=409, content={"message": "CNPJ already exists"})
        
        company_data = schema.model_dump(exclude_unset=True)

        

        await company.set(company_data)

        return company
    
    async def delete_company(
        self, 
        id: int
    ):
        
        company: Company = Company.find_one(Company.id == id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Company not found"}
            )
        
        if company.active:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content={"message": "Your Company need to be disabled"}
            )

        company.delete()

        return {"message": "Company deleted"}