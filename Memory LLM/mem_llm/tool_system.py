"""
Tool System for Function Calling
=================================

Enables agents to call external functions/tools to perform actions.
Inspired by OpenAI's function calling and LangChain's tool system.

Features:
- Decorator-based tool definition
- Automatic schema generation from type hints
- Tool execution with error handling
- Tool result formatting
- Built-in common tools

Author: Cihat Emre Karataş
Version: 2.1.1
"""

import asyncio
import inspect
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union, get_type_hints

logger = logging.getLogger(__name__)


class ToolCallStatus(Enum):
    """Status of tool call execution"""

    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    INVALID_ARGS = "invalid_args"


@dataclass
class ToolParameter:
    """Tool parameter definition with validation (v2.1.0+)"""

    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    # Validation (v2.1.0+)
    pattern: Optional[str] = None  # Regex pattern for strings
    min_value: Optional[Union[int, float]] = None  # Minimum value for numbers
    max_value: Optional[Union[int, float]] = None  # Maximum value for numbers
    min_length: Optional[int] = None  # Minimum length for strings/lists
    max_length: Optional[int] = None  # Maximum length for strings/lists
    choices: Optional[List[Any]] = None  # Allowed values
    validator: Optional[Callable[[Any], bool]] = None  # Custom validator function


@dataclass
class Tool:
    """Tool definition with async support (v2.1.0+)"""

    name: str
    description: str
    function: Callable
    parameters: List[ToolParameter] = field(default_factory=list)
    return_type: str = "string"
    category: str = "general"
    is_async: bool = field(default=False, init=False)

    def __post_init__(self):
        """Detect if function is async"""
        self.is_async = asyncio.iscoroutinefunction(self.function)

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format for LLM"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": {
                "type": "object",
                "properties": {
                    param.name: {"type": param.type, "description": param.description}
                    for param in self.parameters
                },
                "required": [p.name for p in self.parameters if p.required],
            },
            "return_type": self.return_type,
        }

    def validate_arguments(self, **kwargs) -> Dict[str, Any]:
        """
        Validate tool arguments with comprehensive validation (v2.1.0+)

        Returns:
            Validated arguments or raises ValueError
        """
        validated = {}

        for param in self.parameters:
            value = kwargs.get(param.name, param.default)

            # Check required
            if param.required and value is None:
                raise ValueError(f"Missing required parameter: {param.name}")

            if value is None:
                validated[param.name] = value
                continue

            # Type validation
            param_type = param.type.lower()

            # String validations
            if param_type == "string" and isinstance(value, str):
                if param.pattern and not re.match(param.pattern, value):
                    raise ValueError(
                        f"Parameter '{param.name}' does not match pattern: {param.pattern}"
                    )
                if param.min_length and len(value) < param.min_length:
                    raise ValueError(
                        f"Parameter '{param.name}' too short (min: {param.min_length})"
                    )
                if param.max_length and len(value) > param.max_length:
                    raise ValueError(f"Parameter '{param.name}' too long (max: {param.max_length})")

            # Number validations
            if param_type in ["number", "integer"] and isinstance(value, (int, float)):
                if param.min_value is not None and value < param.min_value:
                    raise ValueError(f"Parameter '{param.name}' too small (min: {param.min_value})")
                if param.max_value is not None and value > param.max_value:
                    raise ValueError(f"Parameter '{param.name}' too large (max: {param.max_value})")

            # Choices validation
            if param.choices and value not in param.choices:
                raise ValueError(f"Parameter '{param.name}' must be one of: {param.choices}")

            # Custom validator
            if param.validator and not param.validator(value):
                raise ValueError(f"Parameter '{param.name}' failed custom validation")

            validated[param.name] = value

        return validated

    def execute(self, **kwargs) -> Any:
        """
        Execute the tool with arguments (supports async v2.1.0+)
        """
        try:
            # Validate arguments (v2.1.0+)
            validated_kwargs = self.validate_arguments(**kwargs)

            # Execute function
            if self.is_async:
                # Run async function
                try:
                    asyncio.get_running_loop()
                    # Already in async context, create task
                    return asyncio.create_task(self.function(**validated_kwargs))
                except RuntimeError:
                    # No running loop, run in new loop
                    return asyncio.run(self.function(**validated_kwargs))
            else:
                # Sync function
                return self.function(**validated_kwargs)
        except Exception as e:
            logger.error(f"Tool execution error ({self.name}): {e}")
            raise


