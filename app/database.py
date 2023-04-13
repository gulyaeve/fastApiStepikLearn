from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import Config

DBConfig = Config.DBConfig

DATABASE_URL = f"postgresql+asyncpg://{DBConfig.DB_USER}:{DBConfig.DB_PASS}" \
               f"@{DBConfig.DB_HOST}:{DBConfig.DB_PORT}/{DBConfig.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

asynch_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
