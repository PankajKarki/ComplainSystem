from pydantic import BaseModel
from app.models import RoleType

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str

class UserLogIn(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    phone: str
    first_name: str
    last_name: str
    role: RoleType
    iban: str

