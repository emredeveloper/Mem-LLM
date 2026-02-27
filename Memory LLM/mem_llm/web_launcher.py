#!/usr/bin/env python3
"""
Web UI Launcher for Mem-LLM
Starts the API server and opens the Web UI in the browser.
"""

import sys
import threading
import time
import webbrowser

import requests


def check_backend_available():
    """Check if Ollama or LM Studio is available."""
    backends = []

    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            backends.append("Ollama (http://localhost:11434)")
    except Exception:
        pass

    # Check LM Studio
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=2)
        if response.status_code == 200:
            backends.append("LM Studio (http://localhost:1234)")
    except Exception:
        pass

    return backends


def check_api_ready(url="http://localhost:8000/api/v1/health", timeout=30):
    """Wait for API server to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def start_api_server():
    """Start the FastAPI server in a subprocess."""
    try:
        # Import here to avoid circular imports
        import uvicorn

        from mem_llm.api_server import app

        # Run server in a thread
        def run_server():
            uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        return server_thread
    except Exception as e:
        print(f" Failed to start API server: {e}")
        return None


def main():
    """Main entry point for the web launcher."""
    print(" Mem-LLM Web UI Launcher")
    print("=" * 50)

    # Check available backends
    print("\n Checking available backends...")
    backends = check_backend_available()

    if backends:
        print(" Available backends:")
        for backend in backends:
            print(f"   - {backend}")
    else:
        print("  No local backends detected!")
        print("   Please start Ollama or LM Studio first:")
        print("   - Ollama: https://ollama.ai")
        print("   - LM Studio: https://lmstudio.ai")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != "y":
            sys.exit(0)

    # Start API server
    print("\n Starting API server...")
    server_thread = start_api_server()

    if not server_thread:
        print(" Failed to start API server!")
        sys.exit(1)

    # Wait for server to be ready
    print(" Waiting for API server to be ready...")
    if not check_api_ready():
        print(" API server failed to start within 30 seconds!")
        sys.exit(1)

    print(" API server is ready!")

    # Open browser
    web_url = "http://localhost:8000/"
    print(f"\n Opening Web UI at {web_url}")
    webbrowser.open(web_url)

    print("\n" + "=" * 50)
    print(" Mem-LLM Web UI is running!")
    print("   - Chat: http://localhost:8000/")
    print("   - Memory: http://localhost:8000/memory")
    print("   - Metrics: http://localhost:8000/metrics")
    print("   - API Docs: http://localhost:8000/docs")
    print("\n   Press Ctrl+C to stop the server.")
    print("=" * 50)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()

