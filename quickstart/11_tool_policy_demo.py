"""Demonstrate tool allowlist/denylist policy."""

from mem_llm.tool_system import ToolRegistry, tool

TOOL_ALLOWLIST = ["safe_upper"]
TOOL_DENYLIST = ["unsafe_lower"]
TOOL_ALLOWLIST_ONLY = True


@tool(name="safe_upper", description="Uppercase a string")
def safe_upper(value: str) -> str:
    return value.upper()


@tool(name="unsafe_lower", description="Lowercase a string")
def unsafe_lower(value: str) -> str:
    return value.lower()


def main() -> None:
    registry = ToolRegistry(
        allowlist=TOOL_ALLOWLIST,
        denylist=TOOL_DENYLIST,
        allowlist_only=TOOL_ALLOWLIST_ONLY,
    )
    registry.register_function(safe_upper)
    registry.register_function(unsafe_lower)

    ok = registry.execute("safe_upper", value="Hello")
    blocked = registry.execute("unsafe_lower", value="Hello")

    print("safe_upper:", ok.status.value, ok.result)
    print("unsafe_lower:", blocked.status.value, blocked.error)


if __name__ == "__main__":
    main()
