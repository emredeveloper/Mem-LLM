"""Vector store unit tests."""

import pytest

from mem_llm.memory_db import SQLMemoryManager
from mem_llm.vector_store import ChromaVectorStore


@pytest.mark.unit
def test_default_embedding_model_is_resolvable():
    """The default must be a sentence-transformers id, not an Ollama-style tag.

    `nomic-embed-text-v2-moe:latest` shipped as the default for several releases
    and could never be loaded: the `:latest` suffix is Ollama syntax and makes
    sentence-transformers raise OSError on an invalid repo id.
    """
    import inspect

    default = inspect.signature(ChromaVectorStore.__init__).parameters["embedding_model"].default
    assert ":" not in default, f"{default!r} looks like an Ollama tag, not a HF repo id"


@pytest.mark.unit
def test_semantic_search_finds_non_matching_words(tmp_path):
    """Vector search must find entries that share no keywords with the query."""
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    db = SQLMemoryManager(db_path=str(tmp_path / "v.db"), enable_vector_search=True)
    try:
        if db.vector_store is None:
            # Building the store downloads the embedding model, so a sandbox
            # with no network (or a throttled one) cannot run this. That is an
            # environment limit, not a defect - skip rather than fail.
            pytest.skip("embedding model unavailable (offline or rate limited)")

        db.add_knowledge(
            "job", "Where does Emre work?", "Emre works at Acme Corp as a data scientist."
        )
        db.add_knowledge("hobby", "Hobby", "Emre enjoys mountain biking on weekends.")

        # "profession" appears in neither entry - only semantic search can match.
        results = db.search_knowledge("what is his profession", limit=1)
        assert results, "semantic search returned nothing"
        assert "data scientist" in results[0]["answer"]
    finally:
        db.close()
