"""
Example 13: Multi-Backend Comparison
=====================================
Compare responses across different backends.
"""

import os
import time
from mem_llm import MemAgent, LLMClientFactory

print("\n" + "="*50)
print("MULTI-BACKEND COMPARISON")
print("="*50 + "\n")

test_prompt = "What is Python? Answer in 2 sentences."

# Check available backends
backends = []

if LLMClientFactory.check_backend_availability('ollama'):
    backends.append(('Ollama', 'ollama', 'granite4:tiny-h', {}))

if LLMClientFactory.check_backend_availability('lmstudio'):
    backends.append(('LM Studio', 'lmstudio', 'local-model', {}))

gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    backends.append(('Gemini', 'gemini', 'gemini-2.5-flash', {'api_key': gemini_key}))

if not backends:
    print("No backends available!")
    exit(1)

print(f"Testing {len(backends)} backend(s):\n")

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
        
        print(f"Time: {elapsed:.2f}s")
        print(f"Response: {response}\n")
        
    except Exception as e:
        print(f"Error: {e}\n")

print("="*50 + "\n")
