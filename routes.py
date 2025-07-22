from fastapi import FastAPI

from src.controllers.user_controller import user_routes
from src.controllers.company_controller import company_routes

app = FastAPI()

app.include_router(user_routes, prefix='/users', tags=['users'])
app.include_router(company_routes, prefix='/companies', tags=['companies'])