"""Quickstart: enable graph memory and inspect stored triplets."""

import os

from mem_llm import MemAgent


BACKENDS = (
    ("ollama", os.getenv("OLLAMA_MODEL", "granite4:3b")),
    ("lmstudio", os.getenv("LMSTUDIO_MODEL", "google/gemma-3-4b")),
)


def run_backend(backend: str, model: str) -> None:
    try:
        agent = MemAgent(
            backend=backend,
            model=model,
            enable_graph_memory=True,
            check_connection=False,
        )
        agent.set_user("quickstart_user")

        agent.chat("My favorite language is Python.")
        agent.chat("I live in Berlin.")

        if agent.graph_store:
            print(f"[{backend}] {agent.graph_store.get_summary()}")
            print(f"[{backend}] Triplets:", agent.graph_store.search("Python"))
        else:
            print(f"[{backend}] Graph memory is not available (missing optional dependencies).")
    except Exception as exc:
        print(f"[{backend}] Error:", exc)


def main() -> None:
    for backend, model in BACKENDS:
        run_backend(backend, model)


if __name__ == "__main__":
    main()
