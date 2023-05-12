from datetime import date

from sqlalchemy import select, and_, or_, func, insert
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import RoomFullyBooked
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    """
    WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
    )
    SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
    LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
    WHERE rooms.id = 1
    GROUP BY rooms.quantity, booked_rooms.room_id
    """

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # Рекомендую выводить SQL запрос в консоль для сверки
                # logger.debug(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings.id, Bookings.user_id, Bookings.room_id)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    raise RoomFullyBooked
        except RoomFullyBooked:
            raise RoomFullyBooked
        except (SQLAlchemyError, Exception) as e:
            msg = ""
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            print(f"{msg}, extra={extra}, exc_info=True")
            # logger.error(msg, extra=extra, exc_info=True)
    # @classmethod
    # async def add(
    #         cls,
    #         user_id: int,
    #         room_id: int,
    #         date_from: date,
    #         date_to: date
    # ):
    #     async with async_session_maker() as session:
    #         booked_rooms = select(Bookings).where(
    #             and_(
    #                 Bookings.room_id == 1,
    #                 or_(
    #                     and_(
    #                         Bookings.date_from >= date_from,
    #                         Bookings.date_from <= date_to
    #                     ),
    #                     and_(
    #                         Bookings.date_from <= date_from,
    #                         Bookings.date_to > date_from
    #                     ),
    #                 )
    #             )
    #         ).cte("booked_rooms")
    #
    #         get_rooms_left = select(
    #             (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
    #         ).select_from(Rooms).join(
    #             booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
    #         ).where(Rooms.id == 1).group_by(
    #             Rooms.quantity, booked_rooms.c.room_id
    #         )
    #
    #         # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))
    #
    #         rooms_left = await session.execute(get_rooms_left)
    #         rooms_left = rooms_left.scalar()
    #
    #         if rooms_left > 0:
    #             get_price = select(Rooms.price).filter_by(id=room_id)
    #             price = await session.execute(get_price)
    #             price: int = price.scalar()
    #             add_booking = insert(Bookings).values(
    #                 room_id=room_id,
    #                 user_id=user_id,
    #                 date_from=date_from,
    #                 date_to=date_to,
    #                 price=price,
    #             ).returning(Bookings)
    #
    #             new_booking = await session.execute(add_booking)
    #             await session.commit()
    #             return new_booking.scalar()
    #         else:
    #             return None

    """
    SELECT
        bookings.id,
        bookings.room_id,
        bookings.user_id,
        bookings.date_from,
        bookings.date_to,
        bookings.price,
        bookings.total_cost,
        bookings.total_days,
        rooms.image_id,
        rooms.name,
        rooms.description,
        rooms.services
    FROM bookings
    LEFT JOIN rooms ON bookings.room_id = rooms.id
    WHERE user_id = 3
    """
    @classmethod
    async def find_all_to_user(cls, user_id: int):
        async with async_session_maker() as session:
            get_bookings_for_user = select(
                Bookings.id,
                Bookings.room_id,
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Bookings.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).select_from(Bookings).join(
                Rooms, Bookings.room_id == Rooms.id, isouter=True
            ).where(
                Bookings.user_id == user_id
            )

            bookings_for_user = (await session.execute(get_bookings_for_user)).all()
            # print(bookings_for_user)
            return bookings_for_user
