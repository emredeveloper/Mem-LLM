"""Assert the features that must work with no extras installed.

Run against an installed `mem-llm` from a directory outside the source tree.
Every check here maps to a bug that actually shipped: a dependency that looked
optional but was imported unconditionally, and a search path that failed
silently rather than raising.
"""

import mem_llm
from mem_llm import MemAgent
from mem_llm.memory_db import SQLMemoryManager

# Graph memory imports pydantic unconditionally. While pydantic was undeclared
# the import failed, the error was swallowed, and GraphStore quietly vanished
# from the public API.
assert hasattr(mem_llm, "GraphStore"), "graph memory unavailable on a bare install"

agent = MemAgent(backend="ollama", model="x", enable_graph_memory=True, check_connection=False)
assert agent.graph_store is not None, "enable_graph_memory silently did nothing"

# BM25 ranking depends only on SQLite's own FTS5, so it must work without the
# vector extra.
db = SQLMemoryManager(db_path="ci_check.db")
try:
    assert db.fts_available, "FTS5 index missing"
    db.add_knowledge("billing", "Refund policy", "Refunds are issued within 5 business days.")
    hits = db.search_knowledge("how long do refunds take")
    assert hits, "BM25 search returned nothing"
    assert "Refunds are issued" in hits[0]["answer"], "BM25 ranked the wrong entry first"
finally:
    db.close()

print(f"bare install OK - mem-llm {mem_llm.__version__}, {len(mem_llm.__all__)} exports")
