from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
# from env import MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB
from src.models import __all__

# MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
MONGO_URI = f"mongodb://localhost:27017"

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["FIVE_BACK_END"]

    await init_beanie(database, document_models=__all__)
