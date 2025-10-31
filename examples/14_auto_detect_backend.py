"""
Example 14: Auto-Detect Backend
================================
Automatically detect and use available LLM service.
"""

from mem_llm import MemAgent

print("\n" + "="*50)
print("AUTO-DETECT BACKEND")
print("="*50 + "\n")

try:
    # Auto-detect available backend
    agent = MemAgent(
        auto_detect_backend=True,
        use_sql=False
    )
    
    info = agent.llm.get_info()
    print(f"Detected: {info['backend']}")
    print(f"Model: {info.get('model', 'Unknown')}\n")
    
    # Test conversation
    agent.set_user("demo")
    
    messages = [
        "Hello! My name is Demo User.",
        "I love Python programming.",
        "Do you remember my name and interests?"
    ]
    
    for msg in messages:
        print(f"User: {msg}")
        response = agent.chat(msg)
        print(f"AI: {response}\n")
    
except RuntimeError as e:
    print(f"Error: {e}")
    print("\nNo LLM service found.")
    print("Start Ollama, LM Studio, or set GEMINI_API_KEY")

print("="*50 + "\n")
