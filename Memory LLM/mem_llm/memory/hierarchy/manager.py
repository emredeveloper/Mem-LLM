"""
Hierarchical Memory Manager
===========================

Orchestrates the 4-layer memory system.
"""

import logging
import os
from typing import Any, Dict, Optional

from .categorizer import AutoCategorizer
from .layers import CategoryLayer, DomainLayer, EpisodeLayer, TraceLayer

logger = logging.getLogger(__name__)


class HierarchicalMemory:
    """
    Main entry point for Hierarchical Memory System.
    Manages data flow across Episode, Trace, Category, and Domain layers.
    """

    def __init__(
        self,
        base_memory_manager,
        llm_client=None,
        trace_ttl_seconds: Optional[int] = None,
        category_ttl_seconds: Optional[int] = None,
        domain_ttl_seconds: Optional[int] = None,
    ):
        """
        Args:
            base_memory_manager: Existing MemoryManager or SQLMemoryManager
            llm_client: LLM client for categorization and abstraction
        """
        self.base_memory = base_memory_manager
        self.llm = llm_client

        def _env_int(name: str, default: Optional[int]) -> Optional[int]:
            if default is not None:
                return default
            raw = os.environ.get(name)
            if raw is None or raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                return None

        trace_ttl = _env_int("MEM_LLM_TRACE_TTL_SECONDS", trace_ttl_seconds)
        category_ttl = _env_int("MEM_LLM_CATEGORY_TTL_SECONDS", category_ttl_seconds)
        domain_ttl = _env_int("MEM_LLM_DOMAIN_TTL_SECONDS", domain_ttl_seconds)

        # Initialize Layers
        self.episode_layer = EpisodeLayer(base_memory_manager)
        self.trace_layer = TraceLayer(ttl_seconds=trace_ttl)
        self.category_layer = CategoryLayer(ttl_seconds=category_ttl)
        self.domain_layer = DomainLayer(ttl_seconds=domain_ttl)

        # Initialize Categorizer
        if llm_client:
            self.categorizer = AutoCategorizer(llm_client)
        else:
            self.categorizer = None
            logger.warning(
                "HierarchicalMemory initialized without LLM client. Categorization disabled."
            )

    def add_interaction(
        self, user_id: str, user_message: str, bot_response: str, metadata: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Process and store interaction across all layers.

        Returns:
            Dict with IDs/status for each layer
        """
        result = {}

        # 1. Episode Layer (Raw Storage)
        # This uses the existing system, so it's robust
        episode_id = self.episode_layer.add(
            {
                "user_id": user_id,
                "user_message": user_message,
                "bot_response": bot_response,
                "metadata": metadata,
            }
        )
        result["episode_id"] = episode_id

        # If no LLM, we can't do smart categorization/abstraction yet
        if not self.categorizer:
            return result

        # 2. Categorization
        category, domain = self.categorizer.categorize(user_message, bot_response)
        result["category"] = category
        result["domain"] = domain

        # 3. Trace Layer (Abstraction)
        # Create a memory trace (simplified for now, could be LLM-summarized)
        trace_content = f"User asked about {category}: {user_message[:50]}..."
        trace_id = self.trace_layer.add(
            {
                "user_id": user_id,
                "content": trace_content,
                "original_episode_id": episode_id,
                "category": category,
            }
        )
        result["trace_id"] = trace_id

        # 4. Category Layer (Aggregation)
        # Update category stats
        self.category_layer.add(
            {
                "user_id": user_id,
                "category": category,
                "summary_update": f"Last discussed: {user_message[:30]}...",
            }
        )

        # 5. Domain Layer (High-level Context)
        self.domain_layer.add(
            {"user_id": user_id, "domain": domain, "summary": f"Active in {domain}"}
        )

        return result

    def retrieve(self, query: str, user_id: str, max_depth: int = 4) -> Dict[str, Any]:
        """
        Layer-by-layer retrieval.

        Args:
            query: Search query
            user_id: User ID
            max_depth: How deep to search (1=Domain only, 4=All layers)

        Returns:
            Dict containing results from requested layers
        """
        results = {}

        # Top-down retrieval approach

        # Level 1: Domain
        if max_depth >= 1:
            domains = self.domain_layer.get(query, user_id=user_id)
            results["domains"] = domains

        # Level 2: Category
        if max_depth >= 2:
            categories = self.category_layer.get(query, user_id=user_id)
            results["categories"] = categories

        # Level 3: Traces
        if max_depth >= 3:
            # If we identified relevant categories in L2, filter traces by them
            # For now, simple retrieval
            traces = self.trace_layer.get(query, user_id=user_id)
            results["traces"] = traces

        # Level 4: Episodes (Detailed)
        if max_depth >= 4:
            # Use base memory search
            if hasattr(self.base_memory, "search_conversations"):
                episodes = self.base_memory.search_conversations(user_id, query)
                results["episodes"] = episodes
            else:
                results["episodes"] = []

        return results

    def get_context(self, user_id: str) -> str:
        """
        Construct a hierarchical context string for the LLM.
        """
        context = []

        # 1. Active Domains
        domains = self.domain_layer.get(None, user_id=user_id)
        if domains:
            dom_names = [d["name"] for d in domains]
            context.append(f"Active Domains: {', '.join(dom_names)}")

        # 2. Recent Categories
        categories = self.category_layer.get(None, user_id=user_id)
        if categories:
            # Sort by recency/count
            sorted_cats = sorted(
                categories, key=lambda x: x.get("interaction_count", 0), reverse=True
            )[:3]
            cat_summaries = [f"- {c['name']}: {c.get('summary', '')}" for c in sorted_cats]
            context.append("Recent Topics:\n" + "\n".join(cat_summaries))

        # 3. Recent Traces
        traces = self.trace_layer.get(None, user_id=user_id, limit=3)
        if traces:
            trace_txt = [f"- {t['content']}" for t in traces]
            context.append("Short-term Memory:\n" + "\n".join(trace_txt))

        return "\n\n".join(context)
