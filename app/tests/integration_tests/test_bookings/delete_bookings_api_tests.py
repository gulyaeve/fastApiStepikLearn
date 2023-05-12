from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("status_code", [
    200,
])
async def test_get_and_delete_booking(
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.get("/bookings/get")
    print(response.json())
    assert response.status_code == status_code

    for booking in response.json():
        response_del = await authenticated_ac.delete(f"/bookings/{booking['id']}")
        print(response_del.status_code)
        assert response_del.status_code == status_code

    response = await authenticated_ac.get("/bookings/get")
    print(response.json())
    print(f"{len(response.json())=}")
    assert len(response.json()) == 0
