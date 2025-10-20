"""
Example 2: Basic Memory
=======================
Shows how the agent remembers information across conversations.
"""

from mem_llm import MemAgent

def main():
    # Create agent
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)
    
    # Check if Ollama is running
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Please start Ollama first: ollama serve")
        return
    
    # Set user
    agent.set_user("john")
    
    print("=== Conversation 1: Share Information ===")
    response = agent.chat("My name is John and I love pizza")
    print(f"Bot: {response}\n")
    
    print("=== Conversation 2: Test Memory ===")
    response = agent.chat("What's my name?")
    print(f"Bot: {response}\n")
    
    print("=== Conversation 3: Test Memory Again ===")
    response = agent.chat("What food do I like?")
    print(f"Bot: {response}\n")
    
    # Show saved profile
    profile = agent.get_user_profile()
    print(f"=== Saved Profile ===")
    print(f"Name: {profile.get('name', 'N/A')}")
    print(f"Favorite Food: {profile.get('favorite_food', 'N/A')}")

if __name__ == "__main__":
    main()
