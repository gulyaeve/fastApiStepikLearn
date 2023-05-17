import datetime
import shutil

from fastapi import APIRouter, UploadFile, Depends

from app.exceptions import UserIsNotPresentException
from app.importer.utils import import_from_csv
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/import",
    tags=["Импорт"],
)


@router.post("/{table_name}", status_code=201)
async def import_csv(table_name: str, file: UploadFile,  user: Users = Depends(get_current_user)):
    if user:
        file_path = f"app/static/csv/{table_name}_{datetime.datetime.now()}.csv"
        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        await import_from_csv(table_name, file_path)
    else:
        raise UserIsNotPresentException

