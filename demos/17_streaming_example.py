"""
Streaming Response Example
===========================

This example demonstrates the streaming response feature in Mem-LLM.
Streaming provides real-time response generation, similar to ChatGPT's typing effect.

Benefits:
- Better user experience for long responses
- Real-time feedback
- Lower perceived latency
- Professional chat interface feeling

Author: Cihat Emre Karataş
Version: 1.3.3
"""

import sys
import time
from mem_llm import MemAgent

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def streaming_example_basic():
    """Basic streaming response example"""
    print_header("1. Basic Streaming Response")
    
    # Create agent
    agent = MemAgent(
        model="granite4:tiny-h",
        backend="ollama",
        use_sql=False  # Use simple JSON memory for this example
    )
    
    # Set user
    agent.set_user("alice")
    
    # Get streaming response
    print("👤 User: What is Python and why is it popular?")
    print("🤖 Agent: ", end='', flush=True)
    
    # Stream the response
    for chunk in agent.chat_stream("What is Python and why is it popular?"):
        print(chunk, end='', flush=True)
        time.sleep(0.01)  # Optional: slight delay for visual effect
    
    print("\n")  # New line after response

def streaming_example_multi_message():
    """Multiple streaming messages with memory"""
    print_header("2. Streaming with Memory")
    
    agent = MemAgent(
        model="granite4:3b",
        backend="ollama",
        use_sql=False
    )
    
    agent.set_user("bob")
    
    # First message
    print("👤 User: My name is Bob and I'm learning Python.")
    print("🤖 Agent: ", end='', flush=True)
    
    for chunk in agent.chat_stream("My name is Bob and I'm learning Python."):
        print(chunk, end='', flush=True)
        time.sleep(0.01)
    
    print("\n")
    
    # Second message (agent should remember)
    print("\n👤 User: What was my name?")
    print("🤖 Agent: ", end='', flush=True)
    
    for chunk in agent.chat_stream("What was my name?"):
        print(chunk, end='', flush=True)
        time.sleep(0.01)
    
    print("\n")

def streaming_example_with_kb():
    """Streaming with knowledge base"""
    print_header("3. Streaming with Knowledge Base")
    
    agent = MemAgent(
        model="granite4:3b",
        backend="ollama",
        use_sql=True,  # SQL required for KB
        load_knowledge_base=True
    )
    
    # Add some knowledge
    agent.add_kb_entry(
        category="Python",
        question="Python'da liste (list) nedir?",
        answer="Liste, sıralı ve değiştirilebilir bir veri yapısıdır. Köşeli parantez [] ile tanımlanır. Örnek: my_list = [1, 2, 3, 'a', 'b']"
    )
    
    agent.add_kb_entry(
        category="Python",
        question="Python'da dictionary (sözlük) nedir?",
        answer="Dictionary, anahtar-değer çiftleri içeren bir veri yapısıdır. Süslü parantez {} ile tanımlanır. Örnek: my_dict = {'name': 'Ali', 'age': 25}"
    )
    
    agent.set_user("charlie")
    
    # Ask question (should use KB)
    print("👤 User: Python'da liste nedir ve nasıl kullanılır?")
    print("🤖 Agent: ", end='', flush=True)
    
    for chunk in agent.chat_stream("Python'da liste nedir ve nasıl kullanılır?"):
        print(chunk, end='', flush=True)
        time.sleep(0.01)
    
    print("\n")

def streaming_example_multi_backend():
    """Streaming with different backends"""
    print_header("4. Streaming with Different Backends")
    
    backends = [
        ("ollama", "granite4:3b", "http://localhost:11434"),
        ("lmstudio", "qwen/qwen3-vl-4b", "http://localhost:1234"),
    ]
    
    question = "Hello! Who are you?"
    
    for backend, model, base_url in backends:
        try:
            print(f"\n📡 Testing {backend.upper()} backend...")
            print(f"   Model: {model}")
            print(f"   URL: {base_url}\n")
            
            agent = MemAgent(
                model=model,
                backend=backend,
                base_url=base_url,
                use_sql=False,
                check_connection=False  # Skip connection check for speed
            )
            
            # Check if backend is available
            if not agent.llm.check_connection():
                print(f"   ⚠️  {backend} is not available. Skipping...\n")
                continue
            
            agent.set_user("test_user")
            
            print(f"👤 User: {question}")
            print("🤖 Agent: ", end='', flush=True)
            
            for chunk in agent.chat_stream(question):
                print(chunk, end='', flush=True)
                time.sleep(0.01)
            
            print("\n")
            
        except Exception as e:
            print(f"   ❌ Error with {backend}: {e}\n")

def streaming_example_performance():
    """Compare streaming vs non-streaming performance"""
    print_header("5. Performance Comparison")
    
    agent = MemAgent(
        model="granite4:tiny-h",
        backend="ollama",
        use_sql=False
    )
    
    agent.set_user("perf_test")
    question = "Python'ın avantajları nelerdir?"
    
    # Non-streaming
    print("🔄 Non-Streaming Mode:")
    print(f"👤 User: {question}")
    
    start_time = time.time()
    response = agent.chat(question)
    end_time = time.time()
    
    print(f"🤖 Agent: {response}")
    print(f"⏱️  Total time: {(end_time - start_time):.2f} seconds")
    print(f"⏱️  Time to first token: {(end_time - start_time):.2f} seconds")
    
    print("\n" + "-"*60 + "\n")
    
    # Streaming
    print("⚡ Streaming Mode:")
    print(f"👤 User: {question}")
    print("🤖 Agent: ", end='', flush=True)
    
    start_time = time.time()
    first_token_time = None
    
    for i, chunk in enumerate(agent.chat_stream(question)):
        if i == 0 and first_token_time is None:
            first_token_time = time.time()
        print(chunk, end='', flush=True)
    
    end_time = time.time()
    
    print("\n")
    print(f"⏱️  Total time: {(end_time - start_time):.2f} seconds")
    if first_token_time:
        print(f"⏱️  Time to first token: {(first_token_time - start_time):.2f} seconds")
        print(f"✨ First token was {((end_time - start_time) / (first_token_time - start_time)):.1f}x faster!")

def main():
    """Run all streaming examples"""
    print("\n" + "🌊 "*20)
    print("      MEM-LLM STREAMING RESPONSE DEMO")
    print("🌊 "*20)
    
    try:
        # Run examples
        streaming_example_basic()
        streaming_example_multi_message()
        streaming_example_with_kb()
        streaming_example_multi_backend()
        streaming_example_performance()
        
        print_header("✅ All Examples Completed!")
        print("Streaming provides a much better user experience!")
        print("Use agent.chat_stream() instead of agent.chat() for real-time responses.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

