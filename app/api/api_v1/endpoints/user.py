from typing import Optional, List
from fastapi import APIRouter, dependencies, Depends
from app.models import RoleType
from app.core.auth import oauth2_scheme, is_admin
from app.schemas.user_schema import UserCreate, UserOut
from app.crud.crud_user import CrudUser

user_router = APIRouter()

@user_router.post("/signup/", status_code=201)
async def create_user_signup(user_data: UserCreate):
    token = await CrudUser.create(user_data.dict())
    return {"token": token}


@user_router.get("/", 
                 dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
                 response_model=List[UserOut])
async def get_users(email: Optional[str] = None):
    if email:
        return await CrudUser.get_user_by_email(email)
    return await CrudUser.get_all_users()


@user_router.put("/{user_id}/make_admin",
                 dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
                 status_code=204)
async def make_admin(user_id: int):
    await CrudUser.change_role(RoleType.admin, user_id)


@user_router.put("/{user_id}/make_approver",
                 dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
                 status_code=204)
async def make_approver(user_id: int):
    await CrudUser.change_role(RoleType.approver, user_id)