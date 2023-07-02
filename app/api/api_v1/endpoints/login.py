from fastapi import APIRouter
from app.schemas.user_schema import UserLogIn
from app.crud.crud_user import CrudUser

auth_router = APIRouter()

@auth_router.post("/login/access-token", status_code=201)
async def login_access_token(user_data: UserLogIn):
    token = await CrudUser.authenticate(user_data.dict())
    return {"token": token}