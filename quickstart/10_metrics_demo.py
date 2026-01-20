"""Quickstart: collect response metrics."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(backend="ollama", model="granite4:3b", check_connection=False)
    agent.set_user("quickstart_user")

    response = agent.chat("What is a black hole?", return_metrics=True)
    print("Text:", response.text)
    print("Confidence:", response.confidence)
    print("Latency (ms):", round(response.latency, 1))


if __name__ == "__main__":
    main()
