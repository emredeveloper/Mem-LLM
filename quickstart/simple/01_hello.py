"""
Simple Example 1: Hello World
==============================
Basic chat example - Most basic usage
"""

from mem_llm import MemAgent

# Create agent
agent = MemAgent(
    backend='ollama',        # or 'lmstudio'
    model='llama3.2:3b',
    use_sql=False
)

# Set user
agent.set_user("john")

# Chat
response = agent.chat("Hello! My name is John")
print(response)

response = agent.chat("Do you remember my name?")
print(response)
