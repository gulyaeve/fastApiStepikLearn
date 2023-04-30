from fastapi import HTTPException, status


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User exists",
)


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong email or password",
)


TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No token",
)


TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expired token",
)


IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong token format",
)


UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)


RoomCanNotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Нет свободных номеров"
)


BookingNotExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Бронирование не найдено"
)