import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import UserAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.config import settings
from app.database import engine
from app.logger import logger
from app.users.router import router as users_router
from app.bookings.router import router as booking_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router


sentry_sdk.init(
    dsn="https://d04ff430df104b8fb21745383ff88b16@o4505194654859264.ingest.sentry.io/4505194657611776",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
