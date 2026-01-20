"""Quickstart: register a custom tool and invoke it."""

from mem_llm import MemAgent, tool


@tool(name="greet", description="Greet a user by name")
def greet(name: str) -> str:
    return f"Hello, {name}!"


def main() -> None:
    agent = MemAgent(
        backend="ollama",
        model="granite4:3b",
        enable_tools=True,
        tools=[greet],
        check_connection=False,
    )
    agent.set_user("quickstart_user")

    response = agent.chat('TOOL_CALL: greet(name="Taylor")')
    print("Bot:", response)


if __name__ == "__main__":
    main()
