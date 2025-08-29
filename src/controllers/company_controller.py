from database_connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from src.models.company_model import Company
from src.schemas.company_schema import CreateCompany, CompanyResponse, UpdateCompany
from sqlalchemy.orm import Session
from src.services.company_service import CompanyService
from auth import get_current_user
from starlette import status


company_routes = APIRouter(
    # dependencies=[Depends(get_current_user)]
    )
company_service = CompanyService()

@company_routes.post("/register")
async def create_company(
    schema: CreateCompany,
):
    return await company_service.create_company(schema)

@company_routes.get("/list")
async def list_companies(
    limit: int = 10,
    skip: int = None, 
):  
    return await company_service.list_companies(limit, skip)

@company_routes.get("/details/{id}")
async def details_company(
    id: str,
):
    return await company_service.detail_company(id)

@company_routes.patch("/update")
async def update_company(
    schema: UpdateCompany,
):
    return await company_service.update_company(schema)

@company_routes.delete("/delete")
async def delete_company(
    id: int,
):  
    return await company_service.delete_company(id)
    