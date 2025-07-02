from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
from fastapi.middleware.cors import CORSMiddleware
import sys
from routes import app

sys.dont_write_bytecode = True

logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "details": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )
