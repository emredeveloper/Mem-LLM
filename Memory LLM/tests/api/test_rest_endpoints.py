"""
API endpoint tests for REST API
"""

import pytest
from fastapi.testclient import TestClient

from mem_llm.api_server import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.mark.api
class TestChatEndpoints:
    """Tests for chat API endpoints"""

    def test_chat_endpoint(self, client):
        """Test basic chat endpoint"""
        response = client.post(
            "/api/v1/chat",
            json={"user_id": "test_user", "message": "Hello, test!", "return_metrics": False},
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert data["user_id"] == "test_user"

    def test_chat_with_metrics(self, client):
        """Test chat endpoint with metrics"""
        response = client.post(
            "/api/v1/chat",
            json={"user_id": "test_user", "message": "Test message", "return_metrics": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert "confidence" in data or "text" in data


@pytest.mark.api
class TestMemoryEndpoints:
    """Tests for memory management endpoints"""

    def test_get_user_profile(self, client):
        """Test getting user profile"""
        response = client.get("/api/v1/memory/profile/test_user")
        assert response.status_code in [200, 404]  # User may not exist yet

    def test_search_memories(self, client):
        """Test memory search endpoint"""
        response = client.get(
            "/api/v1/memory/search", params={"user_id": "test_user", "keyword": "test", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.api
class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "api"])
