"""Quickstart: memory recall with two messages."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(backend="ollama", model="granite4:3b", check_connection=False)
    agent.set_user("quickstart_user")

    agent.chat("My name is Alex.")
    reply = agent.chat("What is my name?")
    print("Bot:", reply)


if __name__ == "__main__":
    main()
