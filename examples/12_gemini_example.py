"""
Example 12: Google Gemini Backend
==================================

Use Google Gemini API as backend.

Quick Usage:
    agent = MemAgent(
        backend='gemini',
        model='gemini-2.5-flash',
        api_key='your-api-key'
    )
"""

import os
from mem_llm import MemAgent

print("=" * 60)
print("Google Gemini Backend")
print("=" * 60)

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("\n❌ Error: GEMINI_API_KEY not set")
    print("Set it: export GEMINI_API_KEY='your-key'")
    exit(1)

# Create agent with Gemini
agent = MemAgent(
    backend='gemini',
    model='gemini-2.5-flash',
    api_key=api_key,
    use_sql=False,
    check_connection=False
)

agent.set_user("bob")

# Chat
print("\n💬 Conversation:")
messages = [
    "Hello! My name is Bob and I'm a software engineer.",
    "I develop web applications with React and Node.js.",
    "Do you remember my name, profession, and the technologies I use?"
]

for msg in messages:
    print(f"\nUser: {msg}")
    response = agent.chat(msg)
    print(f"AI: {response}")

print("\n" + "=" * 60)
