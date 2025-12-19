"""
Memory Manager - Memory Management System
Stores, updates and remembers user interactions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class MemoryManager:
    """Memory system that manages user interactions and context"""

    def __init__(self, memory_dir: str = "memories"):
        """
        Args:
            memory_dir: Directory where memory files will be stored
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        self.conversations: Dict[str, List[Dict]] = {}
        self.user_profiles: Dict[str, Dict] = {}

    def _get_user_file(self, user_id: str) -> Path:
        """Returns the path of user's memory file"""
        return self.memory_dir / f"{user_id}.json"

    def load_memory(self, user_id: str) -> Dict:
        """
        Load user's memory

        Args:
            user_id: User ID

        Returns:
            User's memory data
        """
        user_file = self._get_user_file(user_id)

        if user_file.exists():
            with open(user_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations[user_id] = data.get("conversations", [])
                profile = data.get("profile", {})

                # Parse preferences if it's a JSON string (legacy format)
                if isinstance(profile.get("preferences"), str):
                    try:
                        profile["preferences"] = json.loads(profile["preferences"])
                    except (ValueError, json.JSONDecodeError):
                        profile["preferences"] = {}

                self.user_profiles[user_id] = profile
                return data
        else:
            # Create empty memory for new user
            self.conversations[user_id] = []
            self.user_profiles[user_id] = {
                "user_id": user_id,
                "first_seen": datetime.now().isoformat(),
                "preferences": {},
                "summary": {},
            }
            return {"conversations": [], "profile": self.user_profiles[user_id]}

    def save_memory(self, user_id: str) -> None:
        """
        Save user's memory to disk

        Args:
            user_id: User ID
        """
        user_file = self._get_user_file(user_id)

        data = {
            "conversations": self.conversations.get(user_id, []),
            "profile": self.user_profiles.get(user_id, {}),
            "last_updated": datetime.now().isoformat(),
        }

        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_interaction(
        self, user_id: str, user_message: str, bot_response: str, metadata: Optional[Dict] = None
    ) -> None:
        """
        Record a new interaction

        Args:
            user_id: User ID
            user_message: User's message
            bot_response: Bot's response
            metadata: Additional information (order no, issue type, etc.)
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "metadata": metadata or {},
        }

        self.conversations[user_id].append(interaction)
        self.save_memory(user_id)

    # Alias for compatibility
    def add_conversation(
        self, user_id: str, user_message: str, bot_response: str, metadata: Optional[Dict] = None
    ) -> None:
        """Alias for add_interaction"""
        return self.add_interaction(user_id, user_message, bot_response, metadata)

    def update_profile(self, user_id: str, updates: Dict) -> None:
        """
        Update user profile

        Args:
            user_id: User ID
            updates: Information to update
        """
        if user_id not in self.user_profiles:
            self.load_memory(user_id)

        self.user_profiles[user_id].update(updates)
        self.save_memory(user_id)

    def get_recent_conversations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """
        Get last N conversations

        Args:
            user_id: User ID
            limit: Number of conversations to retrieve

        Returns:
            List of recent conversations
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        return self.conversations[user_id][-limit:]

    def search_memory(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Search for keyword in memory

        Args:
            user_id: User ID
            keyword: Word to search for

        Returns:
            Matching interactions
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        results = []
        keyword_lower = keyword.lower()

        for interaction in self.conversations[user_id]:
            if (
                keyword_lower in interaction["user_message"].lower()
                or keyword_lower in interaction["bot_response"].lower()
                or keyword_lower in str(interaction.get("metadata", {})).lower()
            ):
                results.append(interaction)

        return results

    def get_summary(self, user_id: str) -> str:
        """
        Create summary of user's past interactions

        Args:
            user_id: User ID

        Returns:
            Summary text
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        profile = self.user_profiles.get(user_id, {})
        conversations = self.conversations.get(user_id, [])

        if not conversations:
            return "No interactions with this user yet."

        summary_parts = [
            f"User ID: {user_id}",
            f"First conversation: {profile.get('first_seen', 'Unknown')}",
            f"Total interactions: {len(conversations)}",
        ]

        # Add last 3 interactions
        if conversations:
            summary_parts.append("\nRecent interactions:")
            for i, conv in enumerate(conversations[-3:], 1):
                timestamp = conv.get("timestamp", "Unknown")
                user_msg = conv.get("user_message", "")[:50]
                summary_parts.append(f"{i}. {timestamp}: {user_msg}...")

        # Metadata summary
        all_metadata = [c.get("metadata", {}) for c in conversations if c.get("metadata")]
        if all_metadata:
            summary_parts.append("\nSaved information:")
            # Example: order numbers, issues, etc.
            for meta in all_metadata[-3:]:
                for key, value in meta.items():
                    summary_parts.append(f"  - {key}: {value}")

        return "\n".join(summary_parts)

    def clear_memory(self, user_id: str) -> None:
        """
        Completely delete user's memory

        Args:
            user_id: User ID
        """
        user_file = self._get_user_file(user_id)
        if user_file.exists():
            user_file.unlink()

        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self.user_profiles:
            del self.user_profiles[user_id]

    def search_conversations(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Search for keyword in conversations (for JSON version)

        Args:
            user_id: User ID
            keyword: Word to search for

        Returns:
            Matching conversations
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        results = []
        keyword_lower = keyword.lower()

        for interaction in self.conversations.get(user_id, []):
            if (
                keyword_lower in interaction["user_message"].lower()
                or keyword_lower in interaction["bot_response"].lower()
            ):
                results.append(interaction)

        return results

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile (for JSON version)

        Args:
            user_id: User ID

        Returns:
            User profile or None
        """
        if user_id not in self.user_profiles:
            self.load_memory(user_id)

        return self.user_profiles.get(user_id)

    def update_user_profile(self, user_id: str, updates: Dict) -> None:
        """
        Update user profile (SQL-compatible alias)

        Args:
            user_id: User ID
            updates: Fields to update
        """
        return self.update_profile(user_id, updates)

    def add_user(
        self, user_id: str, name: Optional[str] = None, metadata: Optional[Dict] = None
    ) -> None:
        """
        Add or update user (SQL-compatible method)

        Args:
            user_id: User ID
            name: User name (optional)
            metadata: Additional metadata (optional)
        """
        self.load_memory(user_id)
        if name and "name" not in self.user_profiles[user_id]:
            self.user_profiles[user_id]["name"] = name
        if metadata:
            self.user_profiles[user_id].update(metadata)
        self.save_memory(user_id)

    def get_statistics(self) -> Dict:
        """
        Get general statistics (SQL-compatible method)

        Returns:
            Statistics dictionary
        """
        all_users = list(self.memory_dir.glob("*.json"))
        total_interactions = 0

        for user_file in all_users:
            try:
                with open(user_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    total_interactions += len(data.get("conversations", []))
            except (ValueError, json.JSONDecodeError, OSError):
                pass

        return {
            "total_users": len(all_users),
            "total_interactions": total_interactions,
            "knowledge_base_entries": 0,  # JSON doesn't have KB
        }
