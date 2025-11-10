"""
Advanced Example 2: Async Tools
================================
Asynchronous tools - Non-blocking I/O operations
"""

from mem_llm import MemAgent, tool
import asyncio

agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    enable_tools=True,
    use_sql=False
)
agent.set_user("async_user")

# ============================================================================
# Built-in Async Tools
# ============================================================================
print("⚡ Built-in Async Tools:")
print("-" * 50)

# Sleep (non-blocking)
print("\n1️⃣  Async Sleep:")
response = agent.chat("Sleep for 1 second")
print(f"  {response[:80]}...")

# Async file write
print("\n2️⃣  Async File Write:")
response = agent.chat("Write 'Async content!' to file 'async.txt' asynchronously")
print(f"  {response[:80]}...")

# ============================================================================
# Custom Async Tool
# ============================================================================
print("\n\n🎨 Custom Async Tool:")
print("-" * 50)

@tool(name="async_counter", description="Count asynchronously")
async def async_counter(max_count: int) -> str:
    """Count from 1 to max_count with delay"""
    result = []
    for i in range(1, max_count + 1):
        await asyncio.sleep(0.1)
        result.append(str(i))
    return f"Counted: {', '.join(result)}"

agent.tool_registry.register_tool(async_counter)

print("\n3️⃣  Custom Async Counter:")
response = agent.chat("Count to 5 asynchronously")
print(f"  {response[:80]}...")

print("\n✅ Async tools demo complete!")
