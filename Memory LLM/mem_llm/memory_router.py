"""
Memory Router
=============

Unifies core memory, archival memory, conversation recall, and knowledge-base
retrieval behind a small API. It wraps existing MemoryManager/SQLMemoryManager
instances so older storage backends keep working.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class MemoryRouter:
    """Route memory reads/writes across core, archival, recall, and KB stores."""

    CORE_METADATA_KEY = "core_memory_blocks"
    ARCHIVAL_CATEGORY = "__archival_memory__"

    def __init__(
        self,
        base_memory,
        graph_store=None,
        max_core_chars: int = 4000,
        recent_limit: int = 5,
    ):
        self.base_memory = base_memory
        self.graph_store = graph_store
        self.max_core_chars = max_core_chars
        self.recent_limit = recent_limit

    def get_core_blocks(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        profile = self._get_profile(user_id) or {}
        metadata = self._decode_json_object(profile.get("metadata"))
        blocks = metadata.get(self.CORE_METADATA_KEY)

        if not blocks:
            blocks = profile.get(self.CORE_METADATA_KEY)
        if isinstance(blocks, str):
            blocks = self._decode_json_object(blocks)
        if not isinstance(blocks, dict):
            blocks = {}

        blocks.setdefault(
            "human",
            {
                "label": "human",
                "description": "Stable facts and preferences about the current user.",
                "value": "",
                "read_only": False,
            },
        )
        blocks.setdefault(
            "session",
            {
                "label": "session",
                "description": "Current working context and recent durable session state.",
                "value": "",
                "read_only": False,
            },
        )
        return blocks

    def set_core_block(
        self,
        user_id: str,
        label: str,
        value: str,
        description: Optional[str] = None,
        read_only: bool = False,
    ) -> None:
        blocks = self.get_core_blocks(user_id)
        current = blocks.get(label, {})
        blocks[label] = {
            "label": label,
            "description": description or current.get("description", ""),
            "value": self._trim(value, self.max_core_chars),
            "read_only": read_only,
            "updated_at": datetime.now().isoformat(),
        }
        self._save_core_blocks(user_id, blocks)

    def search_recall(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if hasattr(self.base_memory, "search_conversations"):
            return self.base_memory.search_conversations(user_id, query)[:limit]
        return []

    def get_recent_conversations(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        if not hasattr(self.base_memory, "get_recent_conversations"):
            return []
        return self.base_memory.get_recent_conversations(user_id, limit or self.recent_limit)

    def add_archival_memory(
        self,
        user_id: str,
        content: str,
        tags: Optional[List[str]] = None,
        priority: int = 0,
    ) -> int:
        if not content.strip():
            return 0

        if hasattr(self.base_memory, "add_knowledge"):
            return self.base_memory.add_knowledge(
                category=self._archival_category(user_id),
                question=f"Memory for {user_id}",
                answer=content.strip(),
                keywords=[user_id] + (tags or []),
                priority=priority,
            )

        profile = self._get_profile(user_id) or {}
        archival = profile.get("archival_memory", [])
        if isinstance(archival, str):
            try:
                archival = json.loads(archival)
            except (ValueError, json.JSONDecodeError):
                archival = []
        if not isinstance(archival, list):
            archival = []

        archival.append(
            {
                "content": content.strip(),
                "tags": tags or [],
                "created_at": datetime.now().isoformat(),
                "priority": priority,
            }
        )
        self._update_profile(user_id, {"archival_memory": archival[-200:]})
        return len(archival)

    def search_archival_memory(
        self, user_id: str, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        if hasattr(self.base_memory, "search_knowledge"):
            results = self.base_memory.search_knowledge(
                query=query,
                category=self._archival_category(user_id),
                limit=limit,
            )
            return results[:limit]

        profile = self._get_profile(user_id) or {}
        archival = profile.get("archival_memory", [])
        if isinstance(archival, str):
            try:
                archival = json.loads(archival)
            except (ValueError, json.JSONDecodeError):
                archival = []

        query_lower = query.lower()
        matches = []
        for item in archival if isinstance(archival, list) else []:
            content = item.get("content", "")
            tags = " ".join(item.get("tags", []))
            if query_lower in content.lower() or query_lower in tags.lower():
                matches.append(item)
        return matches[:limit]

    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not hasattr(self.base_memory, "search_knowledge"):
            return []
        results = self.base_memory.search_knowledge(query=query, limit=limit)
        return [r for r in results if not str(r.get("category", "")).startswith(self.ARCHIVAL_CATEGORY)]

    def build_context(
        self,
        user_id: str,
        query: str,
        include_archival: bool = True,
        include_graph: bool = True,
    ) -> Dict[str, Any]:
        blocks = self.get_core_blocks(user_id)
        archival = self.search_archival_memory(user_id, query, limit=3) if include_archival else []
        recall = self.search_recall(user_id, query, limit=3)
        graph = self._search_graph(query) if include_graph else []

        sections = []
        core_text = self._format_core_blocks(blocks)
        if core_text:
            sections.append("CORE MEMORY:\n" + core_text)
        if archival:
            sections.append("ARCHIVAL MEMORY:\n" + self._format_archival(archival))
        if recall:
            sections.append("RELEVANT CONVERSATION RECALL:\n" + self._format_recall(recall))
        if graph:
            sections.append("GRAPH MEMORY:\n" + self._format_graph(graph))

        return {
            "text": "\n\n".join(sections),
            "core_blocks": blocks,
            "archival": archival,
            "recall": recall,
            "graph": graph,
        }

    def update_after_interaction(
        self,
        user_id: str,
        user_message: str,
        bot_response: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._update_core_from_metadata(user_id, metadata or {})
        self._update_core_from_profile(user_id)
        candidate = self._extract_simple_archival_candidate(user_message)
        if candidate:
            self.add_archival_memory(user_id, candidate, tags=["auto", "user_fact"], priority=1)

    def _get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        if hasattr(self.base_memory, "get_user_profile"):
            return self.base_memory.get_user_profile(user_id)
        return None

    def _archival_category(self, user_id: str) -> str:
        return f"{self.ARCHIVAL_CATEGORY}:{user_id}"

    def _update_profile(self, user_id: str, updates: Dict[str, Any]) -> None:
        if hasattr(self.base_memory, "update_user_profile"):
            self.base_memory.update_user_profile(user_id, updates)
        elif hasattr(self.base_memory, "update_profile"):
            self.base_memory.update_profile(user_id, updates)

    def _save_core_blocks(self, user_id: str, blocks: Dict[str, Any]) -> None:
        profile = self._get_profile(user_id) or {}
        metadata = self._decode_json_object(profile.get("metadata"))
        metadata[self.CORE_METADATA_KEY] = blocks
        self._update_profile(user_id, {"metadata": metadata, self.CORE_METADATA_KEY: blocks})

    def _update_core_from_metadata(self, user_id: str, metadata: Dict[str, Any]) -> None:
        if not metadata:
            return

        profile_fields = {}
        for key in ("name", "location", "favorite_food", "timezone", "language"):
            if metadata.get(key):
                profile_fields[key] = metadata[key]

        if not profile_fields:
            return

        blocks = self.get_core_blocks(user_id)
        human = blocks.get("human", {})
        existing = human.get("value", "")
        additions = [f"{key}: {value}" for key, value in profile_fields.items()]
        merged = "\n".join([part for part in [existing, "\n".join(additions)] if part]).strip()
        self.set_core_block(
            user_id,
            "human",
            self._dedupe_lines(merged),
            description=human.get("description"),
        )

    def _update_core_from_profile(self, user_id: str) -> None:
        profile = self._get_profile(user_id) or {}
        profile_fields = {}
        for key in ("name", "location", "favorite_food", "timezone", "language"):
            if profile.get(key):
                profile_fields[key] = profile[key]

        preferences = self._decode_json_object(profile.get("preferences"))
        for key in ("location", "favorite_food", "timezone", "language"):
            if preferences.get(key) and key not in profile_fields:
                profile_fields[key] = preferences[key]

        if not profile_fields:
            return

        blocks = self.get_core_blocks(user_id)
        human = blocks.get("human", {})
        existing = human.get("value", "")
        additions = [f"{key}: {value}" for key, value in profile_fields.items()]
        merged = "\n".join([part for part in [existing, "\n".join(additions)] if part]).strip()
        self.set_core_block(
            user_id,
            "human",
            self._dedupe_lines(merged),
            description=human.get("description"),
        )

    def _extract_simple_archival_candidate(self, message: str) -> str:
        lowered = message.lower()
        signals = (
            "my name is",
            "i prefer",
            "i like",
            "i live in",
            "i work",
            "remember",
            "benim ad",
            "ismim",
            "tercih",
            "seviyorum",
            "unutma",
        )
        if any(signal in lowered for signal in signals):
            return message.strip()
        return ""

    def _search_graph(self, query: str) -> List[Any]:
        if not self.graph_store:
            return []
        for token in query.replace("?", " ").replace(".", " ").split():
            if len(token) < 3:
                continue
            search = getattr(self.graph_store, "search_current", self.graph_store.search)
            results = search(token, depth=1)
            if results:
                return results[:5]
        return []

    def _format_core_blocks(self, blocks: Dict[str, Dict[str, Any]]) -> str:
        lines = []
        for label, block in blocks.items():
            value = str(block.get("value", "")).strip()
            if value:
                lines.append(f"[{label}] {value}")
        return "\n".join(lines)

    def _format_archival(self, items: List[Dict[str, Any]]) -> str:
        lines = []
        for item in items:
            content = item.get("answer") or item.get("content") or item.get("text") or ""
            if content:
                lines.append(f"- {content}")
        return "\n".join(lines)

    def _format_recall(self, items: List[Dict[str, Any]]) -> str:
        lines = []
        for item in items:
            user_msg = item.get("user_message", "")
            bot_msg = item.get("bot_response", "")
            lines.append(f"- User: {user_msg}\n  Assistant: {bot_msg}")
        return "\n".join(lines)

    def _format_graph(self, items: List[Any]) -> str:
        return "\n".join(f"- {src} --{rel}--> {dst}" for src, rel, dst in items)

    def _decode_json_object(self, value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value:
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, dict) else {}
            except (ValueError, json.JSONDecodeError):
                return {}
        return {}

    def _trim(self, value: str, limit: int) -> str:
        value = value or ""
        return value[-limit:] if len(value) > limit else value

    def _dedupe_lines(self, value: str) -> str:
        seen = set()
        lines = []
        for line in value.splitlines():
            clean = line.strip()
            if clean and clean not in seen:
                seen.add(clean)
                lines.append(clean)
        return "\n".join(lines)
