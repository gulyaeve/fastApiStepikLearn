import asyncio
import datetime
from datetime import date
from operator import and_

from sqlalchemy import select, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    """
    WITH booked_rooms AS (
        SELECT bookings.id, room_id, date_from, date_to, rooms.hotel_id FROM bookings
        JOIN rooms ON bookings.room_id = rooms.id
        WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
    )
    SELECT rooms.*, rooms.quantity - COUNT(booked_rooms.room_id) AS rooms_left FROM rooms
    LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
    WHERE rooms.hotel_id = 1
    GROUP BY rooms.id
    """

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Rooms,
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            total_days: int = (date_to - date_from).days

            get_rooms = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.price,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                    (Rooms.price * total_days).label("total_cost"),
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    ),
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                .where(Rooms.hotel_id == hotel_id)
                .group_by(Rooms.id)
            )

            # print(get_rooms.compile(engine, compile_kwargs={'literal_binds': True}))
            rooms = await session.execute(get_rooms)
            return rooms.all()


if __name__ == "__main__":
    asyncio.run(
        RoomsDAO.find_all(1, datetime.date(2023, 5, 15), datetime.date(2023, 6, 20))
    )
