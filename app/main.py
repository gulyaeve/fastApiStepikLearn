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


class SPostcard(BaseModel):
    id: int
    name: str
    date_created: datetime


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/postcard")
async def add_postcard(postcard_data: SPostcard):
    return postcard_data.dict()
