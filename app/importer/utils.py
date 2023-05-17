import csv

from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker, Base
from app.logger import logger


async def import_from_csv(
    table_name: str,
    file_path: str,
):
    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        values = []
        for row in reader:
            for key, item in row.items():
                row[key] = eval(item)
                if item.isdigit():
                    row[key] = int(item)
            values.append(row)
        async with async_session_maker() as session:
            try:
                for value in values:
                    query = Base.metadata.tables[table_name].insert().values(value)
                    await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                msg = ""
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc: Error during import"
                elif isinstance(e, Exception):
                    msg = "Unknown Exc: Error during import"
                extra = {"values": values}
                logger.info(msg, extra=extra, exc_info=True)
                await session.rollback()
