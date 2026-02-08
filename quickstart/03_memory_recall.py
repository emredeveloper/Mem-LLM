"""Quickstart: memory recall with two messages."""

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

        agent.chat("My name is Alex.")
        reply = agent.chat("What is my name?")
        print(f"[{backend}] Bot:", reply)
    except Exception as exc:
        print(f"[{backend}] Error:", exc)


def main() -> None:
    for backend, model in BACKENDS:
        run_backend(backend, model)


if __name__ == "__main__":
    main()
