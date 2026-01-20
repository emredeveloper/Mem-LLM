"""Quickstart: basic chat example with a local backend."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(backend="ollama", model="granite4:3b", check_connection=False)
    agent.set_user("quickstart_user")

    response = agent.chat("Hello! Give me a short greeting.")
    print("Bot:", response)


if __name__ == "__main__":
    main()
