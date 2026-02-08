"""Quickstart: register a custom tool and invoke it."""

import os

from mem_llm import MemAgent
from mem_llm.tool_system import tool


@tool(name="greet", description="Greet a user by name")
def greet(name: str) -> str:
    return f"Hello, {name}!"


BACKENDS = (
    ("ollama", os.getenv("OLLAMA_MODEL", "granite4:3b")),
    ("lmstudio", os.getenv("LMSTUDIO_MODEL", "google/gemma-3-4b")),
)


def run_backend(backend: str, model: str) -> None:
    try:
        agent = MemAgent(
            backend=backend,
            model=model,
            enable_tools=True,
            tools=[greet],
            check_connection=False,
        )
        agent.set_user("quickstart_user")

        response = agent.chat('TOOL_CALL: greet(name="Taylor")')
        print(f"[{backend}] Bot:", response)
    except Exception as exc:
        print(f"[{backend}] Error:", exc)


def main() -> None:
    for backend, model in BACKENDS:
        run_backend(backend, model)


if __name__ == "__main__":
    main()
