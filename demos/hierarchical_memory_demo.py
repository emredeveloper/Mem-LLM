#!/usr/bin/env python3
"""
Hierarchical Memory System Demo
================================

Demonstrates the 4-layer hierarchical memory system:
- Episode Layer: Raw interactions
- Trace Layer: Short-term memory
- Category Layer: Topic-based organization
- Domain Layer: High-level context
"""

import os
import sys

# Add parent directory to path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from mem_llm import MemAgent  # noqa: E402

print(f"📂 Loaded MemAgent from: {MemAgent.__module__}")

import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mem_llm")
logger.setLevel(logging.DEBUG)


def run_demo(backend="ollama", model="granite4:3b"):
    print(f"\n🚀 Starting Hierarchical Memory Demo with {backend} ({model})...")

    # Initialize agent with hierarchical memory enabled
    agent = MemAgent(
        backend=backend,
        model=model,
        enable_hierarchical_memory=True,
        use_sql=False,  # Use JSON for simple demo
    )

    user_id = "test_user_hierarchy"
    agent.set_user(user_id)

    # 1. Python Topic
    print("\n1️⃣  Discussing Python (Category: python_coding)...")
    response = agent.chat("How do I create a list in Python?")
    print(f"Bot: {response[:100]}...")

    response = agent.chat("What about a dictionary?")
    print(f"Bot: {response[:100]}...")

    # 2. Travel Topic
    print("\n2️⃣  Discussing Travel (Category: travel)...")
    response = agent.chat("I want to visit Japan next year.")
    print(f"Bot: {response[:100]}...")

    # 3. Check Hierarchy
    print("\n🔍 Inspecting Memory Hierarchy...")

    h_mem = agent.hierarchical_memory

    print("\n--- Domain Layer ---")
    domains = h_mem.domain_layer.get(None, user_id=user_id)
    for d in domains:
        print(f"Domain: {d['name']} | Summary: {d['summary']}")

    print("\n--- Category Layer ---")
    cats = h_mem.category_layer.get(None, user_id=user_id)
    for c in cats:
        print(f"Category: {c['name']} | Interactions: {c['interaction_count']}")

    print("\n--- Trace Layer (Recent) ---")
    traces = h_mem.trace_layer.get(None, user_id=user_id)
    for t in traces:
        print(f"Trace: {t['content']} (Category: {t['category']})")

    print("\n--- Context Injection ---")
    context = h_mem.get_context(user_id)
    print(f"Context injected into LLM:\n{context}")


if __name__ == "__main__":
    # Default to Ollama, but allow LM Studio via args
    backend = "ollama"
    if len(sys.argv) > 1:
        backend = sys.argv[1]

    run_demo(backend=backend)
