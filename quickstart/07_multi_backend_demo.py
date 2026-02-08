"""Quickstart: show how to switch backends with the factory."""

import os

from mem_llm import LLMClientFactory


BACKENDS = (
    ("ollama", os.getenv("OLLAMA_MODEL", "granite4:3b")),
    ("lmstudio", os.getenv("LMSTUDIO_MODEL", "google/gemma-3-4b")),
)


def main() -> None:
    for backend in ("ollama", "lmstudio"):
        available = LLMClientFactory.check_backend_availability(backend)
        print(f"{backend} available:", available)

    for backend, model in BACKENDS:
        try:
            client = LLMClientFactory.create(backend, model=model)
            print(f"{backend} active backend:", client.get_info().get("backend"))
        except Exception as exc:
            print(f"{backend} Error:", exc)


if __name__ == "__main__":
    main()
