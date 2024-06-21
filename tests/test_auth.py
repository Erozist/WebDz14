import pytest
from unittest.mock import AsyncMock, Mock
from sqlalchemy import select
from src.database.models import User
from src.utils.utils import create_access_token
from tests.conftest import TestingSessionLocal

user_data = {"username": "agent007", "email": "agent007@gmail.com", "password": "12345678"}

# Тести для реєстрації користувача
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

@pytest.mark.asyncio
async def test_login_user(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).where(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    response = client.post("auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data

# Тест для входу з неправильною паролем
def test_wrong_password_login(client):
    response = client.post("auth/login",
                           data={"username": user_data.get("email"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

# Тест для входу з неправильною електронною поштою
def test_wrong_email_login(client):
    response = client.post("auth/login",
                           data={"username": "email", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

# Тест для помилки валідації під час входу
def test_validation_error_login(client):
    response = client.post("auth/login",
                           data={"password": user_data.get("password")})
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data

# Тест для отримання інформації про поточного користувача
@pytest.mark.asyncio
async def test_read_users_me(client):
    token = create_access_token(data={"sub": user_data["email"]})
    response = client.get("auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "agent007@gmail.com"

# Тест для верифікації електронної пошти
@pytest.mark.asyncio
async def test_verify_email(client):
    token = create_access_token(data={"sub": user_data["email"]})
    response = client.get(f"auth/verify?token={token}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Email verified successfully"

# Тест для завантаження аватара
@pytest.mark.asyncio
async def test_upload_avatar(client, monkeypatch):
    token = create_access_token(data={"sub": user_data["email"]})
    mock_upload_image = Mock(return_value="http://example.com/avatar.png")
    monkeypatch.setattr("src.routes.auth.upload_image", mock_upload_image)
    
    with open("templates/avatar.png", "rb") as avatar_file:
        response = client.post("auth/upload-avatar", files={"file": avatar_file}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["avatar_url"] == "http://example.com/avatar.png"
