"""
Quickstart 3: Multi-Backend Support
====================================
Test different LLM backends (Ollama, LM Studio).

Installation:
    pip install mem-llm

Requirements:
    - Ollama OR LM Studio running locally
"""

from mem_llm import MemAgent
import requests

def check_backend_available(name, url):
    """Check if backend is available."""
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"  ✓ {name} is available at {url}")
            return True
    except:
        pass
    print(f"  ✗ {name} is NOT available at {url}")
    return False

def test_backend(backend, model, base_url):
    """Test a specific backend."""
    print(f"\nTesting {backend.upper()} backend...")
    print("-"*60)
    
    try:
        agent = MemAgent(
            backend=backend,
            model=model,
            base_url=base_url,
            use_sql=False
        )
        
        agent.set_user(f"{backend}_user")
        
        prompt = "Say 'Hello from {}!' in one sentence.".format(backend.upper())
        response = agent.chat(prompt)
        
        print(f"[Prompt]: {prompt}")
        print(f"[Response]: {response}")
        print(f"✓ {backend.upper()} backend works!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("="*60)
    print("Mem-LLM Quickstart 3: Multi-Backend Support")
    print("="*60)
    
    print("\nChecking available backends...")
    print("-"*60)
    
    ollama_available = check_backend_available("Ollama", "http://localhost:11434/api/tags")
    lmstudio_available = check_backend_available("LM Studio", "http://localhost:1234/v1/models")
    
    if not ollama_available and not lmstudio_available:
        print("\n⚠ No backends available!")
        print("Please start Ollama or LM Studio first.")
        return
    
    # Test Ollama
    if ollama_available:
        test_backend(
            backend='ollama',
            model='granite4:3b',
            base_url='http://localhost:11434'
        )
    
    # Test LM Studio
    if lmstudio_available:
        test_backend(
            backend='lmstudio',
            model='local-model',
            base_url='http://localhost:1234'
        )
    
    # Auto-detect backend
    print("\nTesting Auto-Detect Backend...")
    print("-"*60)
    try:
        agent = MemAgent(auto_detect_backend=True)
        agent.set_user("auto_user")
        response = agent.chat("Which backend am I using?")
        print(f"[Response]: {response}")
        print(f"✓ Auto-detect works! Detected: {agent.backend}")
    except Exception as e:
        print(f"✗ Auto-detect failed: {e}")
    
    print("\n" + "="*60)
    print("✓ Multi-backend test complete!")
    print("="*60)

if __name__ == "__main__":
    main()

