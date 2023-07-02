# ComplainSystem/app/core/config.py


import logging
from functools import lru_cache
from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Complaint System"
    ENVIRONMENT: str = "dev"
    TESTING: bool = bool(0)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# @lru_cache()
# def get_settings() -> BaseSettings:
#     log.info("Loading config settings from the environment...")
#     return Settings()
