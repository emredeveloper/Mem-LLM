"""
Conversation Summarizer
=======================

Automatically summarizes long conversation histories to optimize context window usage.

Features:
- Summarizes last N conversations
- Extracts key facts and context
- Saves tokens by condensing history
- Periodic auto-summary updates
- User profile extraction from summaries

Usage:
```python
from mem_llm import ConversationSummarizer

summarizer = ConversationSummarizer(llm_client)
summary = summarizer.summarize_conversations(conversations, user_id="alice")
```
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional


class ConversationSummarizer:
    """Summarizes conversation histories to optimize context"""

    def __init__(self, llm_client, logger: Optional[logging.Logger] = None):
        """
        Initialize summarizer

        Args:
            llm_client: OllamaClient instance for generating summaries
            logger: Logger instance (optional)
        """
        self.llm = llm_client
        self.logger = logger or logging.getLogger(__name__)

    def summarize_conversations(
        self,
        conversations: List[Dict],
        user_id: str,
        max_conversations: int = 20,
        include_facts: bool = True,
    ) -> Dict[str, Any]:
        """
        Summarize a list of conversations

        Args:
            conversations: List of conversation dicts with user_message and bot_response
            user_id: User identifier
            max_conversations: Maximum number of conversations to summarize
            include_facts: Extract key facts about the user

        Returns:
            Summary dict with text, facts, and metadata
        """
        if not conversations:
            return {
                "summary": "No conversation history available.",
                "key_facts": [],
                "conversation_count": 0,
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
            }

        # Limit conversations
        convs_to_summarize = (
            conversations[-max_conversations:]
            if len(conversations) > max_conversations
            else conversations
        )

        # Build prompt
        prompt = self._build_summary_prompt(convs_to_summarize, user_id, include_facts)

        try:
            # Generate summary
            self.logger.info(
                f"Generating summary for {user_id}: {len(convs_to_summarize)} conversations"
            )

            response = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Lower temperature for consistent summaries
                max_tokens=500,
            )

            # Parse response
            summary_data = self._parse_summary_response(response, convs_to_summarize, user_id)

            self.logger.info(f"✅ Summary generated: {len(summary_data['summary'])} chars")
            return summary_data

        except Exception as e:
            self.logger.error(f"Summary generation failed: {e}")
            return {
                "summary": f"Error generating summary: {str(e)}",
                "key_facts": [],
                "conversation_count": len(convs_to_summarize),
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
                "error": str(e),
            }

    def _build_summary_prompt(
        self, conversations: List[Dict], user_id: str, include_facts: bool
    ) -> str:
        """Build the summarization prompt"""

        # Format conversations
        conv_text = ""
        for i, conv in enumerate(conversations, 1):
            user_msg = conv.get("user_message", "")
            bot_msg = conv.get("bot_response", "")
            conv_text += f"\n{i}. User: {user_msg}\n   Bot: {bot_msg}\n"

        prompt = f"""You are a conversation summarizer. Summarize the following conversations for user '{user_id}'.

CONVERSATIONS:
{conv_text}

TASK:
Create a concise summary (max 200 words) that captures:
1. Main topics discussed
2. User's questions and concerns
3. Important context for future conversations"""

        if include_facts:
            prompt += """
4. Key facts about the user (preferences, background, needs)

