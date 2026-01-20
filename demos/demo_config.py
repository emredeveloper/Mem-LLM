"""Shared demo configuration (override via environment variables)."""

import os

BACKEND = os.environ.get("MEM_LLM_DEMO_BACKEND", "lmstudio")
BASE_URL = os.environ.get("MEM_LLM_DEMO_BASE_URL", "http://127.0.0.1:1234")
MODEL = os.environ.get("MEM_LLM_DEMO_MODEL", "google/gemma-3-4b")

API_KEY = os.environ.get("MEM_LLM_DEMO_API_KEY", "dev-api-key-change-in-production")
ALLOW_ORIGINS = os.environ.get("MEM_LLM_DEMO_ALLOW_ORIGINS", "http://localhost:3000")
AUTH_DISABLED = os.environ.get("MEM_LLM_DEMO_AUTH_DISABLED", "true")

TOOL_ALLOWLIST = os.environ.get("MEM_LLM_DEMO_TOOL_ALLOWLIST", "safe_upper").split(",")
TOOL_DENYLIST = os.environ.get("MEM_LLM_DEMO_TOOL_DENYLIST", "unsafe_lower").split(",")
TOOL_ALLOWLIST_ONLY = os.environ.get("MEM_LLM_DEMO_TOOL_ALLOWLIST_ONLY", "true").lower() in (
    "1",
    "true",
    "yes",
)
