from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from app.users.router import router as users_router
from app.bookings.router import router as booking_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router

app = FastAPI()

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