FORMAT YOUR RESPONSE AS:
SUMMARY: [Your summary here]
KEY_FACTS: [Comma-separated list of facts about the user]
"""
        else:
            prompt += "\n\nProvide only the summary."

        return prompt

    def _parse_summary_response(
        self, response: str, conversations: List[Dict], user_id: str
    ) -> Dict[str, Any]:
        """Parse LLM response into structured summary"""

        summary_text = ""
        key_facts = []

        # Try to parse structured format
        if "SUMMARY:" in response and "KEY_FACTS:" in response:
            parts = response.split("KEY_FACTS:")
            summary_part = parts[0].replace("SUMMARY:", "").strip()
            facts_part = parts[1].strip() if len(parts) > 1 else ""

            summary_text = summary_part

            # Parse facts
            if facts_part:
                # Split by common delimiters
                facts_raw = facts_part.replace("\n", ",").split(",")
                key_facts = [f.strip() for f in facts_raw if f.strip() and len(f.strip()) > 3]
        else:
            # Fallback: use entire response as summary
            summary_text = response.strip()

        return {
            "summary": summary_text,
            "key_facts": key_facts,
            "conversation_count": len(conversations),
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
        }

    def should_update_summary(
        self,
        last_summary_time: Optional[str],
        new_conversations_count: int,
        update_threshold: int = 10,
    ) -> bool:
        """
        Determine if summary should be updated

        Args:
            last_summary_time: ISO timestamp of last summary
            new_conversations_count: Number of new conversations since last summary
            update_threshold: Minimum conversations before update

        Returns:
            True if summary should be updated
        """
        # Always update if no previous summary
        if not last_summary_time:
            return new_conversations_count >= 5  # Need at least 5 convs for meaningful summary

        # Update if threshold reached
        return new_conversations_count >= update_threshold

    def extract_user_insights(self, summary: str) -> Dict[str, Any]:
        """
        Extract structured insights from summary

        Args:
            summary: Summary text

        Returns:
            Insights dict with topics, preferences, etc.
        """
        insights = {"topics": [], "preferences": [], "needs": [], "background": []}

        # Simple keyword-based extraction
        # (Could be enhanced with NER or another LLM call)

        summary_lower = summary.lower()

        # Common topic keywords
        topic_keywords = {
            "programming": ["python", "javascript", "code", "programming", "development"],
            "business": ["business", "startup", "company", "market"],
            "technical": ["technical", "bug", "error", "issue", "problem"],
            "personal": ["personal", "preference", "like", "prefer"],
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in summary_lower for kw in keywords):
                insights["topics"].append(topic)

        return insights

    def get_summary_stats(self, original_text: str, summary_text: str) -> Dict[str, Any]:
        """
        Calculate compression statistics

        Args:
            original_text: Original conversation text
            summary_text: Summarized text

        Returns:
            Stats dict with compression ratio, token savings, etc.
        """
        orig_length = len(original_text)
        summary_length = len(summary_text)

        # Rough token estimation (1 token ≈ 4 chars)
        orig_tokens = orig_length // 4
        summary_tokens = summary_length // 4

        compression_ratio = (1 - summary_length / orig_length) * 100 if orig_length > 0 else 0

        return {
            "original_length": orig_length,
            "summary_length": summary_length,
            "compression_ratio": round(compression_ratio, 2),
            "original_tokens_est": orig_tokens,
            "summary_tokens_est": summary_tokens,
            "tokens_saved": orig_tokens - summary_tokens,
        }


class AutoSummarizer:
    """Automatically manages conversation summaries with periodic updates"""

    def __init__(
        self,
        summarizer: ConversationSummarizer,
        memory_manager,
        update_threshold: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize auto-summarizer

        Args:
            summarizer: ConversationSummarizer instance
            memory_manager: Memory manager (SQL or JSON)
            update_threshold: Update summary every N conversations
            logger: Logger instance
        """
        self.summarizer = summarizer
        self.memory = memory_manager
        self.update_threshold = update_threshold
        self.logger = logger or logging.getLogger(__name__)

        # Track summaries per user
        self.summaries = {}  # {user_id: summary_data}
        self.conversation_counts = {}  # {user_id: count_since_last_summary}

    def check_and_update(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if summary needs updating and update if necessary

        Args:
            user_id: User identifier

        Returns:
            New summary if updated, None otherwise
        """
        # Get conversation count since last summary
        count_since_last = self.conversation_counts.get(user_id, 0)
        last_summary_time = self.summaries.get(user_id, {}).get("generated_at")

        if self.summarizer.should_update_summary(
            last_summary_time, count_since_last, self.update_threshold
        ):
            return self.update_summary(user_id)

        return None

    def update_summary(self, user_id: str, max_conversations: int = 20) -> Dict[str, Any]:
        """
        Force update summary for user

        Args:
            user_id: User identifier
            max_conversations: Max conversations to summarize

        Returns:
            Summary data
        """
        try:
            # Get recent conversations
            if hasattr(self.memory, "get_recent_conversations"):
                conversations = self.memory.get_recent_conversations(user_id, max_conversations)
            else:
                conversations = []

            # Generate summary
            summary = self.summarizer.summarize_conversations(
                conversations, user_id, max_conversations=max_conversations
            )

            # Store summary
            self.summaries[user_id] = summary
            self.conversation_counts[user_id] = 0

            self.logger.info(f"✅ Auto-summary updated for {user_id}")
            return summary

        except Exception as e:
            self.logger.error(f"Auto-summary update failed for {user_id}: {e}")
            return {}

    def get_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current summary for user

        Args:
            user_id: User identifier

        Returns:
            Summary data or None
        """
        return self.summaries.get(user_id)

    def increment_conversation_count(self, user_id: str):
        """Increment conversation count for user"""
        self.conversation_counts[user_id] = self.conversation_counts.get(user_id, 0) + 1

    def reset_summary(self, user_id: str):
        """Reset summary for user"""
        if user_id in self.summaries:
            del self.summaries[user_id]
        self.conversation_counts[user_id] = 0
