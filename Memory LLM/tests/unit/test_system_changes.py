from datetime import datetime, timedelta

import pytest

from mem_llm.api_server import AgentStore
from mem_llm.memory.hierarchy.layers import CategoryLayer, DomainLayer, TraceLayer
from mem_llm.tool_system import ToolRegistry, tool


@tool(name="allowed_tool", description="Allowed tool")
def allowed_tool(value: str) -> str:
    return value.upper()


@tool(name="blocked_tool", description="Blocked tool")
def blocked_tool(value: str) -> str:
    return value.lower()


def test_agent_store_lru_eviction():
    store = AgentStore(ttl_seconds=3600, max_size=2)
    store.set("user1", object())
    store.set("user2", object())

    # Force LRU order: user1 oldest, user2 newest.
    base_time = store._entries["user1"]["last_access"]
    store._entries["user1"]["last_access"] = base_time - 10
    store._entries["user2"]["last_access"] = base_time
    store._lru["user1"] = store._entries["user1"]["last_access"]
    store._lru["user2"] = store._entries["user2"]["last_access"]

    store.set("user3", object())

    assert store.get("user1") is None
    assert store.get("user2") is not None
    assert store.get("user3") is not None


def test_agent_store_ttl(monkeypatch):
    store = AgentStore(ttl_seconds=10, max_size=10)
    store.set("user1", object())

    base_time = store._entries["user1"]["last_access"]

    def fake_time():
        return base_time + 11

    monkeypatch.setattr("mem_llm.api_server.time.time", fake_time)
    assert store.get("user1") is None


def test_trace_layer_ttl_eviction():
    layer = TraceLayer(ttl_seconds=1)
    trace_id = layer.add({"user_id": "u1", "content": "hello"})
    assert trace_id

    old_time = (datetime.now() - timedelta(seconds=5)).isoformat()
    layer.traces["u1"][0]["timestamp"] = old_time

    assert layer.get(None, user_id="u1") == []


def test_category_layer_ttl_eviction():
    layer = CategoryLayer(ttl_seconds=1)
    layer.add({"user_id": "u1", "category": "c1", "summary_update": "s"})

    old_time = (datetime.now() - timedelta(seconds=5)).isoformat()
    layer.categories["u1"]["c1"]["last_updated"] = old_time

    assert layer.get(None, user_id="u1") == []


def test_domain_layer_ttl_eviction():
    layer = DomainLayer(ttl_seconds=1)
    layer.add({"user_id": "u1", "domain": "d1", "summary": "s"})

    old_time = (datetime.now() - timedelta(seconds=5)).isoformat()
    layer.domains["u1"]["d1"]["updated_at"] = old_time

    assert layer.get(None, user_id="u1") == []


def test_tool_allowlist_only_blocks_unlisted():
    registry = ToolRegistry(allowlist=["allowed_tool"], denylist=[], allowlist_only=True)
    registry.register_function(allowed_tool)
    registry.register_function(blocked_tool)

    result_allowed = registry.execute("allowed_tool", value="Test")
    assert result_allowed.status.name == "SUCCESS"
    assert result_allowed.result == "TEST"

    result_blocked = registry.execute("blocked_tool", value="Test")
    assert result_blocked.status.name == "ERROR"
    assert result_blocked.error == "Tool not allowed by policy"


def test_tool_denylist_blocks_even_if_registered():
    registry = ToolRegistry(denylist=["blocked_tool"], allowlist_only=False)
    registry.register_function(blocked_tool)

    result_blocked = registry.execute("blocked_tool", value="Test")
    assert result_blocked.status.name == "ERROR"
    assert result_blocked.error == "Tool not allowed by policy"
