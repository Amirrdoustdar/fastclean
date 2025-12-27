import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
class TestProductAPI:

    async def test_create_product(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/products",
            json={
                "name": str(),
                "price": float(),
                "quantity": int(),
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

    async def test_get_product(self, client: AsyncClient):
        # First create
        create_response = await client.post(
            "/api/v1/products",
            json={
                "name": str(),
                "price": float(),
                "quantity": int(),
            },
        )
        created_id = create_response.json()["id"]

        # Then get
        response = await client.get(f"/api/v1/products/{created_id}")
        assert response.status_code == 200

    async def test_get_product_not_found(self, client: AsyncClient):
        response = await client.get("/api/v1/products/99999")
        assert response.status_code == 404

    async def test_list_products(self, client: AsyncClient):
        response = await client.get("/api/v1/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_delete_product(self, client: AsyncClient):
        # First create
        create_response = await client.post(
            "/api/v1/products",
            json={
                "name": str(),
                "price": float(),
                "quantity": int(),
            },
        )
        created_id = create_response.json()["id"]

        # Then delete
        response = await client.delete(f"/api/v1/products/{created_id}")
        assert response.status_code == 204
