"""
Mem-LLM v2.1.0 - Async Tools Demo
Demonstrates async tool support with non-blocking I/O operations
"""

from mem_llm import MemAgent, tool
import asyncio

print("=" * 60)
print("Mem-LLM v2.1.0 - Async Tools Demo")
print("=" * 60)

# Create agent with tools enabled
# Option 1: Ollama
agent = MemAgent(
    backend='ollama',
    model='granite4:3b',
    enable_tools=True,
    use_sql=False
)

# Option 2: LM Studio
# agent = MemAgent(
#     backend='lmstudio',
#     model='local-model',
#     enable_tools=True,
#     use_sql=False
# )

# Option 3: Auto-detect
# agent = MemAgent(
#     auto_detect_backend=True,
#     enable_tools=True,
#     use_sql=False
# )

agent.set_user("async_demo_user")

print("\n1️⃣  Built-in Async HTTP Tool")
print("-" * 60)
response = agent.chat("Use fetch_url to get data from https://httpbin.org/json")
print(f"Response: {response}\n")

print("\n2️⃣  Built-in Async POST Tool")
print("-" * 60)
response = agent.chat("""
Use post_json to send this data to https://httpbin.org/post:
{"name": "Alice", "age": 30}
""")
print(f"Response: {response}\n")

print("\n3️⃣  Custom Async Tool")
print("-" * 60)

@tool(
    name="async_calculate",
    description="Performs async calculation (simulates complex operation)"
)
async def async_calculate(expression: str) -> str:
    """Async calculator that simulates complex calculations"""
    await asyncio.sleep(0.5)  # Simulate async operation
    try:
        result = eval(expression)
        return f"Async calculation result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Register custom async tool
agent.tool_registry.register_tool(async_calculate)

response = agent.chat("Use async_calculate to compute (100 * 25) + 500")
print(f"Response: {response}\n")

print("\n4️⃣  Multiple Async Operations")
print("-" * 60)

@tool(
    name="fetch_multiple",
    description="Fetches data from multiple URLs in parallel"
)
async def fetch_multiple(urls: str) -> str:
    """Fetch multiple URLs concurrently"""
    import aiohttp
    url_list = [u.strip() for u in urls.split(",")]
    
    async def fetch_one(session, url):
        try:
            async with session.get(url, timeout=5) as resp:
                return f"{url}: {resp.status}"
        except Exception as e:
            return f"{url}: Error - {str(e)}"
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in url_list]
        results = await asyncio.gather(*tasks)
        return "\n".join(results)

agent.tool_registry.register_tool(fetch_multiple)

response = agent.chat("""
Use fetch_multiple to check these URLs:
https://httpbin.org/status/200,https://httpbin.org/status/404
""")
print(f"Response: {response}\n")

print("\n5️⃣  Async File Operations")
print("-" * 60)
response = agent.chat("""
Use write_file_async to create test_async.txt with content:
This file was created using async I/O!
""")
print(f"Response: {response}\n")

response = agent.chat("Use read_file_async to read test_async.txt")
print(f"Response: {response}\n")

print("\n6️⃣  Async Sleep Tool")
print("-" * 60)
response = agent.chat("Use async_sleep to wait for 2 seconds, then tell me you're done")
print(f"Response: {response}\n")

print("\n✅ Async Tools Demo Completed!")
print("=" * 60)
print("\n📊 Key Features Demonstrated:")
print("  - Built-in async HTTP tools (fetch_url, post_json)")
print("  - Custom async tools with @tool decorator")
print("  - Async file operations (read/write)")
print("  - Parallel async operations")
print("  - Async sleep/delays")
print("\n💡 Benefits:")
print("  - Non-blocking I/O operations")
print("  - Better performance for network requests")
print("  - Concurrent operations support")
print("  - Automatic async/sync detection")

