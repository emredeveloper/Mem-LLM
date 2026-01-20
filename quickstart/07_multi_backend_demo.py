"""Quickstart: show how to switch backends with the factory."""

from mem_llm import LLMClientFactory


def main() -> None:
    for backend in ("ollama", "lmstudio"):
        available = LLMClientFactory.check_backend_availability(backend)
        print(f"{backend} available:", available)

    client = LLMClientFactory.create("ollama", model="granite4:3b")
    print("Active backend:", client.get_info().get("backend"))


if __name__ == "__main__":
    main()
