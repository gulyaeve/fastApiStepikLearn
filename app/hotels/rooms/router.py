from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms

from app.hotels.router import router as hotels_router


router = APIRouter(
    prefix=f"{hotels_router.prefix}/rooms",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    return await RoomsDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
