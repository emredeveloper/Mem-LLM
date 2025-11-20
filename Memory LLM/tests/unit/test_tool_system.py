"""
Unit tests for the tool system (ToolRegistry, Tool, @tool decorator)
"""

import pytest

from mem_llm.tool_system import Tool, ToolParameter, ToolRegistry, tool


@pytest.mark.unit
class TestToolParameter:
    """Tests for ToolParameter dataclass"""

    def test_basic_parameter(self):
        """Test basic parameter creation"""
        param = ToolParameter(
            name="test_param",
            type="str",  # Note: it's 'type', not 'param_type'
            description="Test parameter",
        )
        assert param.name == "test_param"
        assert param.type == "str"
        assert param.description == "Test parameter"


@pytest.mark.unit
class TestTool:
    """Tests for Tool class"""

    def test_tool_creation(self):
        """Test basic tool creation"""

        def sample_func(x: int) -> str:
            return str(x)

        tool_obj = Tool(
            name="sample_tool",
            description="A sample tool",
            function=sample_func,
            parameters=[ToolParameter(name="x", type="integer", description="Input number")],
        )

        assert tool_obj.name == "sample_tool"
        assert tool_obj.description == "A sample tool"
        assert callable(tool_obj.function)


@pytest.mark.unit
class TestToolDecorator:
    """Tests for @tool decorator"""

    def test_basic_decorator(self):
        """Test basic tool decorator usage"""

        @tool(name="greet", description="Greet someone")
        def greet_user(name: str) -> str:
            return f"Hello, {name}!"

        # The decorator adds _tool attribute
        assert hasattr(greet_user, "_tool")
        assert greet_user._tool.name == "greet"
        assert greet_user._tool.description == "Greet someone"


@pytest.mark.unit
class TestToolRegistry:
    """Tests for ToolRegistry"""

    def test_registry_creation(self):
        """Test registry creation"""
        registry = ToolRegistry()
        # Registry should be created successfully
        assert registry is not None

    def test_register_tool(self):
        """Test registering a tool"""
        registry = ToolRegistry()

        @tool(name="test_tool", description="Test")
        def test_func(x: int) -> int:
            return x * 2

        # Register using the _tool attribute
        registry.register(test_func._tool)
        tools = registry.list_tools()
        assert "test_tool" in tools


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
