import json
import logging
import re
from typing import TYPE_CHECKING, List, Tuple

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from ...mem_agent import MemAgent

logger = logging.getLogger(__name__)


class GraphExtractor:
    """
    Extracts knowledge graph triplets (Entity, Relation, Entity) from text using an LLM.
    """

    def __init__(self, agent: "MemAgent"):
        self.agent = agent

    def _parse_triplets(self, response: str) -> List[Tuple[str, str, str]]:
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3].strip()
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:-3].strip()

        # Try structured JSON first
        try:
            parsed = json.loads(cleaned_response)
        except json.JSONDecodeError:
            parsed = None

        class Triplet(BaseModel):
            source: str
            relation: str
            target: str

        if parsed is not None:
            normalized = []
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, (list, tuple)) and len(item) == 3:
                        normalized.append(
                            {"source": str(item[0]), "relation": str(item[1]), "target": str(item[2])}
                        )
                    elif isinstance(item, dict):
                        if {"source", "relation", "target"}.issubset(item.keys()):
                            normalized.append(
                                {
                                    "source": str(item["source"]),
                                    "relation": str(item["relation"]),
                                    "target": str(item["target"]),
                                }
                            )

            if normalized:
                try:
                    validated = [Triplet(**item) for item in normalized]
                    return [[t.source, t.relation, t.target] for t in validated]
                except ValidationError:
                    pass

        # Fallback: regex extraction
        triplet_pattern = r'\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]'
        matches = re.findall(triplet_pattern, response)
        if matches:
            return [[m[0], m[1], m[2]] for m in matches]

        return []

    def extract(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract triplets from text.
        Returns list of (Source, Relation, Target).
        """
        prompt = f"""
        Extract knowledge graph triplets from the following conversation.

        GOAL: Identify entities (people, places, interests, facts) and their relations.
        CRITICAL: DO NOT extract conversation metadata like "User says hello"
        or "Assistant replies".
        Only extract factual knowledge about the user or the topics discussed.

        Format: Return ONLY a JSON array of arrays: [["Source", "Relation", "Target"]].
        Example: [["User", "lives_in", "Istanbul"], ["Python", "is_a", "Programming Language"]]

        Text to analyze:
        ---
        {text}
        ---

        JSON Output:
        """

        # Use direct LLM call instead of agent.chat to avoid recursion/infinite loops
        # and to keep extraction logic separate from conversation history
        messages = [{"role": "user", "content": prompt}]
        response = self.agent.llm.chat(messages=messages, temperature=0.1)

        try:
            triplets = self._parse_triplets(response)
            return triplets

        except Exception as e:
            logger.warning(f"Failed to parse graph extraction: {e}. Response was: {response}")
            return []
