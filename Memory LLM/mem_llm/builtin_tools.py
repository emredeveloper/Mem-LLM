"""
Built-in Tools
==============

Common tools that are available by default.

Author: Cihat Emre Karataş
Version: 2.1.3
"""

import json
import math
import os
import platform
import random
import uuid
from datetime import datetime
from typing import List

import psutil

from .tool_system import tool
from .tool_workspace import get_workspace

# ============================================================================
# Math & Calculation Tools
# ============================================================================


@tool(name="calculate", description="Evaluate mathematical expressions", category="math")
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: Mathematical expression (e.g., "2 + 2", "sqrt(16)", "pi * 2", "(25 * 4) + 10")

    Returns:
        Result of the calculation

    Examples:
        calculate("2 + 2") -> 4.0
        calculate("sqrt(16)") -> 4.0
        calculate("pi * 2") -> 6.283185307179586
        calculate("(25 * 4) + 10") -> 110.0
    """
    # Safe eval with math functions
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["abs"] = abs
    allowed_names["round"] = round
    allowed_names["min"] = min
    allowed_names["max"] = max
    allowed_names["sum"] = sum

    try:
        # Clean up expression - replace common text with symbols
        clean_expr = expression.strip()
        clean_expr = clean_expr.replace(" divided by ", " / ")
        clean_expr = clean_expr.replace(" times ", " * ")
        clean_expr = clean_expr.replace(" plus ", " + ")
        clean_expr = clean_expr.replace(" minus ", " - ")

        result = eval(clean_expr, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression '{expression}': {str(e)}")


# ============================================================================
# Text Processing Tools
# ============================================================================


@tool(name="count_words", description="Count words in text", category="text")
def count_words(text: str) -> int:
    """
    Count the number of words in a text.

    Args:
        text: Text to count words in

    Returns:
        Number of words
    """
    return len(text.split())


@tool(name="reverse_text", description="Reverse a text string", category="text")
def reverse_text(text: str) -> str:
    """
    Reverse the order of characters in text.

    Args:
        text: Text to reverse

    Returns:
        Reversed text
    """
    return text[::-1]


@tool(name="to_uppercase", description="Convert text to uppercase", category="text")
def to_uppercase(text: str) -> str:
    """
    Convert text to uppercase.

    Args:
        text: Text to convert

    Returns:
        Uppercase text
    """
    return text.upper()


@tool(name="to_lowercase", description="Convert text to lowercase", category="text")
def to_lowercase(text: str) -> str:
    """
    Convert text to lowercase.

    Args:
        text: Text to convert

    Returns:
        Lowercase text
    """
    return text.lower()


# ============================================================================
# File System Tools
# ============================================================================


@tool(name="read_file", description="Read contents of a text file", category="file")
def read_file(filepath: str) -> str:
    """
    Read and return the contents of a text file.

    Args:
        filepath: Path to the file to read

    Returns:
        File contents as string
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")


@tool(
    name="write_file", description="Write text to a file (v2.1.3: uses workspace)", category="file"
)
def write_file(filepath: str, content: str) -> str:
    """
    Write text content to a file in the tool workspace.

    Args:
        filepath: Filename (stored in tool_workspace/)
        content: Content to write to the file

    Returns:
        Success message with full path
    """
    try:
        workspace = get_workspace()
        full_path = workspace.get_file_path(filepath)

        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {full_path}"
    except Exception as e:
        raise ValueError(f"Error writing file: {e}")


@tool(name="list_files", description="List files in a directory", category="file")
def list_files(directory: str) -> List[str]:
    """
    List all files in a directory.

    Args:
        directory: Path to the directory

    Returns:
        List of filenames
    """
    try:
        return os.listdir(directory)
    except Exception as e:
        raise ValueError(f"Error listing directory: {e}")


# ============================================================================
# Utility Tools
# ============================================================================


