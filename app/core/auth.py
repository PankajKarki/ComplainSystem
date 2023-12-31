import jwt
from decouple import config
from typing import Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from app.db.init_db import database
from app.models import user, RoleType


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user['id'],
                "exp":  datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            # log exception
            raise ex
        


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, config("SECRET_KEY"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")
        

oauth2_scheme = CustomHTTPBearer()

def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
        

def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    

def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
