from typing import List
from fastapi import APIRouter, dependencies, Depends
from starlette.requests import Request
from app.core.auth import oauth2_scheme, is_complainer, is_admin, is_approver
from app.schemas.complaint_schema import ComplaintIn, ComplaintOut
from app.crud.crud_complaint import CrudComplaint

complain_router = APIRouter()

@complain_router.get("/", dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return  await CrudComplaint.get_complaints(user)


@complain_router.post("/create/", 
                      dependencies=[Depends(oauth2_scheme), Depends(is_complainer)], 
                      response_model=ComplaintOut)
async def create_complaints(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return  await CrudComplaint.create_complaint(complaint.dict(), user)


@complain_router.delete("/{complaint_id}",
                        dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
                        status_code=204)
async def delete_complaint(complaint_id: int):
    await CrudComplaint.delete_complaint(complaint_id)


@complain_router.put("/{complaint_id}/approve",
                     dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
                     status_code=204)
async def approve_complaint(complaint_id: int):
    await CrudComplaint.approve(complaint_id)


@complain_router.put("/{complaint_id}/reject",
                     dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
                     status_code=204)
async def reject_complaint(complaint_id: int):
    await CrudComplaint.reject(complaint_id)