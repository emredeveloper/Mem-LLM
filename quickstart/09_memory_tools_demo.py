"""
Mem-LLM v2.1.0 - Memory-Aware Tools Demo
Demonstrates unique memory-aware tools that let agents search their own history
"""

from mem_llm import MemAgent, tool
from datetime import datetime

print("=" * 60)
print("Mem-LLM v2.1.0 - Memory-Aware Tools Demo")
print("=" * 60)

# Create agent with tools enabled
# Option 1: Ollama
agent = MemAgent(
    backend='ollama',
    model='granite4:3b',
    enable_tools=True,
    use_sql=True  # Use SQL for better memory management
)

# Option 2: LM Studio
# agent = MemAgent(
#     backend='lmstudio',
#     model='local-model',
#     enable_tools=True,
#     use_sql=True
# )

# Option 3: Auto-detect
# agent = MemAgent(
#     auto_detect_backend=True,
#     enable_tools=True,
#     use_sql=True
# )

agent.set_user("memory_demo_user")

print("\n1️⃣  Building Conversation History")
print("-" * 60)
print("Creating some conversation history...\n")

conversations = [
    "My name is Alice and I'm a Python developer",
    "I work at TechCorp as a senior engineer",
    "My favorite programming languages are Python and Rust",
    "I have 5 years of experience in machine learning",
    "My current project is about natural language processing",
    "I love working with LLMs and AI agents",
    "My salary is $120,000 per year",
    "I live in San Francisco, California",
]

for msg in conversations:
    response = agent.chat(msg)
    print(f"User: {msg}")
    print(f"Agent: {response}\n")

print("\n2️⃣  Searching Memory with Keywords")
print("-" * 60)

response = agent.chat("Use search_memory to find everything about my job and work")
print(f"Response: {response}\n")

response = agent.chat("Search my memory for information about programming languages")
print(f"Response: {response}\n")

print("\n3️⃣  Getting User Profile Information")
print("-" * 60)

response = agent.chat("Use get_user_info to show me my complete profile")
print(f"Response: {response}\n")

print("\n4️⃣  Listing All Conversations")
print("-" * 60)

response = agent.chat("Use list_conversations to show me all my chat history")
print(f"Response: {response}\n")

print("\n5️⃣  Memory + Calculation Chain")
print("-" * 60)

agent.chat("I save 20% of my monthly income")

response = agent.chat("""
1. Search my memory for my salary
2. Calculate how much I save per month (20% of monthly salary)
3. Calculate my annual savings
4. Tell me the results
""")
print(f"Response: {response}\n")

print("\n6️⃣  Memory + Text Processing Chain")
print("-" * 60)

response = agent.chat("""
1. Search my memory for my favorite programming languages
2. Convert the language names to uppercase
3. Count how many languages I mentioned
4. Tell me the results
""")
print(f"Response: {response}\n")

print("\n7️⃣  Custom Memory-Aware Tool")
print("-" * 60)

@tool(
    name="analyze_interests",
    description="Analyzes user's interests from conversation history"
)
def analyze_interests(conversation_data: str) -> str:
    """Analyze user interests from conversation"""
    keywords = {
        'tech': ['python', 'rust', 'programming', 'machine learning', 'llm', 'ai'],
        'work': ['work', 'job', 'salary', 'engineer', 'project'],
        'location': ['san francisco', 'california', 'live'],
    }
    
    conversation_lower = conversation_data.lower()
    results = {}
    
    for category, words in keywords.items():
        matches = [word for word in words if word in conversation_lower]
        results[category] = len(matches)
    
    return f"Interest Analysis:\n" + \
           f"  Technology: {results['tech']} mentions\n" + \
           f"  Work-related: {results['work']} mentions\n" + \
           f"  Location: {results['location']} mentions"

agent.tool_registry.register_tool(analyze_interests)

response = agent.chat("""
1. Use list_conversations to get all my conversations
2. Use analyze_interests on that data
3. Tell me what my main interests are
""")
print(f"Response: {response}\n")

print("\n8️⃣  Multi-User Memory Search")
print("-" * 60)

# Create another user's conversation
agent.set_user("bob")
agent.chat("My name is Bob and I'm a designer")
agent.chat("I work with Figma and Adobe XD")
agent.chat("My favorite color is blue")

# Switch back to Alice
agent.set_user("memory_demo_user")

response = agent.chat("""
Search my memory to remind me:
- What's my name?
- What do I do?
- What are my favorite programming languages?
""")
print(f"Response: {response}\n")

print("\n9️⃣  Time-Based Memory Analysis")
print("-" * 60)

@tool(
    name="recent_topics",
    description="Extracts recent conversation topics"
)
def recent_topics(conversation_data: str, limit: int = 3) -> str:
    """Get recent conversation topics"""
    lines = [line.strip() for line in conversation_data.split('\n') if line.strip()]
    recent = lines[-limit:] if len(lines) >= limit else lines
    return f"Recent {len(recent)} topics:\n" + "\n".join(f"  - {topic}" for topic in recent)

agent.tool_registry.register_tool(recent_topics)

response = agent.chat("""
1. List my conversations
2. Use recent_topics to show my 3 most recent topics
3. Summarize what we've been discussing
""")
print(f"Response: {response}\n")

print("\n🔟  Memory-Based Decision Making")
print("-" * 60)

response = agent.chat("""
Based on my conversation history:
1. Search my memory for my skills and experience
2. Calculate if I'm qualified for a job requiring: Python, ML, 3+ years experience
3. Use get_user_info to verify my profile
4. Give me a yes/no answer with reasoning
""")
print(f"Response: {response}\n")

print("\n✅ Memory-Aware Tools Demo Completed!")
print("=" * 60)
print("\n📊 Memory Tools Demonstrated:")
print("  1. search_memory - Find information by keywords")
print("  2. get_user_info - Get complete user profile")
print("  3. list_conversations - List all chat history")
print("  4. Memory + calculation chains")
print("  5. Memory + text processing chains")
print("  6. Custom memory analysis tools")
print("  7. Multi-user memory isolation")
print("  8. Time-based memory queries")
print("  9. Memory-based decision making")
print("\n💡 Unique Feature:")
print("  - Agents can search their OWN conversation history!")
print("  - Self-aware AI that remembers and reasons about past interactions")
print("  - Enables context-aware responses and personalization")

