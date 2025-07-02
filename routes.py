from fastapi import FastAPI

from src.controllers.user_controller import user_routes

app = FastAPI()

app.include_router(user_routes, prefix='/users', tags=['users'])