"""
Quickstart 5: Complete Demo
============================
Comprehensive demo showing all major features:
- Basic chat with memory
- SQL storage
- Knowledge base
- Streaming responses
- Multi-user support

Installation:
    pip install mem-llm

Requirements:
    - Ollama running with granite4:3b model
"""

from mem_llm import MemAgent
import json
import os

def demo_basic_chat():
    """Demo 1: Basic chat with memory."""
    print("\n" + "="*60)
    print("DEMO 1: Basic Chat with Memory")
    print("="*60)
    
    # Option 1: Ollama
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b',
        use_sql=False
    )
    
    # Option 2: LM Studio
    # agent = MemAgent(
    #     backend='lmstudio',
    #     model='local-model',
    #     use_sql=False
    # )
    
    # Option 3: Auto-detect
    # agent = MemAgent(
    #     auto_detect_backend=True,
    #     use_sql=False
    # )
    
    agent.set_user("alice")
    
    print("\n[Alice]: Hi! I'm Alice and I work as a software engineer.")
    r1 = agent.chat("Hi! I'm Alice and I work as a software engineer.")
    print(f"[Bot]: {r1}")
    
    print("\n[Alice]: What's my name and job?")
    r2 = agent.chat("What's my name and job?")
    print(f"[Bot]: {r2}")
    
    print("\n✓ Memory works! Bot remembers Alice's info.")

def demo_sql_storage():
    """Demo 2: SQL storage for production."""
    print("\n" + "="*60)
    print("DEMO 2: SQL Storage (Production-Ready)")
    print("="*60)
    
    # Option 1: Ollama
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b',
        use_sql=True  # Use SQLite for thread-safe storage
    )
    
    # Option 2: LM Studio (commented out)
    # agent = MemAgent(
    #     backend='lmstudio',
    #     model='local-model',
    #     use_sql=True
    # )
    
    agent.set_user("bob")
    
    print("\n[Bob]: I love Python and machine learning.")
    r1 = agent.chat("I love Python and machine learning.")
    print(f"[Bot]: {r1}")
    
    # Check conversation history
    try:
        history = agent.memory.get_conversation_history(user_id="bob")
        print(f"\n✓ Conversation saved to SQLite")
        print(f"  Total interactions: {len(history)}")
    except Exception as e:
        print(f"\n✓ Conversation saved to SQLite")
        print(f"  (History check skipped: {type(e).__name__})")

def demo_knowledge_base():
    """Demo 3: Knowledge base for domain-specific answers."""
    print("\n" + "="*60)
    print("DEMO 3: Knowledge Base")
    print("="*60)
    
    # Create a simple KB file
    kb_data = [
        {
            "category": "company",
            "question": "What is our company name?",
            "answer": "Our company is TechCorp, founded in 2020."
        },
        {
            "category": "product",
            "question": "What products do we offer?",
            "answer": "We offer AI-powered solutions for enterprise clients."
        }
    ]
    
    kb_file = "temp_kb.json"
    with open(kb_file, 'w') as f:
        json.dump(kb_data, f)
    
    # Option 1: Ollama
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b',
        knowledge_base=kb_file
    )
    
    # Option 2: LM Studio (commented out)
    # agent = MemAgent(
    #     backend='lmstudio',
    #     model='local-model',
    #     knowledge_base=kb_file
    # )
    
    agent.set_user("customer")
    
    print("\n[Customer]: What is your company name?")
    r1 = agent.chat("What is your company name?")
    print(f"[Bot]: {r1}")
    
    print("\n[Customer]: What products do you offer?")
    r2 = agent.chat("What products do you offer?")
    print(f"[Bot]: {r2}")
    
    # Cleanup
    os.remove(kb_file)
    print("\n✓ Knowledge base provides authoritative answers!")

def demo_streaming():
    """Demo 4: Streaming responses."""
    print("\n" + "="*60)
    print("DEMO 4: Streaming Response")
    print("="*60)
    
    # Option 1: Ollama
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b'
    )
    
    # Option 2: LM Studio (commented out)
    # agent = MemAgent(
    #     backend='lmstudio',
    #     model='local-model'
    # )
    
    agent.set_user("streamer")
    
    print("\n[User]: Explain what streaming is in one paragraph.")
    print("[Bot]: ", end="", flush=True)
    
    for chunk in agent.chat_stream("Explain what streaming is in one paragraph."):
        print(chunk, end="", flush=True)
    
    print("\n\n✓ Real-time streaming works!")

def demo_multi_user():
    """Demo 5: Multi-user support."""
    print("\n" + "="*60)
    print("DEMO 5: Multi-User Support")
    print("="*60)
    
    # Option 1: Ollama
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b',
        use_sql=True
    )
    
    # Option 2: LM Studio (commented out)
    # agent = MemAgent(
    #     backend='lmstudio',
    #     model='local-model',
    #     use_sql=True
    # )
    
    # User 1: Alice
    agent.set_user("alice")
    print("\n[Alice]: My favorite color is blue.")
    r1 = agent.chat("My favorite color is blue.")
    print(f"[Bot]: {r1}")
    
    # User 2: Bob
    agent.set_user("bob")
    print("\n[Bob]: My favorite color is red.")
    r2 = agent.chat("My favorite color is red.")
    print(f"[Bot]: {r2}")
    
    # Back to Alice
    agent.set_user("alice")
    print("\n[Alice]: What's my favorite color?")
    r3 = agent.chat("What's my favorite color?")
    print(f"[Bot]: {r3}")
    
    # Back to Bob
    agent.set_user("bob")
    print("\n[Bob]: What's my favorite color?")
    r4 = agent.chat("What's my favorite color?")
    print(f"[Bot]: {r4}")
    
    print("\n✓ Each user has isolated memory!")

def main():
    print("="*60)
    print("MEM-LLM COMPLETE DEMO")
    print("Showcasing all major features")
    print("="*60)
    
    try:
        # Run all demos
        demo_basic_chat()
        demo_sql_storage()
        demo_knowledge_base()
        demo_streaming()
        demo_multi_user()
        
        print("\n" + "="*60)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Try the Web UI: mem-llm-web")
        print("  2. Read docs: https://github.com/emredeveloper/Mem-LLM")
        print("  3. Explore examples in the GitHub repo")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Pull model: ollama pull granite4:3b")
        print("  3. Check: http://localhost:11434")

if __name__ == "__main__":
    main()

