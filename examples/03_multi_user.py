"""
Example 3: Multiple Users
=========================
Shows how different users have separate memories.
"""

from mem_llm import MemAgent

def main():
    agent = MemAgent()
    
    # Check setup
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Please start Ollama: ollama serve")
        return
    
    # === User 1: Alice ===
    print("=" * 60)
    print("USER 1: Alice")
    print("=" * 60)
    
    agent.set_user("alice")
    
    print("Alice: I love cats and reading books")
    response = agent.chat("I love cats and reading books")
    print(f"Bot: {response}\n")
    
    # === User 2: Bob ===
    print("=" * 60)
    print("USER 2: Bob")
    print("=" * 60)
    
    agent.set_user("bob")
    
    print("Bob: I'm a software engineer who enjoys hiking")
    response = agent.chat("I'm a software engineer who enjoys hiking")
    print(f"Bot: {response}\n")
    
    # === Back to Alice ===
    print("=" * 60)
    print("BACK TO USER 1: Alice")
    print("=" * 60)
    
    agent.set_user("alice")
    
    print("Alice: What do you know about me?")
    response = agent.chat("What do you know about me?")
    print(f"Bot: {response}\n")
    
    # === Back to Bob ===
    print("=" * 60)
    print("BACK TO USER 2: Bob")
    print("=" * 60)
    
    agent.set_user("bob")
    
    print("Bob: What's my job?")
    response = agent.chat("What's my job?")
    print(f"Bot: {response}\n")
    
    print("=" * 60)
    print("✅ Each user has completely separate memory!")
    print("=" * 60)

if __name__ == "__main__":
    main()
