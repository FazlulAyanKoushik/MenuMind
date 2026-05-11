import pytest


@pytest.mark.asyncio
async def test_health_endpoint():
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
