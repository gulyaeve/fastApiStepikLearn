
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from app.config import settings
from app.users.router import router as users_router
from app.bookings.router import router as booking_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
