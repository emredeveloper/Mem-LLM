"""Quickstart: enable tools and use the calculator tool."""

from mem_llm import MemAgent


def main() -> None:
    agent = MemAgent(
        backend="ollama",
        model="granite4:3b",
        enable_tools=True,
        check_connection=False,
    )
    agent.set_user("quickstart_user")

    response = agent.chat('TOOL_CALL: calculate(expression="(25 * 4) + 10")')
    print("Bot:", response)


if __name__ == "__main__":
    main()
