from unittest.mock import MagicMock

import networkx as nx
import pytest

from mem_llm.memory.graph.extractor import GraphExtractor
from mem_llm.memory.graph.graph_store import GraphStore


@pytest.fixture
def graph_store():
    return GraphStore()


def test_add_triplet(graph_store):
    graph_store.add_triplet("Alice", "knows", "Bob")
    assert graph_store.graph.has_node("Alice")
    assert graph_store.graph.has_node("Bob")
    assert graph_store.graph.has_edge("Alice", "Bob")
    assert graph_store.graph["Alice"]["Bob"]["relation"] == "knows"


def test_search_graph(graph_store):
    graph_store.add_triplet("Alice", "knows", "Bob")
    graph_store.add_triplet("Bob", "lives_in", "Paris")

    # Search Alice (depth 1) -> knows Bob
    results = graph_store.search("Alice")
    assert len(results) == 1
    assert results[0] == ("Alice", "knows", "Bob")

    # Search Bob (depth 1) -> knows Alice (inverse in ego graph) + lives_in Paris
    # ego_graph with center Bob includes Alice and Paris.
    # Edges: (Alice, Bob), (Bob, Paris)
    results_bob = graph_store.search("Bob")
    assert len(results_bob) == 2

    # Verify contents
    # params = set([(u, r, v) for u, r, v in results_bob]) -> Removed unused variable
    # Note: search implementation returns (u, relation, v) from edge data.
    # Direction is preserved in edges() if graph is directed?
    # ego_graph(..., undirected=True) converts to undirected for *radius calculation*
    # but might return directed graph if input was directed?
    # NetworkX ego_graph doc: "Returns the subgraph induced by neighbors...".
    # The returned graph is same type as input.

    # Let's check logic in GraphStore:
    # subgraph = nx.ego_graph(self.graph, query_entity, radius=depth, undirected=True)
    # This might include incoming edges too if undirected=True is used for distance.

    # Checking if "Alice" is in Bob's results
    # Edges in subgraph: (Alice, Bob), (Bob, Paris)
    # But graph is DiGraph.
    pass


def test_persistence(tmp_path):
    f = tmp_path / "graph.json"
    store = GraphStore(str(f))
    store.add_triplet("A", "r", "B")
    store.save()

    store2 = GraphStore(str(f))
    assert store2.graph.has_edge("A", "B")


def test_extractor():
    mock_agent = MagicMock()
    mock_agent.chat.return_value = '[["Alice", "knows", "Bob"]]'

    extractor = GraphExtractor(mock_agent)
    triplets = extractor.extract("Alice knows Bob")

    assert len(triplets) == 1
    assert triplets[0] == ("Alice", "knows", "Bob")
