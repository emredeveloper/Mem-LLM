"""
Example 14: Auto-Detect Backend
================================

Automatically detect and use available LLM service.

Quick Usage:
    agent = MemAgent(auto_detect_backend=True)
"""

from mem_llm import MemAgent

print("=" * 60)
print("Auto-Detect Backend")
print("=" * 60)

try:
    # Auto-detect available backend
    agent = MemAgent(
        auto_detect_backend=True,
        use_sql=False
    )
    
    info = agent.llm.get_info()
    print(f"\n✅ Detected: {info['backend']}")
    print(f"   Model: {info.get('model', 'Unknown')}\n")
    
    # Test conversation
    agent.set_user("demo")
    
    messages = [
        "Hello! My name is Demo User.",
        "I love Python programming.",
        "Do you remember my name and interests?"
    ]
    
    print("💬 Conversation:")
    for msg in messages:
        print(f"\nUser: {msg}")
        response = agent.chat(msg)
        print(f"AI: {response}")
    
except RuntimeError as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 No LLM service found.")
    print("   Start Ollama, LM Studio, or set GEMINI_API_KEY")

print("\n" + "=" * 60)
