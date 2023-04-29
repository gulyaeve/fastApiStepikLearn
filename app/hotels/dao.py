import asyncio
import datetime
from datetime import date
from operator import and_

from sqlalchemy import select, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    """
    WITH booked_rooms AS (
        SELECT bookings.id, room_id, date_from, date_to, rooms.hotel_id FROM bookings
        JOIN rooms ON bookings.room_id = rooms.id
        WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
    )
    SELECT hotels.*, hotels.rooms_quantity - COUNT(booked_rooms.hotel_id) AS left_rooms FROM hotels
    JOIN rooms ON hotels.id = rooms.hotel_id
    LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
    WHERE Lower(hotels.location) like Lower('%АлТАй%')
    GROUP BY hotels.id
    """
    @classmethod
    async def find_all(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(
                Bookings.id,
                Bookings.room_id,
                Bookings.date_from,
                Bookings.date_to,
                Rooms
            ).select_from(Bookings).join(Rooms, Bookings.room_id == Rooms.id).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    ),
                )
            ).cte("booked_rooms")

            get_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (Hotels.rooms_quantity - func.count(booked_rooms.c.hotel_id)).label("left_rooms")
            ).select_from(Hotels).join(
                Rooms, Hotels.id == Rooms.hotel_id
            ).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).where(
                func.lower(Hotels.location).contains(location.lower())
            ).group_by(
                Hotels.id
            )
            # print(get_hotels.compile(engine, compile_kwargs={'literal_binds': True}))
            hotels = await session.execute(get_hotels)
            # print(hotels)
            return hotels.all()


if __name__ == "__main__":
    asyncio.run(HotelsDAO.find_all("АлтАй", datetime.date(2023, 5, 15), datetime.date(2023, 6, 20)))
