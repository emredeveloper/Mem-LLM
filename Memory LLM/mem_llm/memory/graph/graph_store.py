import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx

logger = logging.getLogger(__name__)


class GraphStore:
    """
    Knowledge Graph storage using NetworkX.
    Nodes represent entities (Person, Place, Concept).
    Edges represent relationships.
    """

    def __init__(self, persistence_path: Optional[str] = None):
        self.graph = nx.DiGraph()
        self.persistence_path = persistence_path

        if self.persistence_path and os.path.exists(self.persistence_path):
            self.load()

    def add_triplet(self, source: str, relation: str, target: str, metadata: Dict[str, Any] = None):
        """Add a subject-predicate-object triplet to the graph."""
        self.graph.add_node(source)
        self.graph.add_node(target)

        # Check if edge exists to avoid duplicates or update metadata
        if self.graph.has_edge(source, target):
            # Update existing edge data if needed, or simple overwrite
            edge_data = dict(self.graph.get_edge_data(source, target) or {})
            edge_data["count"] = edge_data.get("count", 1) + 1
            edge_data["last_updated"] = datetime.now().isoformat()

            existing_relation = edge_data.get("relation")
            relations = set(edge_data.get("relations", []))
            if existing_relation and existing_relation != relation:
                relations.add(existing_relation)
            relations.add(relation)
            if relations:
                edge_data["relations"] = sorted(relations)

            if metadata:
                for key, value in metadata.items():
                    if key not in edge_data:
                        edge_data[key] = value
                    elif isinstance(edge_data[key], dict) and isinstance(value, dict):
                        edge_data[key].update(value)
                    elif isinstance(edge_data[key], list) and isinstance(value, list):
                        merged = list(dict.fromkeys(edge_data[key] + value))
                        edge_data[key] = merged

            edge_data["relation"] = relation
            self.graph.add_edge(source, target, **edge_data)
            logger.debug(f"Updated triplet: {source} -[{relation}]-> {target}")
            return

        edge_metadata = metadata.copy() if metadata else {}
        edge_metadata.setdefault("count", 1)
        edge_metadata.setdefault("created_at", datetime.now().isoformat())
        self.graph.add_edge(source, target, relation=relation, **edge_metadata)
        logger.debug(f"Added triplet: {source} -[{relation}]-> {target}")

    def search(self, query_entity: str, depth: int = 1) -> List[Tuple[str, str, str]]:
        """
        Return triplets related to the query entity.
        Returns list of (source, relation, target).
        """
        if query_entity not in self.graph:
            return []

        triplets = []
        # Get immediate neighbors (ego graph)
        # Note: ego_graph directionality depends on use case.
        # Usually we want outgoing and incoming.
        try:
            subgraph = nx.ego_graph(self.graph, query_entity, radius=depth, undirected=True)
            for u, v, data in subgraph.edges(data=True):
                relation = data.get("relation", "related_to")
                triplets.append((u, relation, v))
        except Exception as e:
            logger.error(f"Graph search error: {e}")

        return triplets

    def get_summary(self) -> str:
        """Return a text summary of graph stats."""
        return (
            f"Graph contains {self.graph.number_of_nodes()} entities "
            f"and {self.graph.number_of_edges()} relationships."
        )

    def save(self):
        """Save graph to JSON."""
        if not self.persistence_path:
            return

        data = nx.node_link_data(self.graph)
        os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
        with open(self.persistence_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Graph saved to {self.persistence_path}")

    def load(self):
        """Load graph from JSON."""
        if not self.persistence_path or not os.path.exists(self.persistence_path):
            return

        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)
            self.graph = nx.node_link_graph(data)
            logger.info(f"Graph loaded from {self.persistence_path}")
        except Exception as e:
            logger.error(f"Failed to load graph: {e}")

    def clear(self):
        """Clear the graph and save empty state."""
        self.graph.clear()
        if self.persistence_path:
            self.save()
        logger.info("Graph cleared")
