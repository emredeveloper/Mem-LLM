"""Security hardening unit tests."""

import asyncio
import importlib
import shutil
from pathlib import Path

import pytest

from mem_llm.builtin_tools import calculate
from mem_llm.tool_system import ToolRegistry, tool
from mem_llm.tool_workspace import ToolWorkspace


@pytest.mark.unit
def test_calculate_blocks_unsafe_expression():
    """`calculate` should reject code-like payloads."""
    payload = "[c for c in ().__class__.__base__.__subclasses__()]"
    with pytest.raises(ValueError):
        calculate(payload)


@pytest.mark.unit
def test_tool_workspace_blocks_path_traversal():
    """Workspace should not allow escaping via relative or absolute paths."""
    workspace_root = Path("workspace_test_tmp")
    if workspace_root.exists():
        shutil.rmtree(workspace_root)

    try:
        workspace = ToolWorkspace(base_dir=str(workspace_root))

        with pytest.raises(ValueError):
            workspace.get_file_path("../../escape.txt")

        with pytest.raises(ValueError):
            workspace.get_file_path("C:/Windows/temp/escape.txt")
    finally:
        if workspace_root.exists():
            shutil.rmtree(workspace_root)


@pytest.mark.unit
def test_auth_is_enabled_by_default(monkeypatch):
    """Auth should be on unless explicitly disabled via env."""
    pytest.importorskip("fastapi")

    monkeypatch.delenv("MEM_LLM_AUTH_DISABLED", raising=False)
    monkeypatch.delenv("MEM_LLM_API_KEY", raising=False)

    import mem_llm.api_auth as api_auth

    api_auth = importlib.reload(api_auth)

    assert api_auth.AUTH_DISABLED is False
    assert api_auth.DEFAULT_API_KEY
    assert api_auth.DEFAULT_API_KEY != "dev-api-key-change-in-production"


@pytest.mark.unit
def test_registry_executes_async_tool_inside_running_loop():
    """Tool registry should return final result, not a Task object, in active loops."""
    registry = ToolRegistry()

    @tool(name="async_square", description="Square a number asynchronously")
    async def async_square(x: int) -> int:
        await asyncio.sleep(0.01)
        return x * x

    registry.register(async_square._tool)

    async def _run_check():
        result = registry.execute("async_square", x=4)
        assert result.status.value == "success"
        assert result.result == 16

    asyncio.run(_run_check())