"""Quickstart: search the knowledge base (BM25, and optionally hybrid).

Search is ranked by BM25 out of the box - no extra install, because FTS5 ships
with SQLite. Install the vector extra to add semantic search on top:

    pip install mem-llm[vector]

With it, results from both retrievers are combined, so a question phrased in
completely different words still finds the right entry.
"""

import shutil
import tempfile
from pathlib import Path

from mem_llm.memory_db import SQLMemoryManager

# Set to True after `pip install mem-llm[vector]` to see semantic matching.
USE_VECTOR = False


def main() -> None:
    workdir = Path(tempfile.mkdtemp())
    db = SQLMemoryManager(db_path=str(workdir / "kb.db"), enable_vector_search=USE_VECTOR)

    try:
        print("BM25 ranking:", db.fts_available)
        print("semantic search:", bool(db.vector_store))

        db.add_knowledge(
            "billing", "How do I get a refund?", "Refunds are issued within 5 business days."
        )
        db.add_knowledge("billing", "Payment methods", "We accept credit cards and bank transfer.")
        db.add_knowledge(
            "shipping", "Shipping time", "Orders ship in 2 days. Refund policy does not apply."
        )

        # BM25 ranks by relevance: the entry *about* refunds wins over the one
        # that only mentions the word in passing.
        show(db, "refund")

        # Porter stemming, so "refunds" matches "refund".
        show(db, "how long do refunds take")

        # Category filter still narrows the search.
        show(db, "refund", category="shipping")

        if USE_VECTOR:
            # No shared keyword with any entry - only semantic search finds it.
            show(db, "how do I get my money back")
        else:
            print("\n(enable USE_VECTOR to try 'how do I get my money back')")
    finally:
        db.close()
        shutil.rmtree(workdir, ignore_errors=True)


def show(db: SQLMemoryManager, query: str, category: str | None = None) -> None:
    results = db.search_knowledge(query, category=category, limit=2)
    label = f"{query!r}" + (f" in {category!r}" if category else "")
    print(f"\n{label}")
    for entry in results:
        print("   ", entry["answer"][:60])


if __name__ == "__main__":
    main()
