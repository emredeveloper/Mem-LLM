"""
Simple Example 2: Streaming
============================
Live streaming responses - Real-time output
"""

from mem_llm import MemAgent

agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    use_sql=False
)

agent.set_user("user1")

# Streaming response
print("Question: What is Python?\n")
print("Answer: ", end="", flush=True)

for chunk in agent.chat_stream("Write 2 sentences about Python programming language"):
    print(chunk, end="", flush=True)

print("\n")
