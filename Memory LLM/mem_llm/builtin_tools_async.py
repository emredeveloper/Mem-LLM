"""
Built-in Async Tools (v2.1.0+)
==============================

Async versions of common tools for I/O-bound operations.

Author: C. Emre Karataş
Version: 2.1.1
"""

import asyncio
from typing import Any, Dict

import aiohttp

from .tool_system import tool

# ============================================================================
# Async Web & API Tools
# ============================================================================


@tool(
    name="fetch_url",
    description="Fetch content from a URL asynchronously",
    category="web",
    pattern={"url": r"^https?://"},
    max_length={"url": 2048},
)
async def fetch_url(url: str, timeout: int = 10) -> str:
    """
    Fetch content from a URL.

    Args:
        url: The URL to fetch (must start with http:// or https://)
        timeout: Request timeout in seconds (default: 10)

    Returns:
        Response text or error message
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    text = await response.text()
                    return text[:5000]  # Limit to 5000 chars
                return f"HTTP {response.status}: {response.reason}"
    except asyncio.TimeoutError:
        return f"Request timed out after {timeout}s"
    except Exception as e:
        return f"Error fetching URL: {e}"


@tool(
    name="post_json",
    description="Post JSON data to an API endpoint",
    category="web",
    pattern={"url": r"^https?://"},
)
async def post_json(url: str, data: Dict[str, Any], timeout: int = 10) -> str:
    """
    Post JSON data to an API endpoint.

    Args:
        url: The API endpoint URL
        data: JSON data to post
        timeout: Request timeout in seconds

    Returns:
        Response text or error message
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, timeout=timeout) as response:
                text = await response.text()
                return f"Status {response.status}: {text[:500]}"
    except Exception as e:
        return f"Error posting data: {e}"


# ============================================================================
# Async File Operations
# ============================================================================


@tool(
    name="read_file_async",
    description="Read a file asynchronously",
    category="file",
    max_length={"filepath": 260},
)
async def read_file_async(filepath: str) -> str:
    """
    Read a file asynchronously.

    Args:
        filepath: Path to the file

    Returns:
        File contents or error message
    """
    try:
        loop = asyncio.get_event_loop()
        with open(filepath, "r", encoding="utf-8") as f:
            content = await loop.run_in_executor(None, f.read)
        return content
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading file: {e}"


@tool(name="write_file_async", description="Write to a file asynchronously", category="file")
async def write_file_async(filepath: str, content: str) -> str:
    """
    Write to a file asynchronously.

    Args:
        filepath: Path to the file
        content: Content to write

    Returns:
        Success message or error
    """
    try:
        loop = asyncio.get_event_loop()
        with open(filepath, "w", encoding="utf-8") as f:
            await loop.run_in_executor(None, f.write, content)
        return f"Successfully wrote {len(content)} chars to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"


# ============================================================================
# Async Utility Tools
# ============================================================================


@tool(
    name="sleep",
    description="Asynchronously wait for specified seconds",
    category="utility",
    min_value={"seconds": 0},
    max_value={"seconds": 60},
)
async def async_sleep(seconds: float) -> str:
    """
    Wait asynchronously for specified seconds.

    Args:
        seconds: Number of seconds to wait (0-60)

    Returns:
        Completion message
    """
    await asyncio.sleep(seconds)
    return f"Waited for {seconds} seconds"


# ============================================================================
# Export Async Tools
# ============================================================================

ASYNC_BUILTIN_TOOLS = [
    fetch_url,
    post_json,
    read_file_async,
    write_file_async,
    async_sleep,
]

# Backward compatibility
ASYNC_TOOLS = ASYNC_BUILTIN_TOOLS
