"""
Quickstart 4: Web UI & REST API
================================
Launch the Web UI with REST API server.

Installation:
    pip install mem-llm[api]

Requirements:
    - Ollama OR LM Studio running locally
"""

import subprocess
import webbrowser
import time
import sys
import requests

def check_backend_available():
    """Check if any backend is available."""
    backends = []
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            backends.append("Ollama (http://localhost:11434)")
    except:
        pass
    
    # Check LM Studio
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=2)
        if response.status_code == 200:
            backends.append("LM Studio (http://localhost:1234)")
    except:
        pass
    
    return backends

def wait_for_api_server(timeout=30):
    """Wait for API server to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def main():
    print("="*60)
    print("Mem-LLM Quickstart 4: Web UI & REST API")
    print("="*60)
    
    print("\nChecking backends...")
    backends = check_backend_available()
    
    if backends:
        print("✓ Available backends:")
        for backend in backends:
            print(f"  - {backend}")
    else:
        print("⚠ No backends detected!")
        print("Please start Ollama or LM Studio first.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("\nStarting API server...")
    print("-"*60)
    
    try:
        # Start API server
        from mem_llm import api_server
        
        print("✓ API server module loaded")
        print("\nStarting server at http://localhost:8000")
        print("\nAvailable endpoints:")
        print("  - Web UI:    http://localhost:8000/")
        print("  - Memory:    http://localhost:8000/memory")
        print("  - Metrics:   http://localhost:8000/metrics")
        print("  - API Docs:  http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the server")
        print("="*60)
        
        # Run server (blocking)
        import uvicorn
        uvicorn.run(api_server.app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nAlternative: Use the CLI command:")
        print("  mem-llm-web")

if __name__ == "__main__":
    main()

