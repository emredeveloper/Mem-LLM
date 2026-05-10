import shutil
import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

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

    results = graph_store.search("Alice")
    assert len(results) == 1
    assert results[0] == ("Alice", "knows", "Bob")

    results_bob = graph_store.search("Bob")
    assert len(results_bob) == 2


def test_temporal_graph_current_edges_ignore_closed_facts(graph_store):
    graph_store.add_triplet(
        "User",
        "prefers_language",
        "Python",
        metadata={"valid_from": "2026-01-01T00:00:00", "valid_to": "2026-02-01T00:00:00"},
    )
    graph_store.add_triplet(
        "User",
        "prefers_language",
        "Rust",
        metadata={"valid_from": "2026-02-01T00:00:00"},
    )

    current = graph_store.search_current("User")

    assert ("User", "prefers_language", "Rust") in current
    assert ("User", "prefers_language", "Python") not in current


def test_temporal_graph_search_at_time(graph_store):
    graph_store.add_triplet(
        "User",
        "works_at",
        "Company A",
        metadata={"valid_from": "2026-01-01T00:00:00", "valid_to": "2026-03-01T00:00:00"},
    )
    graph_store.add_triplet(
        "User",
        "works_at",
        "Company B",
        metadata={"valid_from": "2026-03-01T00:00:00"},
    )

    then = graph_store.search_at_time("User", datetime(2026, 2, 1))
    now = graph_store.search_at_time("User", datetime(2026, 4, 1))

    assert ("User", "works_at", "Company A") in then
    assert ("User", "works_at", "Company B") not in then
    assert ("User", "works_at", "Company B") in now


def test_temporal_graph_supersedes_same_relation(graph_store):
    graph_store.add_triplet(
        "User",
        "lives_in",
        "Istanbul",
        metadata={"valid_from": "2026-01-01T00:00:00"},
    )
    graph_store.add_triplet(
        "User",
        "lives_in",
        "Ankara",
        metadata={"valid_from": "2026-03-01T00:00:00", "supersedes": True},
    )

    current = graph_store.search_current("User")
    historical = graph_store.search_at_time("User", datetime(2026, 2, 1))

    assert ("User", "lives_in", "Ankara") in current
    assert ("User", "lives_in", "Istanbul") not in current
    assert ("User", "lives_in", "Istanbul") in historical


def test_persistence():
    root = Path(__file__).resolve().parents[1] / ".tmp"
    root.mkdir(parents=True, exist_ok=True)
    test_dir = root / f"graph_{uuid.uuid4().hex[:8]}"
    test_dir.mkdir(parents=True, exist_ok=True)
    f = test_dir / "graph.json"

    store = GraphStore(str(f))
    store.add_triplet("A", "r", "B")
    store.save()

    store2 = GraphStore(str(f))
    assert store2.graph.has_edge("A", "B")
    shutil.rmtree(test_dir, ignore_errors=True)


def test_extractor():
    mock_agent = MagicMock()
    mock_agent.llm = MagicMock()
    mock_agent.llm.chat.return_value = '[["Alice", "knows", "Bob"]]'

    extractor = GraphExtractor(mock_agent)
    triplets = extractor.extract("Alice knows Bob")

    assert len(triplets) == 1
    assert triplets[0] == ["Alice", "knows", "Bob"]
