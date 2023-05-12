from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 201),
    (4, "2030-05-02", "2030-05-16", 4, 201),
    (4, "2030-05-03", "2030-05-17", 5, 201),
    (4, "2030-05-04", "2030-05-18", 6, 201),
    (4, "2030-05-05", "2030-05-19", 7, 201),
    (4, "2030-05-06", "2030-05-20", 8, 201),
    (4, "2030-05-07", "2030-05-21", 9, 201),
    (4, "2030-05-08", "2030-05-22", 10, 201),
    (4, "2030-05-09", "2030-05-23", 10, 409),
    (4, "2030-05-10", "2030-05-24", 10, 409),
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        booked_rooms,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    print(response.json())
    assert response.status_code == status_code

    # Необходимо добавить эндпоинт для получения бронирований
    response = await authenticated_ac.get("/bookings/get")
    print(f"{len(response.json())=} {booked_rooms=}")
    assert len(response.json()) == booked_rooms


@pytest.mark.parametrize("room_id,date_from,date_to,status_code_create,status_code_read,status_code_delete,"
                         "status_code_check", [
                             (5, "2030-05-01", "2030-05-15", 201, 200, 200, 409),
                         ])
async def test_crud_booking(
        room_id,
        date_from,
        date_to,
        status_code_create,
        status_code_read,
        status_code_delete,
        status_code_check,
        authenticated_ac: AsyncClient,
):
    # создание бронирования
    new_booking = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    print(f"{new_booking.json()=}")
    assert new_booking.status_code == status_code_create

    if new_booking.status_code == status_code_create:
        # получение бронирования
        booking = await authenticated_ac.get(f"/bookings/get/{new_booking.json()['id']}")
        print(f"{booking.json()=}")
        assert booking.status_code == status_code_read
        assert booking.json()['id'] == new_booking.json()['id']

        # удаление бронирования
        response_del = await authenticated_ac.delete(f"/bookings/{booking.json()['id']}")
        print(response_del.status_code)
        assert response_del.status_code == status_code_delete

        # проверка удаления
        response_check = await authenticated_ac.get(f"/bookings/get/{booking.json()['id']}")
        print(response_check.status_code)
        assert response_check.status_code == status_code_check
