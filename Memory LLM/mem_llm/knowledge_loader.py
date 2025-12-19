"""
Knowledge Base Loader
Loads pre-prepared problem/solution database into the system
"""

import json

from .memory_db import SQLMemoryManager


class KnowledgeLoader:
    """Knowledge base management and loading"""

    def __init__(self, db_manager: SQLMemoryManager):
        """
        Args:
            db_manager: SQL memory manager
        """
        self.db = db_manager

    def load_from_json(self, file_path: str) -> int:
        """Load knowledge base from JSON file"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for entry in data.get("knowledge_base", []):
            self.db.add_knowledge(
                category=entry["category"],
                question=entry["question"],
                answer=entry["answer"],
                keywords=entry.get("keywords", []),
                priority=entry.get("priority", 0),
            )
            count += 1

        return count

    def load_default_ecommerce_kb(self) -> int:
        """Load default e-commerce knowledge base"""
        knowledge = [
            {
                "category": "shipping",
                "question": "When will my order arrive?",
                "answer": "Orders are shipped within 2-3 business days and delivered within 3-5 days.",
                "keywords": ["shipping", "delivery", "time"],
                "priority": 10,
            },
            {
                "category": "return",
                "question": "How do I return a product?",
                "answer": "You can return products within 14 days. Create a request from My Orders page.",
                "keywords": ["return", "refund"],
                "priority": 10,
            },
        ]

        count = 0
        for entry in knowledge:
            self.db.add_knowledge(**entry)
            count += 1

        return count

    def load_default_tech_support_kb(self) -> int:
        """Load default tech support knowledge base"""
        knowledge = [
            {
                "category": "connection",
                "question": "Cannot connect to internet",
                "answer": "1) Restart your modem/router 2) Check Wi-Fi password 3) Try other devices",
                "keywords": ["internet", "connection", "wifi"],
                "priority": 10,
            },
        ]

        count = 0
        for entry in knowledge:
            self.db.add_knowledge(**entry)
            count += 1

        return count
