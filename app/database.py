from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

# DBConfig = Config.DBConfig

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL)

asynch_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
