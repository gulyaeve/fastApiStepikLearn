import datetime
from datetime import date

from fastapi import APIRouter

from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    max_days = datetime.timedelta(days=30)
    if date_to <= date_from:
        raise DateFromCannotBeAfterDateTo
    if date_to - date_from > max_days:
        raise CannotBookHotelForLongPeriod
    return await HotelsDAO.find_all(location=location, date_from=date_from, date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
