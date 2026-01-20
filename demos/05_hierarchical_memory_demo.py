"""Add interactions and retrieve hierarchical context."""

from mem_llm.mem_agent import MemAgent

from demo_config import BACKEND, BASE_URL, MODEL


def main() -> None:
    agent = MemAgent(
        model=MODEL,
        backend=BACKEND,
        base_url=BASE_URL,
        enable_hierarchical_memory=True,
    )

    agent.set_user("demo_user")
    agent.hierarchical_memory.add_interaction(
        user_id="demo_user",
        user_message="I like hiking in the mountains.",
        bot_response="That sounds refreshing.",
    )
    agent.hierarchical_memory.add_interaction(
        user_id="demo_user",
        user_message="I also enjoy Python for data analysis.",
        bot_response="Great choice for analysis.",
    )

    context = agent.hierarchical_memory.get_context(user_id="demo_user")
    print(context)


if __name__ == "__main__":
    main()
