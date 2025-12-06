import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_create_user():
    """Test creating user via API"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users/",
            json={"email": "test@example.com", "username": "testuser"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user():
    """Test getting user via API"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create user first
        create_response = await client.post(
            "/api/v1/users/",
            json={"email": "test2@example.com", "username": "testuser2"}
        )
        user_id = create_response.json()["id"]
        
        # Get user
        response = await client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id