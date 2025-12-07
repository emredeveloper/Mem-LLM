"""
Hierarchical Memory Layers
==========================

Defines the different layers of the hierarchical memory system.
"""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional


class BaseLayer(ABC):
    """Abstract base class for memory layers"""

    def __init__(self, name: str):
        self.name = name
        self.data = {}  # Simple in-memory storage for now, can be extended to DB

    @abstractmethod
    def add(self, item: Dict[str, Any], **kwargs) -> str:
        """Add item to layer"""
        pass

    @abstractmethod
    def get(self, query: Any, **kwargs) -> List[Dict[str, Any]]:
        """Retrieve items from layer"""
        pass

    @abstractmethod
    def clear(self, user_id: Optional[str] = None):
        """Clear layer data"""
        pass


class EpisodeLayer(BaseLayer):
    """
    Bottom layer: Stores raw interactions (Episodes).
    Wraps the existing MemoryManager or SQLMemoryManager.
    """

    def __init__(self, base_memory_manager):
        super().__init__("episode")
        self.base_memory = base_memory_manager

    def add(self, item: Dict[str, Any], **kwargs) -> str:
        """
        Add interaction to base memory.
        Expected item keys: user_id, user_message, bot_response
        """
        user_id = item.get("user_id")
        if not user_id:
            raise ValueError("user_id is required for EpisodeLayer")

        # Use the base memory manager to add interaction
        # This ensures compatibility with existing storage (SQL/JSON)
        if hasattr(self.base_memory, "add_interaction"):
            return self.base_memory.add_interaction(
                user_id=user_id,
                user_message=item.get("user_message", ""),
                bot_response=item.get("bot_response", ""),
                metadata=item.get("metadata"),
            )
        return ""

    def get(self, query: Any, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieve recent episodes.
        kwargs: user_id, limit
        """
        user_id = kwargs.get("user_id")
        limit = kwargs.get("limit", 5)

        if not user_id:
            return []

        if hasattr(self.base_memory, "get_recent_conversations"):
            return self.base_memory.get_recent_conversations(user_id, limit)
        return []

    def clear(self, user_id: Optional[str] = None):
        if user_id and hasattr(self.base_memory, "clear_memory"):
            self.base_memory.clear_memory(user_id)


class TraceLayer(BaseLayer):
    """
    Second layer: Stores memory traces (summarized/abstracted episodes).
    """

    def __init__(self):
        super().__init__("trace")
        # Structure: {user_id: [trace_items]}
        self.traces = {}

    def add(self, item: Dict[str, Any], **kwargs) -> str:
        """
        Add a memory trace.
        item: {user_id, content, original_episode_id, timestamp}
        """
        user_id = item.get("user_id")
        if not user_id:
            return ""

        if user_id not in self.traces:
            self.traces[user_id] = []

        trace_id = f"trace_{str(uuid.uuid4())}"
        trace_item = {
            "id": trace_id,
            "content": item.get("content"),
            "timestamp": datetime.now().isoformat(),
            "original_episode_id": item.get("original_episode_id"),
            "category": item.get("category"),
        }

        self.traces[user_id].append(trace_item)
        return trace_id

    def get(self, query: Any, **kwargs) -> List[Dict[str, Any]]:
        """
        Get traces for user, optionally filtered by category.
        """
        user_id = kwargs.get("user_id")
        category = kwargs.get("category")
        limit = kwargs.get("limit", 10)

        if not user_id or user_id not in self.traces:
            return []

        items = self.traces[user_id]

        if category:
            items = [i for i in items if i.get("category") == category]

        return sorted(items, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def clear(self, user_id: Optional[str] = None):
        if user_id:
            self.traces.pop(user_id, None)
        else:
            self.traces = {}


class CategoryLayer(BaseLayer):
    """
    Third layer: Organizes memories by category.
    Stores aggregated insights per category.
    """

    def __init__(self):
        super().__init__("category")
        # Structure: {user_id: {category_name: {summary, last_updated, interaction_count}}}
        self.categories = {}

    def add(self, item: Dict[str, Any], **kwargs) -> str:
        """
        Update category information.
        item: {user_id, category, summary_update}
        """
        user_id = item.get("user_id")
        category = item.get("category")

        if not user_id or not category:
            return ""

        if user_id not in self.categories:
            self.categories[user_id] = {}

        if category not in self.categories[user_id]:
            self.categories[user_id][category] = {
                "name": category,
                "summary": "",
                "interaction_count": 0,
                "created_at": datetime.now().isoformat(),
            }

        cat_data = self.categories[user_id][category]
        cat_data["interaction_count"] += 1
        cat_data["last_updated"] = datetime.now().isoformat()

        # In a real implementation, we would merge summaries intelligently
        # For now, we append or replace
        new_summary = item.get("summary_update")
        if new_summary:
            cat_data["summary"] = new_summary

        return category

    def get(self, query: Any, **kwargs) -> List[Dict[str, Any]]:
        """Get all categories for user"""
        user_id = kwargs.get("user_id")
        if not user_id or user_id not in self.categories:
            return []

        return list(self.categories[user_id].values())

    def clear(self, user_id: Optional[str] = None):
        if user_id:
            self.categories.pop(user_id, None)
        else:
            self.categories = {}


class DomainLayer(BaseLayer):
    """
    Top layer: High-level domain summaries.
    Broadest context (e.g., "Professional Life", "Hobbies").
    """

    def __init__(self):
        super().__init__("domain")
        # Structure: {user_id: {domain_name: summary}}
        self.domains = {}

    def add(self, item: Dict[str, Any], **kwargs) -> str:
        user_id = item.get("user_id")
        domain = item.get("domain")
        summary = item.get("summary")

        if not user_id or not domain:
            return ""

        if user_id not in self.domains:
            self.domains[user_id] = {}

        self.domains[user_id][domain] = {
            "name": domain,
            "summary": summary,
            "updated_at": datetime.now().isoformat(),
        }
        return domain

    def get(self, query: Any, **kwargs) -> List[Dict[str, Any]]:
        user_id = kwargs.get("user_id")
        if not user_id or user_id not in self.domains:
            return []
        return list(self.domains[user_id].values())

    def clear(self, user_id: Optional[str] = None):
        if user_id:
            self.domains.pop(user_id, None)
        else:
            self.domains = {}
