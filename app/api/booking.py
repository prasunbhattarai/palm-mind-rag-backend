from fastapi import APIRouter
from pydantic import BaseModel

from app.services.booking import create_booking

router = APIRouter()


class BookingRequest(BaseModel):
    name: str
    email: str
    date: str
    time: str


class BookingResponse(BaseModel):
    id: int
    name: str
    email: str
    date: str
    time: str


@router.post("/booking")
def booking(req: BookingRequest):
    result = create_booking(
        name=req.name,
        email=req.email,
        interview_date=req.date,
        interview_time=req.time,
    )
    if "error" in result:
        return result
    return BookingResponse(**result)
