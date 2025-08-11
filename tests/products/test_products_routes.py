import pytest
from fastapi import status
from httpx import AsyncClient


async def create_user_and_get_token(
    client: AsyncClient, email: str, password: str
) -> str:
    user_data = {"email": email, "password": password}
    await client.post("/api/v1/auth/register", json=user_data)
    login_data = {"username": email, "password": password}
    response = await client.post("/api/v1/auth/login", data=login_data)
    return response.json()["access_token"]


@pytest.mark.anyio
class TestCreateProduct:
    async def test_successfully(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "create_success@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {
            "name": "Test Product",
            "description": "This is a test product.",
            "price": 9.99,
        }
        response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Product"

    async def test_unauthenticated(self, client: AsyncClient):
        product_data = {"name": "Unauth Product", "price": 9.99}
        response = await client.post("/api/v1/products/", json=product_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            ({"description": "Missing name", "price": 10.0}),
            ({"name": "Missing price", "description": "A description"}),
            ({"name": "Invalid Price", "price": -1.0}),
        ],
    )
    async def test_invalid_data(self, client: AsyncClient, invalid_payload: dict):
        token = await create_user_and_get_token(
            client, "create_invalid@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            "/api/v1/products/", json=invalid_payload, headers=headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
class TestReadProduct:
    async def test_get_all_for_user(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "get_all@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {"name": "My Product", "price": 19.99}
        await client.post("/api/v1/products/", json=product_data, headers=headers)
        response = await client.get("/api/v1/products/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "My Product"

    async def test_get_one_successfully(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "get_one_success@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {"name": "Specific Product", "price": 29.99}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers
        )
        product_id = create_response.json()["id"]
        response = await client.get(f"/api/v1/products/{product_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Specific Product"

    async def test_get_one_not_found(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "get_one_notfound@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(
            "/api/v1/products/60d5ec49e7a4a62c3d4d7e9a", headers=headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_one_forbidden(self, client: AsyncClient):
        token1 = await create_user_and_get_token(
            client, "get_one_forbidden1@example.com", "password123"
        )
        headers1 = {"Authorization": f"Bearer {token1}"}
        product_data = {"name": "User 1 Product", "price": 10.00}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers1
        )
        product_id = create_response.json()["id"]
        token2 = await create_user_and_get_token(
            client, "get_one_forbidden2@example.com", "password123"
        )
        headers2 = {"Authorization": f"Bearer {token2}"}
        response = await client.get(f"/api/v1/products/{product_id}", headers=headers2)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
class TestUpdateProduct:
    async def test_successfully(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "update_success@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {"name": "Original Name", "price": 10.00}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers
        )
        product_id = create_response.json()["id"]
        update_data = {"name": "Updated Name", "price": 20.00}
        response = await client.put(
            f"/api/v1/products/{product_id}", json=update_data, headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"

    async def test_forbidden(self, client: AsyncClient):
        token1 = await create_user_and_get_token(
            client, "update_forbidden1@example.com", "password123"
        )
        headers1 = {"Authorization": f"Bearer {token1}"}
        product_data = {"name": "User 1 Product", "price": 10.00}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers1
        )
        product_id = create_response.json()["id"]
        token2 = await create_user_and_get_token(
            client, "update_forbidden2@example.com", "password123"
        )
        headers2 = {"Authorization": f"Bearer {token2}"}
        update_data = {"name": "Attempted Update"}
        response = await client.put(
            f"/api/v1/products/{product_id}", json=update_data, headers=headers2
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_not_found(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "update_notfound@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {"name": "Updated Name"}
        response = await client.put(
            "/api/v1/products/60d5ec49e7a4a62c3d4d7e9a",
            json=update_data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_invalid_data(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "update_invalid@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {"name": "Original", "price": 10.0}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers
        )
        product_id = create_response.json()["id"]
        invalid_update_data = {"price": -5.0}
        response = await client.put(
            f"/api/v1/products/{product_id}", json=invalid_update_data, headers=headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
class TestDeleteProduct:
    async def test_successfully(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "delete_success@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        product_data = {"name": "To Be Deleted", "price": 5.00}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers
        )
        product_id = create_response.json()["id"]
        delete_response = await client.delete(
            f"/api/v1/products/{product_id}", headers=headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        get_response = await client.get(
            f"/api/v1/products/{product_id}", headers=headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    async def test_forbidden(self, client: AsyncClient):
        token1 = await create_user_and_get_token(
            client, "delete_forbidden1@example.com", "password123"
        )
        headers1 = {"Authorization": f"Bearer {token1}"}
        product_data = {"name": "User 1 Product", "price": 10.00}
        create_response = await client.post(
            "/api/v1/products/", json=product_data, headers=headers1
        )
        product_id = create_response.json()["id"]
        token2 = await create_user_and_get_token(
            client, "delete_forbidden2@example.com", "password123"
        )
        headers2 = {"Authorization": f"Bearer {token2}"}
        response = await client.delete(
            f"/api/v1/products/{product_id}", headers=headers2
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_not_found(self, client: AsyncClient):
        token = await create_user_and_get_token(
            client, "delete_notfound@example.com", "password123"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.delete(
            "/api/v1/products/60d5ec49e7a4a62c3d4d7e9a", headers=headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
