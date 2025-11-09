"""
Mem-LLM Web UI Launcher
========================
Simple launcher that starts API server and opens Web UI
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def main():
    print("="*70)
    print(" MEM-LLM WEB UI LAUNCHER")
    print("="*70)
    
    # Check if API server is already running
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("\n✓ API Server is already running")
            skip_start = True
        else:
            skip_start = False
    except:
        skip_start = False
    
    if not skip_start:
        # Start API server in new window
        print("\nStarting API Server...")
        mem_llm_path = Path("Memory LLM")
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(
                    'start "Mem-LLM API Server" cmd /k "python -m mem_llm.api_server"',
                    shell=True,
                    cwd=str(mem_llm_path)
                )
            else:  # Linux/Mac
                subprocess.Popen(
                    ['python', '-m', 'mem_llm.api_server'],
                    cwd=str(mem_llm_path)
                )
            
            print("✓ API Server started in new window")
            print("  URL: http://localhost:8000")
            
            # Wait for server to be ready
            print("\nWaiting for API Server to be ready...")
            for i in range(10):
                time.sleep(1)
                try:
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=1)
                    if response.status_code == 200:
                        print("✓ API Server is ready!")
                        break
                except:
                    print(".", end="", flush=True)
            else:
                print("\n⚠ API Server may still be starting...")
                print("  Give it a few more seconds")
                
        except Exception as e:
            print(f"✗ Error starting API Server: {e}")
            print("\nManual start:")
            print("  cd 'Memory LLM'")
            print("  python -m mem_llm.api_server")
            return
    
    # Open Web UI
    print("\nOpening Web UI in browser...")
    web_ui_path = Path("Memory LLM") / "web_ui" / "index.html"
    
    if not web_ui_path.exists():
        print(f"✗ Web UI not found: {web_ui_path}")
        return
    
    web_ui_url = web_ui_path.absolute().as_uri()
    
    try:
        webbrowser.open(web_ui_url)
        print("✓ Web UI opened in browser")
    except Exception as e:
        print(f"⚠ Could not open browser: {e}")
        print(f"\nOpen manually: {web_ui_url}")
    
    print("\n" + "="*70)
    print(" READY TO USE!")
    print("="*70)
    print("""
In the Web UI:
  1. Enter User ID (e.g., user123)
  2. Select Backend (Ollama/LM Studio)
  3. Click "Connect" button
  4. Start chatting!

Pages:
  - Chat: index.html
  - Memory: memory.html
  - Metrics: metrics.html

API Documentation:
  http://localhost:8000/docs

To stop API Server: Close the API Server window or press CTRL+C
""")
    print("="*70)

if __name__ == "__main__":
    main()

