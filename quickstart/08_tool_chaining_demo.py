"""
Mem-LLM v2.1.0 - Tool Chaining Demo
Demonstrates how LLM can chain multiple tools together for complex tasks
"""

from mem_llm import MemAgent, tool
import json

print("=" * 60)
print("Mem-LLM v2.1.0 - Tool Chaining Demo")
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

agent.set_user("chaining_demo_user")

print("\n1️⃣  Simple Math Chain")
print("-" * 60)
print("Task: Calculate (10 + 20) * 3, then get uppercase of result")

response = agent.chat("""
First calculate (10 + 20) * 3,
then convert the result to uppercase text
""")
print(f"Response: {response}\n")

print("\n2️⃣  File Operations Chain")
print("-" * 60)
print("Task: Write file, read it back, count words, then report")

response = agent.chat("""
1. Write a file 'test_chain.txt' with content: 'Hello World Python Programming'
2. Read the file back
3. Count the words in it
4. Tell me the word count
""")
print(f"Response: {response}\n")

print("\n3️⃣  Data Processing Chain")
print("-" * 60)

@tool(
    name="generate_data",
    description="Generates sample data in JSON format"
)
def generate_data(count: int) -> str:
    """Generate sample user data"""
    data = [
        {"id": i, "name": f"User{i}", "score": i * 10}
        for i in range(1, count + 1)
    ]
    return json.dumps(data, indent=2)

@tool(
    name="filter_data",
    description="Filters data based on condition"
)
def filter_data(json_data: str, min_score: int) -> str:
    """Filter data by minimum score"""
    try:
        data = json.loads(json_data)
        filtered = [item for item in data if item.get('score', 0) >= min_score]
        return json.dumps(filtered, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@tool(
    name="summarize_data",
    description="Summarizes data statistics"
)
def summarize_data(json_data: str) -> str:
    """Get data statistics"""
    try:
        data = json.loads(json_data)
        count = len(data)
        total_score = sum(item.get('score', 0) for item in data)
        avg_score = total_score / count if count > 0 else 0
        return f"Count: {count}, Total Score: {total_score}, Average: {avg_score:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

# Register custom tools
agent.tool_registry.register_tool(generate_data)
agent.tool_registry.register_tool(filter_data)
agent.tool_registry.register_tool(summarize_data)

response = agent.chat("""
1. Use generate_data to create 5 user records
2. Use filter_data to keep only users with score >= 30
3. Use summarize_data to get statistics
4. Tell me the results
""")
print(f"Response: {response}\n")

print("\n4️⃣  Memory + Tools Chain")
print("-" * 60)
print("Task: Store info, search memory, then use calculation")

# First, store some information
agent.chat("I bought 5 apples for $10 total")
agent.chat("I bought 3 oranges for $6 total")

response = agent.chat("""
1. Search my memory for fruit purchases
2. Calculate the average price per fruit
3. Tell me which fruit is more expensive
""")
print(f"Response: {response}\n")

print("\n5️⃣  Complex Multi-Step Chain")
print("-" * 60)

@tool(
    name="analyze_text",
    description="Analyzes text and returns statistics"
)
def analyze_text(text: str) -> str:
    """Analyze text statistics"""
    words = text.split()
    chars = len(text)
    unique_words = len(set(words))
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    return json.dumps({
        "total_words": len(words),
        "total_chars": chars,
        "unique_words": unique_words,
        "avg_word_length": round(avg_word_len, 2)
    }, indent=2)

agent.tool_registry.register_tool(analyze_text)

response = agent.chat("""
Do this step by step:
1. Write a file 'story.txt' with: 'The quick brown fox jumps over the lazy dog'
2. Read the file
3. Use analyze_text on the content
4. Use count_words to verify word count
5. Convert the entire text to uppercase
6. Tell me all the results
""")
print(f"Response: {response}\n")

print("\n6️⃣  Conditional Tool Chaining")
print("-" * 60)

@tool(
    name="check_number",
    description="Checks if number is positive, negative, or zero"
)
def check_number(num: float) -> str:
    """Check number sign"""
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"

agent.tool_registry.register_tool(check_number)

response = agent.chat("""
1. Calculate: (5 * 3) - 20
2. Use check_number on the result
3. If positive, multiply by 2; if negative, reverse_text the result
4. Tell me the final answer
""")
print(f"Response: {response}\n")

print("\n7️⃣  Async + Sync Tool Chain")
print("-" * 60)

response = agent.chat("""
1. Use fetch_url to get data from https://httpbin.org/json
2. Save the response to file 'api_data.txt' using write_file
3. Read it back with read_file
4. Count how many words are in the response
5. Tell me the word count
""")
print(f"Response: {response}\n")

print("\n✅ Tool Chaining Demo Completed!")
print("=" * 60)
print("\n📊 Chaining Patterns Demonstrated:")
print("  1. Simple sequential chains (A → B → C)")
print("  2. File operation chains (write → read → process)")
print("  3. Data processing pipelines (generate → filter → summarize)")
print("  4. Memory-aware chains (remember → search → calculate)")
print("  5. Multi-step complex workflows (6+ steps)")
print("  6. Conditional chains (if-then logic)")
print("  7. Mixed async/sync chains")
print("\n💡 Benefits:")
print("  - LLM automatically determines tool order")
print("  - No manual workflow coding needed")
print("  - Handles complex multi-step tasks")
print("  - Passes results between tools automatically")

