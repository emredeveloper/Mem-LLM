import re
from collections import Counter
from typing import Dict, List


class TopicExtractor:
    """Extract topics from conversation text"""

    # Common stop words to ignore
    STOP_WORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "could",
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
        "me",
        "him",
        "her",
        "us",
        "them",
        "my",
        "your",
        "his",
        "its",
        "our",
        "their",
        "this",
        "that",
        "these",
        "those",
        "here",
        "there",
        "where",
        "when",
        "what",
        "who",
        "how",
        "why",
        "which",
        "any",
        "some",
        "all",
        "no",
        "not",
        "can",
        "cannot",
        "just",
        "only",
        "also",
        "very",
        "much",
        "more",
        "most",
        "other",
        "such",
        "into",
        "over",
        "under",
        "up",
        "down",
        "out",
        "off",
        "about",
        "then",
        "than",
        "now",
        "so",
        "if",
        "as",
        "like",
        "good",
        "well",
        "get",
        "got",
        "go",
        "going",
        "make",
        "made",
        "know",
        "think",
        "see",
        "say",
        "said",
        "tell",
        "told",
        "ask",
        "asked",
        "want",
        "need",
        "use",
        "used",
        "find",
        "found",
        "give",
        "gave",
        "take",
        "took",
        "look",
        "looked",
        "come",
        "came",
        "work",
        "worked",
        "try",
        "tried",
        "help",
        "helped",
        "please",
        "thanks",
        "thank",
        "hello",
        "hi",
        "hey",
        "bye",
        "ok",
        "okay",
        "yes",
        "yeah",
        "sure",
        "fine",
        "great",
        "nice",
        "cool",
    }

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract top N keywords from text"""
        if not text:
            return []

        # Lowercase and tokenize (simple regex for words)
        words = re.findall(r"\b\w+\b", text.lower())

        # Filter stop words and short words
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 2]

        # Count and return top N
        counter = Counter(filtered)
        return [word for word, _ in counter.most_common(top_n)]

    def extract_topics(self, messages: List[str], top_n: int = 10) -> Dict[str, int]:
        """Extract topics from multiple messages"""
        if not messages:
            return {}

        all_text = " ".join(messages)

        # Get more keywords initially to filter later if needed
        keywords = self.extract_keywords(all_text, top_n * 3)

        # Count occurrences across messages to find distribution
        # We want to know how many times each keyword appears in the total corpus
        # But extract_keywords already gives us the most common ones.
        # So we can just recount them or use the counter from extract_keywords logic.

        # Let's do it more efficiently:
        words = re.findall(r"\b\w+\b", all_text.lower())
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 2]
        counter = Counter(filtered)

        return dict(counter.most_common(top_n))
