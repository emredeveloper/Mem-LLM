"""Extract and store graph triplets."""

from mem_llm.mem_agent import MemAgent

from demo_config import BACKEND, BASE_URL, MODEL


def main() -> None:
    agent = MemAgent(
        model=MODEL,
        backend=BACKEND,
        base_url=BASE_URL,
        enable_graph_memory=True,
    )

    text = "Alice knows Bob. Bob lives in Paris."
    triplets = agent.graph_extractor.extract(text)

    for source, relation, target in triplets:
        agent.graph_store.add_triplet(source, relation, target)

    print(agent.graph_store.get_summary())


if __name__ == "__main__":
    main()
