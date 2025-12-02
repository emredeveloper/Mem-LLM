"""
Auto Categorizer
================

Uses LLM to automatically categorize interactions for hierarchical memory.
"""

import logging
from typing import Any, Tuple

logger = logging.getLogger(__name__)


class AutoCategorizer:
    """
    Analyzes interactions and assigns them to categories and domains.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def categorize(self, user_message: str, bot_response: str) -> Tuple[str, str]:
        """
        Analyze interaction and return (Category, Domain).

        Returns:
            Tuple[str, str]: (Category, Domain) e.g., ("python_coding", "technology")
        """
        prompt = self._build_prompt(user_message, bot_response)

        try:
            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for consistency
                max_tokens=50,
            )

            return self._parse_response(response)

        except Exception as e:
            logger.error(f"Categorization failed: {e}")
            return ("general", "general")

    def _build_prompt(self, user_msg: str, bot_msg: str) -> str:
        return f"""Analyze the following interaction and assign it to a specific CATEGORY and a broader DOMAIN.

INTERACTION:
User: {user_msg[:500]}
Bot: {bot_msg[:500]}

INSTRUCTIONS:
1. Identify the specific topic (CATEGORY). Use snake_case (e.g., python_coding, travel_planning).
2. Identify the high-level field (DOMAIN). Use snake_case (e.g., technology, lifestyle).
3. Return ONLY the category and domain separated by a pipe character (|).

EXAMPLES:
- "How do I use pandas?" -> python_coding|technology
- "Book a flight to Paris" -> travel_planning|lifestyle
- "I feel sad today" -> emotional_support|personal

RESPONSE FORMAT:
category_name|domain_name"""

    def _parse_response(self, response: str) -> Tuple[str, str]:
        try:
            # Clean up response
            text = response.strip().lower()

            if "|" in text:
                parts = text.split("|")
                category = parts[0].strip()
                domain = parts[1].strip()
                # Example:
                # {'category': 'python_coding', 'domain': 'technology'}
                return category, domain

            # Fallback parsing
            return "general", "general"

        except Exception:
            return "general", "general"
