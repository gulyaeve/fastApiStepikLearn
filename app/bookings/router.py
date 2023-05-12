from datetime import date

from fastapi import APIRouter, Request, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCanNotBeBooked, BookingNotExists
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/get")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all_to_user(user_id=user.id)


@router.get("/get/{booking_id}")
async def get_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not booking:
        raise BookingNotExists
    return booking


@router.post("", status_code=201)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked
    return booking


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if not booking:
        raise BookingNotExists
    else:
        await BookingDAO.delete(id=booking_id, user_id=user.id)
