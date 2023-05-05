import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pies.com", "kotpies", 200),
    ("kot@pies.com", "kopies", 409),
    ("pes@kot.com", "pesocot", 200),
    ("abcde", "kot0pies", 422),
])
async def test_register_user(email, password, status_code: int, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
