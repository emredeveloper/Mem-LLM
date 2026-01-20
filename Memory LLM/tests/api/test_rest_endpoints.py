"""
API endpoint tests for REST API
"""

import pytest
from fastapi.testclient import TestClient

from mem_llm.api_server import app
from mem_llm.api_auth import DEFAULT_API_KEY


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Default auth headers for API requests"""
    return {"X-API-Key": DEFAULT_API_KEY}


@pytest.mark.api
class TestChatEndpoints:
    """Tests for chat API endpoints"""

    def test_chat_endpoint(self, client, auth_headers):
        """Test basic chat endpoint"""
        response = client.post(
            "/api/v1/chat",
            json={"user_id": "test_user", "message": "Hello, test!", "return_metrics": False},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert data["user_id"] == "test_user"

    def test_chat_with_metrics(self, client, auth_headers):
        """Test chat endpoint with metrics"""
        response = client.post(
            "/api/v1/chat",
            json={"user_id": "test_user", "message": "Test message", "return_metrics": True},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "confidence" in data or "text" in data


@pytest.mark.api
class TestMemoryEndpoints:
    """Tests for memory management endpoints"""

    def test_get_user_profile(self, client, auth_headers):
        """Test getting user profile"""
        response = client.get("/api/v1/users/test_user/profile", headers=auth_headers)
        assert response.status_code in [200, 404]  # User may not exist yet

    def test_search_memories(self, client, auth_headers):
        """Test memory search endpoint"""
        response = client.post(
            "/api/v1/memory/search",
            json={"user_id": "test_user", "query": "test", "limit": 10},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "results" in data
        assert isinstance(data["results"], list)


@pytest.mark.api
class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check(self, client, auth_headers):
        """Test health check endpoint"""
        response = client.get("/api/v1/health", headers=auth_headers)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "api"])
