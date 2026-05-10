from mem_llm.memory_manager import MemoryManager
from mem_llm.memory_router import MemoryRouter


def test_memory_router_core_block_roundtrip(tmp_path):
    memory = MemoryManager(str(tmp_path))
    memory.add_user("alice")
    router = MemoryRouter(memory)

    router.set_core_block("alice", "human", "name: Alice", description="User facts")
    blocks = router.get_core_blocks("alice")

    assert blocks["human"]["value"] == "name: Alice"
    assert blocks["human"]["description"] == "User facts"


def test_memory_router_archival_json_search(tmp_path):
    memory = MemoryManager(str(tmp_path))
    memory.add_user("alice")
    router = MemoryRouter(memory)

    router.add_archival_memory("alice", "Alice prefers concise Python examples.", tags=["python"])
    results = router.search_archival_memory("alice", "Python", limit=3)

    assert len(results) == 1
    assert "concise Python" in results[0]["content"]


def test_memory_router_build_context_includes_core_archival_and_recall(tmp_path):
    memory = MemoryManager(str(tmp_path))
    memory.add_interaction("alice", "I prefer Python.", "Noted.")
    router = MemoryRouter(memory)
    router.set_core_block("alice", "human", "name: Alice")
    router.add_archival_memory("alice", "Alice prefers Python for automation.", tags=["python"])

    context = router.build_context("alice", "Python")

    assert "CORE MEMORY" in context["text"]
    assert "ARCHIVAL MEMORY" in context["text"]
    assert "RELEVANT CONVERSATION RECALL" in context["text"]