@tool(name="get_current_time", description="Get current date and time", category="utility")
def get_current_time() -> str:
    """
    Get the current date and time.

    Returns:
        Current datetime as string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool(name="create_json", description="Create JSON from key-value pairs", category="utility")
def create_json(key: str, value: str) -> str:
    """
    Create a simple JSON object from a key-value pair.

    Args:
        key: JSON key
        value: JSON value

    Returns:
        Formatted JSON string

    Example:
        create_json("name", "John") -> {"name": "John"}
    """
    try:
        # Try to parse value as JSON type
        try:
            parsed_value = json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            parsed_value = value

        result = {key: parsed_value}
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error creating JSON: {e}"


@tool(name="get_system_info", description="Get system environment information", category="utility")
def get_system_info() -> str:
    """
    Get information about the system environment.

    Returns:
        System information (OS, CPU, Memory)
    """
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory()
    total_mem_gb = round(memory.total / (1024**3), 2)
    os_info = f"{platform.system()} {platform.release()}"

    return (
        f"🖥️ System Info:\n"
        f"  OS: {os_info}\n"
        f"  CPU: {cpu_count} cores\n"
        f"  Memory: {total_mem_gb} GB\n"
        f"  Python: {platform.python_version()}"
    )


@tool(name="generate_random", description="Generate random strings or UUIDs", category="utility")
def generate_random(type: str = "uuid", length: int = 12) -> str:
    """
    Generate a random string or UUID.

    Args:
        type: Type of random string ('uuid', 'hex', 'password')
        length: Length for hex/password (default: 12)

    Returns:
        Generated random string
    """
    if type == "uuid":
        return str(uuid.uuid4())
    elif type == "hex":
        return "".join(random.choices("0123456789abcdef", k=length))
    elif type == "password":
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return "".join(random.choices(chars, k=length))
    return f"Unsupported type: {type}"


# ============================================================================
# Memory & Context Tools (NEW in v2.0.0)
# ============================================================================


@tool(name="search_memory", description="Search through conversation history", category="memory")
def search_memory(query: str, limit: int = 5) -> str:
    """
    Search through conversation history for a keyword or phrase.

    Args:
        query: The keyword/phrase to search for in conversation history
        limit: Maximum number of results to return (default: 5)

    Returns:
        Search results or error message

    Examples:
        search_memory("weather", 3) -> "Found 2 conversations about weather..."

    Note:
        This tool requires MemAgent context. Will return instructions if called standalone.
    """
    # This is a placeholder - actual implementation happens in MemAgent._execute_tool_calls
    return f"MEMORY_SEARCH:{query}:{limit}"


@tool(name="get_user_info", description="Get current user profile information", category="memory")
def get_user_info() -> str:
    """
    Get information about the current user.

    Returns:
        User profile information

    Examples:
        get_user_info() -> "Current user: john_doe (active since 2025-01-15)"

    Note:
        This tool requires MemAgent context. Will return instructions if called standalone.
    """
    # This is a placeholder - actual implementation happens in MemAgent._execute_tool_calls
    return "MEMORY_USER_INFO"


@tool(name="list_conversations", description="List recent conversations", category="memory")
def list_conversations(limit: int = 5) -> str:
    """
    List recent conversation sessions.

    Args:
        limit: Maximum number of conversations to list (default: 5)

    Returns:
        List of recent conversations

    Examples:
        list_conversations(3) -> "Last 3 conversations: ..."

    Note:
        This tool requires MemAgent context. Will return instructions if called standalone.
    """
    # This is a placeholder - actual implementation happens in MemAgent._execute_tool_calls
    return f"MEMORY_LIST_CONVERSATIONS:{limit}"


# ============================================================================
# Workspace Management Tools (v2.1.3+)
# ============================================================================


@tool(name="list_workspace_files", description="List files in tool workspace", category="utility")
def list_workspace_files(pattern: str = "*") -> str:
    """
    List files created by tools in the workspace.

    Args:
        pattern: File pattern to match (default: "*" for all files)

    Returns:
        List of workspace files with sizes
    """
    workspace = get_workspace()
    files = workspace.list_files(pattern=pattern)

    if not files:
        return "No files in workspace"

    result = f"📁 Workspace files ({len(files)}):\n"
    for f in files:
        size = f.stat().st_size
        result += f"  - {f.name} ({size} bytes)\n"

    return result


@tool(name="cleanup_workspace", description="Clean up tool workspace files", category="utility")
def cleanup_workspace() -> str:
    """
    Clean up all files in the tool workspace.

    Returns:
        Cleanup confirmation message
    """
    workspace = get_workspace()
    stats = workspace.get_stats()
    workspace.cleanup()

    return (
        f"🧹 Workspace cleaned: {stats['total_files']} files ({stats['total_size_mb']} MB) removed"
    )


@tool(name="workspace_stats", description="Get tool workspace statistics", category="utility")
def workspace_stats() -> str:
    """
    Get statistics about the tool workspace.

    Returns:
        Workspace statistics (files, size, location)
    """
    workspace = get_workspace()
    stats = workspace.get_stats()

    return (
        f"📊 Workspace Statistics:\n"
        f"  Files: {stats['total_files']}\n"
        f"  Size: {stats['total_size_mb']} MB\n"
        f"  Location: {stats['workspace_dir']}\n"
        f"  Session: {stats['current_session']}"
    )


# ============================================================================
# Export all tools
# ============================================================================

BUILTIN_TOOLS = [
    # Math
    calculate,
    # Text
    count_words,
    reverse_text,
    to_uppercase,
    to_lowercase,
    # File
    read_file,
    write_file,
    list_files,
    # Utility
    get_current_time,
    create_json,
    get_system_info,
    generate_random,
    # Memory (v2.0.0+)
    search_memory,
    get_user_info,
    list_conversations,
    # Workspace (v2.1.3+)
    list_workspace_files,
    cleanup_workspace,
    workspace_stats,
]
