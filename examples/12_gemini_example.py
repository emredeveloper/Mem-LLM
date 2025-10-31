"""
Example 12: Google Gemini Backend
==================================
Simple example using Google Gemini API.
"""

import os
from mem_llm import MemAgent

print("\n" + "="*50)
print("GOOGLE GEMINI EXAMPLE")
print("="*50 + "\n")

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("Error: GEMINI_API_KEY not set")
    print("Set it: export GEMINI_API_KEY='your-key'")
    exit(1)

# Create agent with Gemini
agent = MemAgent(
    backend='gemini',
    model='gemini-2.5-flash',
    api_key=api_key,
    use_sql=False
)

agent.set_user("bob")

# Chat
conversations = [
    "Hello! My name is Bob and I'm a software engineer.",
    "I develop web applications with React and Node.js.",
    "Do you remember my name, profession, and the technologies I use?"
]

for msg in conversations:
    print(f"User: {msg}")
    response = agent.chat(msg)
    print(f"AI: {response}\n")

print("="*50 + "\n")
