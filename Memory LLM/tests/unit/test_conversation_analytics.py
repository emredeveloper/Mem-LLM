import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock

import pytest

from mem_llm.conversation_analytics import ConversationAnalytics
from mem_llm.memory_manager import MemoryManager


class TestConversationAnalytics:
    @pytest.fixture
    def mock_memory_manager(self):
        manager = Mock(spec=MemoryManager)
        return manager

    @pytest.fixture
    def analytics(self, mock_memory_manager):
        return ConversationAnalytics(mock_memory_manager)

    @pytest.fixture
    def sample_data(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        return {
            "conversations": [
                {
                    "timestamp": yesterday.isoformat(),
                    "user_message": "Hello, how are you?",
                    "bot_response": "I am fine, thank you.",
                    "metadata": {},
                },
                {
                    "timestamp": now.isoformat(),
                    "user_message": "Tell me about Python programming.",
                    "bot_response": "Python is a great language.",
                    "metadata": {},
                },
                {
                    "timestamp": now.isoformat(),
                    "user_message": "What is a variable in Python?",
                    "bot_response": "A variable stores data.",
                    "metadata": {},
                },
            ],
            "profile": {},
        }

    def test_get_conversation_stats(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        stats = analytics.get_conversation_stats("user1")

        assert stats["total_messages"] == 6  # 3 user + 3 bot
        assert stats["user_messages"] == 3
        assert stats["assistant_messages"] == 3
        assert stats["total_conversations"] == 3
        assert stats["most_active_day"] is not None
        assert stats["first_interaction"] is not None
        assert stats["last_interaction"] is not None

    def test_get_conversation_stats_empty(self, analytics, mock_memory_manager):
        mock_memory_manager.load_memory.return_value = {"conversations": []}

        stats = analytics.get_conversation_stats("user1")

        assert stats["total_messages"] == 0
        assert stats["total_conversations"] == 0
        assert stats["avg_message_length"] == 0.0

    def test_get_topic_distribution(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        topics = analytics.get_topic_distribution("user1")

        # "python" should be a topic
        assert "python" in topics
        assert topics["python"] >= 2

        # Stop words should be filtered
        assert "the" not in topics
        assert "is" not in topics

    def test_get_engagement_metrics(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        metrics = analytics.get_engagement_metrics("user1")

        assert metrics["active_days"] >= 1
        assert metrics["engagement_score"] > 0
        assert metrics["avg_session_length"] > 0

    def test_get_time_distribution(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        dist = analytics.get_time_distribution("user1")

        assert len(dist) == 24
        # Check if total count matches total conversations
        total_count = sum(dist.values())
        assert total_count == 3

    def test_export_report_json(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        json_report = analytics.export_report("user1", format="json")
        data = json.loads(json_report)

        assert data["user_id"] == "user1"
        assert "statistics" in data
        assert "topics" in data
        assert "engagement" in data

    def test_export_report_markdown(self, analytics, mock_memory_manager, sample_data):
        mock_memory_manager.load_memory.return_value = sample_data

        md_report = analytics.export_report("user1", format="markdown")

        assert "# Analytics Report for user1" in md_report
        assert "## General Statistics" in md_report
        assert "## Top Topics" in md_report

    def test_export_report_invalid_format(self, analytics, mock_memory_manager):
        mock_memory_manager.load_memory.return_value = {}

        with pytest.raises(ValueError):
            analytics.export_report("user1", format="invalid")
