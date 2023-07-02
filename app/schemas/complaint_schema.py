from datetime import datetime
from pydantic import BaseModel
from app.models import State

class ComplaintBase(BaseModel):
    title: str
    description: str
    amount: float

class ComplaintIn(ComplaintBase):
    encoded_photo: str
    extention: str

class ComplaintOut(ComplaintBase):
    id: int
    photo_url: str
    created_at: datetime
    status: State
