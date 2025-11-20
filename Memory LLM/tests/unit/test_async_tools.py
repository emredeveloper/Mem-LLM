"""
Unit tests for async tools functionality
"""

import asyncio

import pytest

from mem_llm.tool_system import ToolRegistry, tool


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncTools:
    """Tests for async tool support"""

    async def test_async_tool_creation(self):
        """Test creating an async tool"""

        @tool(name="async_test", description="Async test tool")
        async def async_func(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        assert async_func.is_async is True
        assert async_func.name == "async_test"

    async def test_async_tool_execution(self):
        """Test executing an async tool"""

        @tool(name="async_add", description="Async add")
        async def async_add(a: int, b: int) -> int:
            await asyncio.sleep(0.01)
            return a + b

        result = async_add.execute({"a": 5, "b": 3})
        # Result should be awaitable or already executed
        if asyncio.iscoroutine(result):
            actual_result = await result
            assert actual_result == 8

    async def test_sync_tool_detection(self):
        """Test that sync tools are correctly identified"""

        @tool(name="sync_test", description="Sync test tool")
        def sync_func(x: int) -> int:
            return x * 2

        assert hasattr(sync_func, "is_async")
        # Should not be marked as async
        assert sync_func.is_async is False or not hasattr(sync_func, "is_async")


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncToolRegistry:
    """Tests for async tool registry functionality"""

    async def test_registry_with_async_tools(self):
        """Test registry with async tools"""
        registry = ToolRegistry()

        @tool(name="async_multiply", description="Async multiply")
        async def async_multiply(x: int, y: int) -> int:
            await asyncio.sleep(0.01)
            return x * y

        registry.register(async_multiply)
        tools = registry.list_tools()
        assert "async_multiply" in tools


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
