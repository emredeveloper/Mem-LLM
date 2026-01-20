"""Run the API server with auth enabled.

Usage:
  python demos/01_api_server_demo.py

Then call:
  curl -H "X-API-Key: dev-api-key-change-in-production" http://localhost:8000/api/v1/health
"""

import uvicorn

from demo_config import ALLOW_ORIGINS, API_KEY, AUTH_DISABLED


def main() -> None:
    import os

    os.environ.setdefault("MEM_LLM_ALLOW_ORIGINS", ALLOW_ORIGINS)
    os.environ.setdefault("MEM_LLM_API_KEY", API_KEY)
    os.environ.setdefault("MEM_LLM_AUTH_DISABLED", AUTH_DISABLED)
    port = int(os.environ.get("MEM_LLM_DEMO_PORT", "8001"))
    uvicorn.run("mem_llm.api_server:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
