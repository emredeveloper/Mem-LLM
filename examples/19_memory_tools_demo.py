"""
Example 19: Memory-Aware Tools Demo (v2.0.0+)
==============================================

Demonstrates how agents can use tools to access their own memory!

New in v2.0.0:
- search_memory: Search conversation history
- get_user_info: Get current user profile
- list_conversations: List recent conversations

This creates a truly self-aware agent that can:
- Remember past conversations
- Search its own memory
- Provide context from history
"""

import sys
from pathlib import Path

# Add parent directory to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent / "Memory LLM"))

from mem_llm import MemAgent

def main():
    print("=" * 70)
    print("🧠 Memory-Aware Tools Demo (v2.0.0)")
    print("=" * 70)
    print()
    
    try:
        # Initialize agent with tools enabled
        agent = MemAgent(
            backend='ollama',
            model="granite4:3b",
            enable_tools=True  # Enables all built-in tools including memory tools
        )
        agent.set_user("memory_test_user")
        print("✅ Agent initialized with memory-aware tools")
        print()
        
        # --- Step 1: Have some conversations to build memory ---
        print("=" * 70)
        print("STEP 1: Building Conversation History")
        print("=" * 70)
        print()
        
        conversations = [
            "My name is Alice and I'm a Python developer",
            "I love working with AI and machine learning",
            "My favorite frameworks are FastAPI and PyTorch",
            "I'm currently building a chatbot application",
        ]
        
        for msg in conversations:
            print(f"👤 User: {msg}")
            response = agent.chat(msg)
            print(f"🤖 Bot: {response[:100]}...")
            print()
        
        # --- Step 2: Use memory tools to access history ---
        print("=" * 70)
        print("STEP 2: Accessing Memory with Tools")
        print("=" * 70)
        print()
        
        # Test 1: Get user info
        print("📊 Test: Get User Info")
        print("👤 User: What's my user info?")
        response = agent.chat("What's my user info?")
        print(f"🤖 Bot: {response}")
        print()
        
        # Test 2: List conversations
        print("📝 Test: List Conversations")
        print("👤 User: Show me my last 3 conversations")
        response = agent.chat("Show me my last 3 conversations")
        print(f"🤖 Bot: {response}")
        print()
        
        # Test 3: Search memory
        print("🔍 Test: Search Memory")
        print("👤 User: Search my memory for 'Python'")
        response = agent.chat("Search my memory for 'Python'")
        print(f"🤖 Bot: {response}")
        print()
        
        # Test 4: Combined query
        print("🔗 Test: Combined Memory Query")
        print("👤 User: What did I say about frameworks?")
        response = agent.chat("What did I say about frameworks?")
        print(f"🤖 Bot: {response}")
        print()
        
        # --- Step 3: Tool chaining with memory ---
        print("=" * 70)
        print("STEP 3: Tool Chaining with Memory")
        print("=" * 70)
        print()
        
        print("⛓️  Test: Memory + Calculation")
        print("👤 User: Count how many conversations I had, then multiply by 10")
        response = agent.chat("Count how many conversations I had, then multiply by 10")
        print(f"🤖 Bot: {response}")
        print()
        
        print("⛓️  Test: Memory + Text Processing")
        print("👤 User: Search for 'AI' in my memory and count the words in the results")
        response = agent.chat("Search for 'AI' in my memory and count the words in the results")
        print(f"🤖 Bot: {response}")
        print()
        
        # --- Summary ---
        print("=" * 70)
        print("✅ MEMORY TOOLS DEMO COMPLETED!")
        print("=" * 70)
        print()
        print("🎯 Key Achievements:")
        print("  ✅ Agent can access its own conversation history")
        print("  ✅ Agent can search past conversations")
        print("  ✅ Agent can get user profile information")
        print("  ✅ Agent can chain memory tools with other tools")
        print("  ✅ Creates truly self-aware AI agents!")
        print()
        print("💡 Use Cases:")
        print("  - Personal AI assistants that remember everything")
        print("  - Context-aware chatbots")
        print("  - Knowledge management systems")
        print("  - Self-documenting agents")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("⚠️  Make sure:")
        print("  1. Ollama is running: ollama serve")
        print("  2. Model is available: ollama pull granite4:3b")
        print()

if __name__ == "__main__":
    main()

