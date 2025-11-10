"""
Example 18: Function Calling / Tools (v2.0.0)
==============================================

NEW MAJOR FEATURE: Function calling allows the agent to use external tools!

The agent can now:
- Call functions to perform actions
- Use built-in tools (math, file ops, text processing)
- Register custom tools
- Chain multiple tool calls

Quick Usage:
    agent = MemAgent(enable_tools=True)
    agent.chat("Calculate 25 * 4 + 10")  # Agent will use calculator tool!
"""

import sys
from pathlib import Path

# Add parent directory to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent / "Memory LLM"))

from mem_llm import MemAgent, tool

print("="*70)
print("Function Calling Demo (v2.0.0)")
print("="*70)

# ============================================================================
# Demo 1: Built-in Tools
# ============================================================================

print("\n" + "="*70)
print("DEMO 1: Built-in Tools")
print("="*70)

agent = MemAgent(
    backend='ollama',
    model='granite4:3b',
    enable_tools=True,  # 🔥 Enable tool system
    use_sql=False
)

agent.set_user("demo_user")

# Test calculator
print("\n📊 Testing Calculator:")
print("User: Calculate (25 * 4) + 10")
response = agent.chat("Calculate (25 * 4) + 10")
print(f"Bot: {response}")

# Test text processing
print("\n📝 Testing Text Processing:")
print("User: Count the words in 'Hello world from AI agent'")
response = agent.chat("Count the words in 'Hello world from AI agent'")
print(f"Bot: {response}")

# Test current time
print("\n🕐 Testing Time:")
print("User: What is the current time?")
response = agent.chat("What is the current time?")
print(f"Bot: {response}")

# ============================================================================
# Demo 2: Custom Tools
# ============================================================================

print("\n" + "="*70)
print("DEMO 2: Custom Tools")
print("="*70)

# Define custom tools
@tool(name="get_weather", description="Get weather for a city", category="utility")
def get_weather(city: str) -> str:
    """Get weather information for a city"""
    # Simulated weather data
    weather_data = {
        "New York": "Sunny, 22°C",
        "London": "Rainy, 15°C",
        "Tokyo": "Cloudy, 18°C",
        "Paris": "Windy, 20°C"
    }
    return weather_data.get(city, f"Weather data not available for {city}")


@tool(name="translate", description="Translate text to Spanish", category="text")
def translate_to_spanish(text: str) -> str:
    """Simple translation (demo only)"""
    translations = {
        "hello": "hola",
        "goodbye": "adiós",
        "thank you": "gracias",
        "good morning": "buenos días"
    }
    return translations.get(text.lower(), f"Translation not available for '{text}'")


# Create agent with custom tools
agent_custom = MemAgent(
    backend='ollama',
    model='granite4:3b',
    enable_tools=True,
    tools=[get_weather, translate_to_turkish],  # 🔥 Add custom tools
    use_sql=False
)

agent_custom.set_user("demo_user_custom")

print("\n🌤️  Testing Custom Weather Tool:")
print("User: What's the weather in Tokyo?")
response = agent_custom.chat("What's the weather in Tokyo?")
print(f"Bot: {response}")

print("\n🌍 Testing Custom Translation Tool:")
print("User: Translate 'hello' to Turkish")
response = agent_custom.chat("Translate 'hello' to Turkish")
print(f"Bot: {response}")

# ============================================================================
# Demo 3: Complex Multi-Tool Usage
# ============================================================================

print("\n" + "="*70)
print("DEMO 3: Complex Multi-Tool Usage")
print("="*70)

# Agent can chain multiple tools
print("\n🔗 Testing Tool Chaining:")
print("User: Calculate 100 divided by 4, then convert the result to uppercase text")
response = agent.chat("Calculate 100 divided by 4, then convert the result to uppercase text")
print(f"Bot: {response}")

# ============================================================================
# Demo 4: File Operations
# ============================================================================

print("\n" + "="*70)
print("DEMO 4: File Operations")
print("="*70)

print("\n📁 Testing File Tools:")
print("User: Create a file called 'test_output.txt' with content 'Hello from AI agent!'")
response = agent.chat("Create a file called 'test_output.txt' with content 'Hello from AI agent!'")
print(f"Bot: {response}")

print("\nUser: Read the file 'test_output.txt'")
response = agent.chat("Read the file 'test_output.txt'")
print(f"Bot: {response}")

# Clean up
import os
if os.path.exists("test_output.txt"):
    os.remove("test_output.txt")
    print("\n🗑️  Cleaned up test file")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "="*70)
print("✅ FUNCTION CALLING DEMO COMPLETED!")
print("="*70)

print("\n📚 Available Built-in Tools:")
print("  Math: calculate")
print("  Text: count_words, reverse_text, to_uppercase, to_lowercase")
print("  File: read_file, write_file, list_files")
print("  Utility: get_current_time, create_json")

print("\n🎯 Key Features:")
print("  ✅ Built-in tools (10+ tools)")
print("  ✅ Custom tool registration")
print("  ✅ Automatic tool detection")
print("  ✅ Multi-tool chaining")
print("  ✅ Error handling")
print("  ✅ Type hints support")

print("\n🚀 Next Steps:")
print("  1. Create your own custom tools with @tool decorator")
print("  2. Combine tools with memory and knowledge base")
print("  3. Build complex agent workflows")
print("  4. Explore tool categories and organization")

print("\n" + "="*70)

