"""Quickstart: basic chat example with a local backend."""

import os

from mem_llm import MemAgent


BACKENDS = (
    ("ollama", os.getenv("OLLAMA_MODEL", "granite4:3b")),
    ("lmstudio", os.getenv("LMSTUDIO_MODEL", "google/gemma-3-4b")),
)


def run_backend(backend: str, model: str) -> None:
    try:
        agent = MemAgent(backend=backend, model=model, check_connection=False)
        agent.set_user("quickstart_user")
        response = agent.chat("Hello! Give me a short greeting.")
        print(f"[{backend}] Bot:", response)
    except Exception as exc:
        print(f"[{backend}] Error:", exc)


def main() -> None:
    for backend, model in BACKENDS:
        run_backend(backend, model)


if __name__ == "__main__":
    main()
