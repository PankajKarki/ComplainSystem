from fastapi import FastAPI, Depends
from app.db.init_db import database
from app.core.config import Settings, settings
from app.api.api_v1.routes import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @app.get("/ping")
# async def pong(settings: Settings = Depends(get_settings)):
#     return {
#         "ping": "pong!",
#         "environment": settings.ENVIRONMENT,
#         "testing": settings.TESTING
#     }