@dataclass
class ToolCallResult:
    """Result of a tool call"""

    tool_name: str
    status: ToolCallStatus
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: str = "general",
    # Validation parameters (v2.1.0+)
    pattern: Optional[Dict[str, str]] = None,  # {param_name: regex_pattern}
    min_value: Optional[Dict[str, Union[int, float]]] = None,  # {param_name: min}
    max_value: Optional[Dict[str, Union[int, float]]] = None,  # {param_name: max}
    min_length: Optional[Dict[str, int]] = None,  # {param_name: min_len}
    max_length: Optional[Dict[str, int]] = None,  # {param_name: max_len}
    choices: Optional[Dict[str, List[Any]]] = None,  # {param_name: [valid_values]}
    validators: Optional[Dict[str, Callable]] = None,  # {param_name: validator_func}
) -> Callable:
    r"""
    Decorator to define a tool/function that the agent can call.

    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
        category: Tool category for organization
        pattern: Regex patterns for string parameters (v2.1.0+)
        min_value: Minimum values for number parameters (v2.1.0+)
        max_value: Maximum values for number parameters (v2.1.0+)
        min_length: Minimum length for string/list parameters (v2.1.0+)
        max_length: Maximum length for string/list parameters (v2.1.0+)
        choices: Allowed values for parameters (v2.1.0+)
        validators: Custom validator functions (v2.1.0+)

    Example:
        @tool(name="calculate", description="Perform mathematical calculations")
        def calculator(expression: str) -> float:
            '''Evaluate a mathematical expression'''
            return eval(expression)

        # With validation (v2.1.0+):
        @tool(
            name="validate_email",
            pattern={"email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'},
            min_length={"email": 5},
            max_length={"email": 254}
        )
        def send_email(email: str) -> str:
            return f"Email sent to {email}"
    """

    def decorator(func: Callable) -> Tool:
        # Get function metadata
        func_name = name or func.__name__
        func_desc = description or (func.__doc__ or "").strip()

        # Extract parameters from type hints
        type_hints = get_type_hints(func)
        sig = inspect.signature(func)
        parameters = []

        for param_name, param in sig.parameters.items():
            if param_name in type_hints:
                param_type = type_hints[param_name]
                # Map Python types to JSON schema types
                type_map = {
                    str: "string",
                    int: "integer",
                    float: "number",
                    bool: "boolean",
                    list: "array",
                    dict: "object",
                }
                json_type = type_map.get(param_type, "string")
            else:
                json_type = "string"

            param_desc = f"Parameter: {param_name}"
            required = param.default == inspect.Parameter.empty

            # Add validation parameters (v2.1.0+)
            param_obj = ToolParameter(
                name=param_name,
                type=json_type,
                description=param_desc,
                required=required,
                default=param.default if param.default != inspect.Parameter.empty else None,
                pattern=pattern.get(param_name) if pattern else None,
                min_value=min_value.get(param_name) if min_value else None,
                max_value=max_value.get(param_name) if max_value else None,
                min_length=min_length.get(param_name) if min_length else None,
                max_length=max_length.get(param_name) if max_length else None,
                choices=choices.get(param_name) if choices else None,
                validator=validators.get(param_name) if validators else None,
            )
            parameters.append(param_obj)

        # Get return type
        return_type = "string"
        if "return" in type_hints:
            ret_type = type_hints["return"]
            type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}
            return_type = type_map.get(ret_type, "string")

        # Create Tool object
        tool_obj = Tool(
            name=func_name,
            description=func_desc,
            function=func,
            parameters=parameters,
            return_type=return_type,
            category=category,
        )

        # Attach tool metadata to function
        func._tool = tool_obj
        return func

    return decorator


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._load_builtin_tools()

    def _load_builtin_tools(self):
        """Load built-in tools"""
        # Import built-in tools when available
        try:
            from .builtin_tools import BUILTIN_TOOLS

            for tool_func in BUILTIN_TOOLS:
                if hasattr(tool_func, "_tool"):
                    self.register(tool_func._tool)
        except ImportError:
            pass

        # Load async built-in tools (v2.1.0+)
        try:
            from .builtin_tools_async import ASYNC_BUILTIN_TOOLS

            for tool_func in ASYNC_BUILTIN_TOOLS:
                if hasattr(tool_func, "_tool"):
                    self.register(tool_func._tool)
        except ImportError:
            pass

    def register(self, tool: Tool):
        """Register a tool"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def register_tool(self, tool_or_func):
        """
        Register a tool (alias for backward compatibility and convenience)

        Args:
            tool_or_func: Either a Tool object or a decorated function
        """
        if isinstance(tool_or_func, Tool):
            self.register(tool_or_func)
        elif hasattr(tool_or_func, "_tool"):
            self.register(tool_or_func._tool)
        else:
            # Try to treat it as a function
            self.register_function(tool_or_func)

    def register_function(self, func: Callable):
        """Register a function as a tool"""
        if hasattr(func, "_tool"):
            self.register(func._tool)
        else:
            # Auto-create tool from function
            tool_obj = tool()(func)
            if hasattr(tool_obj, "_tool"):
                self.register(tool_obj._tool)

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name (alias for get())"""
        return self.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Tool]:
        """List all tools, optionally filtered by category"""
        tools = list(self.tools.values())
        if category:
            tools = [t for t in tools if t.category == category]
        return tools

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get schema for all tools (for LLM prompt)"""
        return [tool.to_dict() for tool in self.tools.values()]

    def execute(self, tool_name: str, **kwargs) -> ToolCallResult:
        """Execute a tool by name"""
        import time

        start_time = time.time()

        # Get tool
        tool = self.get(tool_name)
        if not tool:
            # Log available tools for debugging
            available_tools = list(self.tools.keys())
            logger.warning(f"Tool '{tool_name}' not found in call. Available tools: {available_tools}. Full match: {match.group(0) if 'match' in locals() else 'N/A'}")
            return ToolCallResult(
                tool_name=tool_name,
                status=ToolCallStatus.NOT_FOUND,
                error=f"Tool '{tool_name}' not found. Available tools: {available_tools}",
                execution_time=time.time() - start_time,
            )

        # Execute tool
        try:
            result = tool.execute(**kwargs)
            return ToolCallResult(
                tool_name=tool_name,
                status=ToolCallStatus.SUCCESS,
                result=result,
                execution_time=time.time() - start_time,
            )
        except ValueError as e:
            return ToolCallResult(
                tool_name=tool_name,
                status=ToolCallStatus.INVALID_ARGS,
                error=str(e),
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            return ToolCallResult(
                tool_name=tool_name,
                status=ToolCallStatus.ERROR,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class ToolCallParser:
    """Parse LLM output to detect and extract tool calls"""

    # Pattern to detect tool calls in LLM output
    # Format: TOOL_CALL: tool_name(arg1="value1", arg2="value2")
    # Using a more robust pattern that handles nested parentheses and validates tool names
    TOOL_CALL_PATTERN = r"TOOL_CALL:\s*([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)(?=\s|$|[^a-zA-Z0-9_\(])"

    # Alternative patterns for natural language tool calls (v2.1.3+)
    # Updated to better handle nested parentheses and validate tool names
    NATURAL_PATTERNS = [
        (
            r"(?:using|use|call|execute)\s+(?:the\s+)?[`']?([a-zA-Z_][a-zA-Z0-9_]*)[`']?\s+"
            r"(?:tool|function)?\s*(?:with|to|on)?\s*\((.*?)\)(?=\s|$|[.!?])"
        ),
        r"(?:tool|function)\s+[`']?([a-zA-Z_][a-zA-Z0-9_]*)[`']?\s*\((.*?)\)(?=\s|$|[.!?])",
        r"`([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)`",  # Markdown code format
    ]

    @staticmethod
    def parse(text: str) -> List[Dict[str, Any]]:
        """
        Parse text to extract tool calls.
        Supports both explicit TOOL_CALL format and natural language (v2.1.3+).

        Returns:
            List of dicts with 'tool' and 'arguments' keys
        """
        logger.debug(f"Attempting to parse tool calls from text: {text[:200]}...")
        tool_calls = []

        # Try explicit TOOL_CALL format first
        matches = re.finditer(ToolCallParser.TOOL_CALL_PATTERN, text, re.MULTILINE)
        matches_list = list(matches)

        logger.debug(f"Found {len(matches_list)} matches with explicit TOOL_CALL pattern")

        # If no explicit format found, try natural language patterns (v2.1.3+)
        if not matches_list:
            for pattern in ToolCallParser.NATURAL_PATTERNS:
                pattern_matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
                matches_list.extend(pattern_matches)
                logger.debug(f"Pattern '{pattern[:30]}...' found {len(pattern_matches)} matches")
                if pattern_matches:
                    logger.info(
                        f"🔍 Detected natural language tool call using pattern: {pattern[:50]}..."
                    )
                    break

        matches = matches_list

        logger.debug(f"Total matches found: {len(matches)}")

        for match in matches:
            # Extract the full tool call string to handle nested parentheses properly
            full_match_str = match.group(0)
            tool_name = match.group(1)
            # Get the argument part for debugging too
            try:
                args_str = match.group(2)
            except IndexError:
                args_str = ""

            logger.debug(f"Full match: '{full_match_str}', Tool name: '{tool_name}', Args: '{args_str}'")

            # Validate that the tool name is a valid identifier to prevent issues like 'tool_name'
            # This prevents cases where LLM generates something like "tool_name" as a literal instead of a real tool name
            import re
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tool_name):
                logger.warning(f"Invalid tool name format: '{tool_name}'. Skipping this match: {full_match_str}")
                continue

            # More robust argument extraction that handles nested parentheses
            extracted_args = ToolCallParser._extract_arguments(full_match_str, tool_name)

            # Debug logging to help with troubleshooting
            logger.debug(f"Parsed tool call - Name: '{tool_name}', Args: '{extracted_args}'")

            # Parse arguments
            arguments = {}
            if extracted_args.strip():
                try:
                    # Try to parse as Python kwargs
                    # Handle both key="value" and positional args
                    args_dict = {}

                    # Split by comma, but respect quotes and parentheses
                    parts = []
                    current = ""
                    in_quotes = False
                    paren_depth = 0
                    quote_char = None

                    for char in extracted_args:
                        if char in ['"', "'"] and quote_char is None:
                            quote_char = char
                            in_quotes = True
                            current += char
                        elif char == quote_char:
                            in_quotes = False
                            quote_char = None
                            current += char
                        elif char == "(" and not in_quotes:
                            paren_depth += 1
                            current += char
                        elif char == ")" and not in_quotes:
                            paren_depth -= 1
                            current += char
                        elif char == "," and not in_quotes and paren_depth == 0:
                            if current.strip():
                                parts.append(current.strip())
                            current = ""
                        else:
                            current += char

                    if current.strip():
                        parts.append(current.strip())

                    # Parse each part
                    for i, part in enumerate(parts):
                        if "=" in part and not part.strip().startswith('"'):
                            key, value = part.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip("\"'")
                            args_dict[key] = value
                        else:
                            # Positional argument - use index as key
                            value = part.strip().strip("\"'")
                            # Try to infer parameter name from common patterns
                            if i == 0 and value:
                                # First arg is usually the main parameter
                                if tool_name == "calculate":
                                    args_dict["expression"] = value
                                elif tool_name in [
                                    "count_words",
                                    "reverse_text",
                                    "to_uppercase",
                                    "to_lowercase",
                                ]:
                                    args_dict["text"] = value
                                elif tool_name == "get_weather":
                                    args_dict["city"] = value
                                elif tool_name in ["read_file", "write_file"]:
                                    args_dict["filepath"] = value
                                else:
                                    args_dict[f"arg{i}"] = value

                    arguments = args_dict
                except Exception as e:
                    logger.warning(f"Failed to parse arguments: {extracted_args} - Error: {e}")

            tool_calls.append({"tool": tool_name, "arguments": arguments})

        logger.debug(f"Returning {len(tool_calls)} tool calls: {tool_calls}")
        return tool_calls

    @staticmethod
    def _extract_arguments(full_match_str: str, tool_name: str) -> str:
        """
        Extract arguments from a tool call string, properly handling nested parentheses.

        Args:
            full_match_str: Full matched tool call string (e.g., "TOOL_CALL: calculate((25 * 4) + 10)")
            tool_name: Name of the tool

        Returns:
            Arguments string extracted from the tool call
        """
        # Find the position of the first opening parenthesis after the tool name
        paren_pos = -1
        tool_name_pos = full_match_str.find(tool_name)
        if tool_name_pos != -1:
            paren_pos = full_match_str.find('(', tool_name_pos + len(tool_name))

        if paren_pos == -1:
            return ""

        # Now extract the content between parentheses, handling nested ones
        paren_count = 0
        start_pos = paren_pos + 1  # Start after the first '('
        for i in range(start_pos, len(full_match_str)):
            char = full_match_str[i]
            if char == '(':
                paren_count += 1
            elif char == ')':
                if paren_count == 0:
                    # This is the matching closing parenthesis
                    return full_match_str[start_pos:i]
                paren_count -= 1

        # If we get here, parentheses weren't properly matched
        # Return what we have until the end (this might happen with malformed input)
        return full_match_str[start_pos:]

    @staticmethod
    def has_tool_call(text: str) -> bool:
        """Check if text contains a tool call"""
        return bool(re.search(ToolCallParser.TOOL_CALL_PATTERN, text))

    @staticmethod
    def remove_tool_calls(text: str) -> str:
        """Remove tool call syntax from text, keeping only natural language"""
        return re.sub(ToolCallParser.TOOL_CALL_PATTERN, "", text).strip()


def format_tools_for_prompt(tools: List[Tool]) -> str:
    """
    Format tools as a string for LLM prompt.

    Returns:
        Formatted string describing available tools
    """
    if not tools:
        return ""

    lines = ["You have access to the following tools:"]
    lines.append("")

    for tool in tools:
        lines.append(f"- **{tool.name}**: {tool.description}")

        if tool.parameters:
            lines.append("  Parameters:")
            for param in tool.parameters:
                req = "required" if param.required else "optional"
                lines.append(f"    - {param.name} ({param.type}, {req}): {param.description}")

        lines.append("")

    lines.append("=" * 80)
    lines.append("⚡ TOOL USAGE INSTRUCTIONS (v2.1.3+):")
    lines.append("-" * 80)
    lines.append("✅ PREFERRED FORMAT (use this!):")
    lines.append('  TOOL_CALL: tool_name(param1="value1", param2="value2")')
    lines.append("")
    lines.append("📝 EXAMPLES:")
    lines.append('  TOOL_CALL: calculate(expression="(25 * 4) + 10")')
    lines.append('  TOOL_CALL: count_words(text="Hello world from AI")')
    lines.append('  TOOL_CALL: write_file(filepath="test.txt", content="Hello!")')
    lines.append("  TOOL_CALL: get_current_time()")
    lines.append("")
    lines.append("🔥 CRITICAL RULES:")
    lines.append("  1. USE THE EXACT FORMAT ABOVE - Don't just describe, actually CALL!")
    lines.append('  2. Always use named parameters: param="value"')
    lines.append("  3. Use double quotes for string values")
    lines.append("  4. One tool call per line")
    lines.append("  5. After execution, tool results appear and you continue responding")
    lines.append("")
    lines.append("❌ WRONG: The tool 'calculate' can solve this...")
    lines.append('✅ RIGHT: TOOL_CALL: calculate(expression="5 + 3")')
    lines.append("=" * 80)
    lines.append("")

    return "\n".join(lines)
