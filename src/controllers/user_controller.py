from fastapi import APIRouter, Depends, HTTPException
from database_connection import get_db
from starlette import status
from sqlalchemy.orm import Session
from src.schemas.user_schema import CreateUser, LoginUser
from src.services.user_service import UserService
from src.models.user_model import User

user_routes = APIRouter()
user_service = UserService()


@user_routes.post("/register")
async def create_user(
    schema: CreateUser, 
    db: Session = Depends(get_db)
):
    user_exist = db.query(User).filter(User.email == schema.email).first()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This e-mail already exists"
        )

    if schema.role != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    return await user_service.create_user(db, schema)

@user_routes.post("/login")
async def login(
    schema: LoginUser, 
    db: Session = Depends(get_db)
):  
    
    return await user_service.login(db, schema)

