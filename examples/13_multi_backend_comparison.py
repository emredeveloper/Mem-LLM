"""
Example 13: Multi-Backend Comparison
====================================

Compare responses across different backends (Ollama vs LM Studio).

Quick Usage:
    agent1 = MemAgent(backend='ollama', model='granite4:3b')
    agent2 = MemAgent(backend='lmstudio', model='local-model')
"""

import time
from mem_llm import MemAgent, LLMClientFactory

print("=" * 60)
print("Multi-Backend Comparison")
print("=" * 60)

test_prompt = "What is Python? Answer in 2 sentences."

# Check available backends
backends = []

if LLMClientFactory.check_backend_availability('ollama'):
    backends.append(('Ollama', 'ollama', 'granite4:3b', {}))

if LLMClientFactory.check_backend_availability('lmstudio'):
    backends.append(('LM Studio', 'lmstudio', 'local-model', {}))

if not backends:
    print("\n❌ No backends available!")
    exit(1)

print(f"\n📊 Testing {len(backends)} backend(s):\n")

# Test each backend
for name, backend, model, kwargs in backends:
    print(f"[{name}]")
    print(f"Prompt: {test_prompt}")
    
    try:
        agent = MemAgent(
            backend=backend,
            model=model,
            use_sql=False,
            check_connection=False,
            **kwargs
        )
        agent.set_user("tester")
        
        start = time.time()
        response = agent.chat(test_prompt)
        elapsed = time.time() - start
        
        print(f"⏱️  Time: {elapsed:.2f}s")
        print(f"💬 Response: {response}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")

print("=" * 60)
