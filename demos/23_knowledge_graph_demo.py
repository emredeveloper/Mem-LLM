import os
import sys
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_llm import MemAgent


def main():
    print("🚀 Initializing MemAgent with Knowledge Graph...")

    # Enable graph memory and advanced features
    agent = MemAgent(
        auto_detect_backend=True,
        enable_graph_memory=True,
        # Use simple JSON memory for demo to allow local graph.json creation
        use_sql=False,
        memory_dir="demo_memories",
    )
    agent.set_user("demo_user")  # Fix: User ID required for LLM chat

    if not agent.graph_store:
        print("❌ Graph Store not available. Please install networkx: pip install networkx")
        return

    print("\n🕸️  KNOWLEDGE GRAPH DEMO")
    print("========================")

    # 1. Automatic Extraction from Text
    text = "Elon Musk is the CEO of SpaceX. SpaceX is located in Hawthorne, California. Elon Musk also founded Neuralink."
    print(f'\n📝 Analyzing text: "{text}"')

    print("   Extracting triplets... (this uses the LLM)")
    triplets = agent.graph_extractor.extract(text)

    print(f"   Found {len(triplets)} relationships:")
    for source, relation, target in triplets:
        print(f"   - {source} --[{relation}]--> {target}")
        # Add to graph
        agent.graph_store.add_triplet(source, relation, target)

    # 2. Manual Addition
    print("\n➕ Adding manual relationship...")
    agent.graph_store.add_triplet("Neuralink", "develops", "Brain-Computer Interfaces")
    print("   - Neuralink --[develops]--> Brain-Computer Interfaces")

    # 3. Search the Graph
    query = "Elon Musk"
    print(f"\n🔍 Searching graph for '{query}'...")
    results = agent.graph_store.search(query, depth=1)

    if results:
        for s, r, t in results:
            print(f"   Found: {s} {r} {t}")
    else:
        print("   No results found.")

    # 4. Save
    agent.graph_store.save()
    print(f"\n💾 Graph saved to {agent.graph_store.persistence_path}")

    # Visualization Tip
    print(
        "\n💡 Tip: Run the Web UI (python -m mem_llm.api_server) to visualize this graph interactively!"
    )


if __name__ == "__main__":
    main()
