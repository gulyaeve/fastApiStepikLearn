from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "hotel_location,date_from,date_to,status_code",
    [
        ("алтай", "2030-05-01", "2030-05-15", 200),
        ("алтай", "2030-05-02", "2030-04-16", 400),
        ("алтай", "2030-05-03", "2030-06-17", 400),
    ],
)
async def test_get_hotels(
    hotel_location,
    date_from,
    date_to,
    status_code,
    ac: AsyncClient,
):
    response = await ac.get(
        f"/hotels/{hotel_location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    print(response.json())
    assert response.status_code == status_code
