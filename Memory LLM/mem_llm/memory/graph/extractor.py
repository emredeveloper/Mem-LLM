import json
import logging
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from ...mem_agent import MemAgent

logger = logging.getLogger(__name__)


class GraphExtractor:
    """
    Extracts knowledge graph triplets (Entity, Relation, Entity) from text using an LLM.
    """

    def __init__(self, agent: "MemAgent"):
        self.agent = agent

    def extract(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract triplets from text.
        Returns list of (Source, Relation, Target).
        """
        prompt = f"""
        Analyze the following text and extract knowledge graph triplets.
        Return ONLY a JSON array of arrays, where each inner array is ["Source", "Relation", "Target"].
        Entities should be simplistic and normalized (e.g., "Elon Musk", not "he").
        Relations should be verbs or prepositions (e.g., "is_CEO_of", "located_in").

        Text: "{text}"

        Example Output:
        [["Alice", "knows", "Bob"], ["Bob", "lives_in", "Paris"]]

        JSON Output:
        """

        response = self.agent.chat(prompt)

        try:
            # Clean response to ensure it's just JSON
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:-3]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:-3]

            triplets = json.loads(cleaned_response)

            valid_triplets = []
            for t in triplets:
                if isinstance(t, list) and len(t) == 3:
                    valid_triplets.append((str(t[0]), str(t[1]), str(t[2])))

            return valid_triplets

        except json.JSONDecodeError:
            logger.warning(f"Failed to parse graph extraction JSON: {response}")
            return []
        except Exception as e:
            logger.error(f"Graph extraction error: {e}")
            return []
