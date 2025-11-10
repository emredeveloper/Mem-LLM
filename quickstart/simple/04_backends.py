"""
Simple Example 4: Multiple Backends
====================================
Different LLM backends - Ollama, LM Studio
"""

from mem_llm import MemAgent

# OPTION 1: Ollama
agent_ollama = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    use_sql=False
)

# OPTION 2: LM Studio
agent_lmstudio = MemAgent(
    backend='lmstudio',
    model='any-model',  # Any model loaded in LM Studio
    use_sql=False
)

# OPTION 3: Auto-detect (tries Ollama and LM Studio)
agent_auto = MemAgent(
    backend='auto',     # Auto-detect available backend
    model='llama3.2:3b',
    use_sql=False
)

# Use one
agent = agent_ollama  # Choose your preferred backend
agent.set_user("test")

response = agent.chat("Hello!")
print(response)
