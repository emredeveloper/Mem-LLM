"""Quickstart: stream a response chunk-by-chunk."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(backend="ollama", model="granite4:3b", check_connection=False)
    agent.set_user("quickstart_user")

    print("Bot:", end=" ")
    for chunk in agent.chat_stream("Tell me a short story about a cat."):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
