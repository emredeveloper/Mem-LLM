"""
Quickstart 2: Streaming Response
=================================
Real-time ChatGPT-style streaming response.

Installation:
    pip install mem-llm

Requirements:
    - Ollama running on localhost:11434
"""

from mem_llm import MemAgent
import sys

def main():
    print("="*60)
    print("Mem-LLM Quickstart 2: Streaming Response")
    print("="*60)
    
    # Create agent
    agent = MemAgent(
        backend='ollama',
        model='granite4:3b'
    )
    
    agent.set_user("streaming_user")
    
    # Non-streaming chat
    print("\n1. Regular (Non-Streaming) Response:")
    print("-"*60)
    print("[User]: Tell me a short story about AI.")
    response = agent.chat("Tell me a short story about AI.")
    print(f"[Bot]: {response}\n")
    
    # Streaming chat (ChatGPT-style)
    print("\n2. Streaming Response (Real-time):")
    print("-"*60)
    print("[User]: What are the benefits of streaming responses?")
    print("[Bot]: ", end="", flush=True)
    
    for chunk in agent.chat_stream("What are the benefits of streaming responses?"):
        print(chunk, end="", flush=True)
        sys.stdout.flush()
    
    print("\n")
    print("="*60)
    print("✓ Streaming works! Notice the typing effect.")
    print("="*60)

if __name__ == "__main__":
    main()

