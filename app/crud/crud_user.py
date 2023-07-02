from fastapi import HTTPException
from asyncpg import UniqueViolationError
from app.db.init_db import database
from app.models import user, RoleType
from app.core.auth import AuthManager
from app.core.security import get_password_hash, verify_password

class CrudUser:
    @staticmethod
    async def create(user_data):
        user_data["password"] = get_password_hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def authenticate(user_data):
        user_do = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        if not user_do:
            raise HTTPException(
                status_code=400,
                detail="Wrong email or password"
            )
        elif not verify_password(user_data["password"], user_do["password"]):
            raise HTTPException(
                status_code=400,
                detail="Wrong email or password"
            )
        return AuthManager.encode_token(user_do)
    

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())
    
    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_all(user.select().where(user.c.email == email))
    
    @staticmethod
    async def change_role(role: RoleType, user_id):
        await database.execute(user.update().where(user.c.id == user_id).values(role=role))


