"""Hybrid retrieval tests: FTS5/BM25 ranking and reciprocal rank fusion."""

import pytest

from mem_llm.memory_db import SQLMemoryManager


@pytest.fixture
def kb(tmp_path):
    db = SQLMemoryManager(db_path=str(tmp_path / "kb.db"))
    db.add_knowledge(
        "billing", "How do I get a refund?", "Refunds are issued within 5 business days."
    )
    db.add_knowledge("billing", "Payment methods", "We accept credit cards and bank transfer.")
    db.add_knowledge(
        "ship", "Shipping time", "Orders ship in 2 days. Refund policy does not apply."
    )
    yield db
    db.close()


@pytest.mark.unit
def test_fts_index_is_available(kb):
    assert kb.fts_available, "FTS5 index was not created"


@pytest.mark.unit
def test_bm25_ranks_by_relevance_not_insertion_order(kb):
    """The entry about refunds must outrank one that merely mentions the word.

    Plain LIKE matching returns both and orders by priority/id, so the
    incidental mention can come first. BM25 weighs term frequency and field
    length instead.
    """
    results = kb.search_knowledge("refund", limit=3)
    assert results, "no results"
    assert "Refunds are issued" in results[0]["answer"]


@pytest.mark.unit
def test_porter_stemming_matches_word_variants(kb):
    """'refunds' in the query should match 'refund' in the text."""
    results = kb.search_knowledge("how long do refunds take", limit=2)
    assert results
    assert "Refunds are issued" in results[0]["answer"]


@pytest.mark.unit
def test_category_filter_still_applies(kb):
    results = kb.search_knowledge("refund", category="ship", limit=3)
    assert results
    assert all(r["category"] == "ship" for r in results)


@pytest.mark.unit
@pytest.mark.parametrize("bad", ['NEAR("a" "b")', "AND OR", '"unclosed', "*", "", "()"])
def test_fts_operators_in_user_text_do_not_raise(kb, bad):
    """Free text may contain FTS5 syntax; it must be quoted, never executed."""
    kb.search_knowledge(bad, limit=1)


@pytest.mark.unit
def test_existing_database_is_backfilled_into_the_index(tmp_path):
    """Databases written before the FTS index existed must stay searchable."""
    import sqlite3

    dbfile = tmp_path / "legacy.db"
    conn = sqlite3.connect(dbfile)
    conn.execute(
        """CREATE TABLE knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
            question TEXT NOT NULL, answer TEXT NOT NULL, keywords TEXT,
            priority INTEGER DEFAULT 0, active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    )
    conn.execute(
        "INSERT INTO knowledge_base (category, question, answer) VALUES "
        "('billing','Refund policy','Refunds are issued within 5 business days.')"
    )
    conn.commit()
    conn.close()

    db = SQLMemoryManager(db_path=str(dbfile))
    try:
        results = db.search_knowledge("refund", limit=2)
        assert results, "pre-existing rows were not indexed"
        assert "Refunds are issued" in results[0]["answer"]

        # Reopening must not backfill a second time.
        db.close()
        db = SQLMemoryManager(db_path=str(dbfile))
        count = db.conn.execute("SELECT count(*) FROM knowledge_fts").fetchone()[0]
        assert count == 1, f"index has {count} rows, expected 1"
    finally:
        db.close()


@pytest.mark.unit
def test_rrf_prefers_entries_found_by_both_retrievers():
    """An item ranked by both lists beats one ranked highly by only one."""
    dense = [{"id": 1, "answer": "a"}, {"id": 2, "answer": "b"}]
    sparse = [{"id": 3, "answer": "c"}, {"id": 1, "answer": "a"}]

    fused = SQLMemoryManager._reciprocal_rank_fusion([dense, sparse], limit=3)

    assert [x["id"] for x in fused][0] == 1
    assert len(fused) == 3, "fusion must dedupe, not concatenate"
