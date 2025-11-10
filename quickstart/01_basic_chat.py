"""
Quickstart 1: Basic Chat
=========================
Simple chat example with memory using Ollama backend.

Installation:
    pip install mem-llm

Requirements:
    - Ollama running on localhost:11434
    - A model pulled (e.g., ollama pull granite4:3b)
"""

from mem_llm import MemAgent

def main():
    print("="*60)
    print("Mem-LLM Quickstart 1: Basic Chat")
    print("="*60)
    
    # Create agent with Ollama backend
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b',
        use_sql=False  # Use simple JSON storage
    )
    
    # Set user
    agent.set_user("quickstart_user")
    
    # Chat 1: Introduce yourself
    print("\n[User]: Hi! My name is Alice and I love Python programming.")
    response1 = agent.chat("Hi! My name is Alice and I love Python programming.")
    print(f"[Bot]: {response1}\n")
    
    # Chat 2: Ask about name (tests memory)
    print("[User]: What's my name?")
    response2 = agent.chat("What's my name?")
    print(f"[Bot]: {response2}\n")
    
    # Chat 3: Ask about interest (tests memory)
    print("[User]: What do I love?")
    response3 = agent.chat("What do I love?")
    print(f"[Bot]: {response3}\n")
    
    print("="*60)
    print("✓ Success! Memory is working correctly.")
    print("="*60)

if __name__ == "__main__":
    main()

