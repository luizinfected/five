from fastapi import APIRouter, Depends
from database_connection import get_db
from sqlalchemy.orm import Session
from src.schemas.user_schema import CreateUser, LoginUser
from src.services.user_service import UserService

user_routes = APIRouter()
user_service = UserService()


@user_routes.post("/register")
async def create_user(
    schema: CreateUser, 
    db: Session = Depends(get_db)
):
    return await user_service.create_user(db, schema)

@user_routes.post("/login")
async def login(
    schema: LoginUser, 
    db: Session = Depends(get_db)
):  
    return await user_service.login(db, schema)

