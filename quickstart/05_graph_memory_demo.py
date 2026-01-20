"""Quickstart: enable graph memory and inspect stored triplets."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(
        backend="ollama",
        model="granite4:3b",
        enable_graph_memory=True,
        check_connection=False,
    )
    agent.set_user("quickstart_user")

    agent.chat("My favorite language is Python.")
    agent.chat("I live in Berlin.")

    if agent.graph_store:
        print(agent.graph_store.get_summary())
        print("Triplets:", agent.graph_store.search("Python"))
    else:
        print("Graph memory is not available (missing optional dependencies).")


if __name__ == "__main__":
    main()
