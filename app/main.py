from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from app.bookings.router import router as booking_router

app = FastAPI()

app.include_router(booking_router)


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
