import pytest
from fastapi import status
from unittest.mock import AsyncMock
from sqlalchemy import select
from src.database.models import User
from src.utils.password import get_password_hash
from tests.conftest import TestingSessionLocal

user_data = {"username": "agent007", "email": "agent007@gmail.com", "password": "12345678"}



def test_register_user(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("auth/register", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "password" not in data

def test_repeat_register(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("auth/register", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Email already registered"

# @pytest.mark.asyncio
# async def test_login_user(client):
#     async with TestingSessionLocal() as session:
#         current_user = await session.execute(select(User).where(User.email == user_data.get("email")))
#         current_user = current_user.scalar_one_or_none()
#         if current_user:
#             current_user.confirmed = True
#             await session.commit()

#     response = client.post("auth/login",
#                            data={"username": user_data.get("email"), "password": user_data.get("password")})
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert "access_token" in data
#     assert "refresh_token" in data
#     assert "token_type" in data


# def test_wrong_password_login(client):
#     response = client.post("auth/login",
#                            data={"username": user_data.get("email"), "password": "password"})
#     assert response.status_code == 401, response.text
#     data = response.json()
#     assert data["detail"] == "Incorrect email or password"


# def test_wrong_email_login(client):
#     response = client.post("auth/login",
#                            data={"username": "email", "password": user_data.get("password")})
#     assert response.status_code == 401, response.text
#     data = response.json()
#     assert data["detail"] == "Incorrect email or password"


# def test_validation_error_login(client):
#     response = client.post("auth/login",
#                            data={"password": user_data.get("password")})
#     assert response.status_code == 422, response.text
#     data = response.json()
#     assert "detail" in data
    

# async def test_read_users_me(client, monkeypatch):
#     async def mock_get_current_user():
#         return User(id=1, email="deadpool@example.com", hashed_password="hashedpassword", is_verified=True)

#     monkeypatch.setattr('src.routes.auth.user.get_current_user', mock_get_current_user)

#     response = client.get("/users/me/")
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["email"] == "deadpool@example.com"