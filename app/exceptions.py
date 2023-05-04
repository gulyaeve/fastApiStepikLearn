from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT,
    detail = "User exists",


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Wrong email or password",


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "No token",


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Expired token",


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Wrong token format",


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class RoomCanNotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT,
    detail = "Нет свободных номеров"


class BookingNotExists(BookingException):
    status_code = status.HTTP_409_CONFLICT,
    detail = "Бронирование не найдено"
