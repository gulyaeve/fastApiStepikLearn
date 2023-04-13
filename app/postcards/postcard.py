from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Postcard(Base):
    __tablename__ = "postcards"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)
