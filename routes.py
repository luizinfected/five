from fastapi import FastAPI
from db import init_db
from src.controllers.user_controller import user_routes
from src.controllers.company_controller import company_routes

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(user_routes, prefix='/users', tags=['users'])
app.include_router(company_routes, prefix='/companies', tags=['companies'])