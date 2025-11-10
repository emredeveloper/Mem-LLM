"""
Example 16: Vector Search & Semantic Knowledge Base (v1.3.2+)
===============================================================

Semantic search with ChromaDB - understands meaning, not just keywords!

Requirements:
    pip install chromadb sentence-transformers

Quick Usage:
    agent = MemAgent(use_sql=True, enable_vector_search=True)
    agent.memory.sync_all_kb_to_vector_store()  # Sync existing KB
    agent.chat("Siparişim ne zaman gelecek?")  # Finds "When will my order arrive?"
"""

from mem_llm import MemAgent

print("=" * 60)
print("Vector Search Demo")
print("=" * 60)

# 1. Create agent with vector search enabled
print("\n1️⃣ Creating agent with vector search...")
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=True,
    enable_vector_search=True,  # 🔍 Enable semantic search
    load_knowledge_base=True,
    check_connection=False
)

# 2. Add KB entries
print("\n2️⃣ Adding knowledge base entries...")
agent.memory.add_knowledge(
    category="shipping",
    question="When will my order arrive?",
    answer="Orders are shipped within 2-3 business days and delivered within 3-5 days.",
    keywords=["shipping", "delivery"]
)

agent.memory.add_knowledge(
    category="return",
    question="How do I return a product?",
    answer="You can return products within 14 days. Create a return request from My Orders page.",
    keywords=["return", "refund"]
)

# 3. Sync to vector store
print("\n3️⃣ Syncing KB to vector store...")
if hasattr(agent.memory, 'sync_all_kb_to_vector_store'):
    count = agent.memory.sync_all_kb_to_vector_store()
    print(f"   ✅ Synced {count} entries")

# 4. Test semantic search
print("\n4️⃣ Testing semantic search:")
queries = [
    "Siparişim ne zaman gelecek?",  # Turkish
    "How long does delivery take?",  # English - different words, same meaning
    "I want to send this back"  # Natural language - finds return policy
]

for query in queries:
    results = agent.memory.search_knowledge(query, limit=2, use_vector_search=True)
    print(f"\n   Query: '{query}'")
    if results:
        best = results[0]
        print(f"   ✅ Found: {best.get('question', '')}")
        print(f"      Score: {best.get('score', 0):.2%}")
    else:
        print("   ❌ No results")

# 5. Compare with keyword search
print("\n5️⃣ Comparison: Keyword vs Vector")
test_query = "When does my package arrive?"

print(f"\n   Query: '{test_query}'")
keyword_results = agent.memory.search_knowledge(test_query, use_vector_search=False)
vector_results = agent.memory.search_knowledge(test_query, use_vector_search=True)

print(f"   Keyword Search: {len(keyword_results)} results")
print(f"   Vector Search:  {len(vector_results)} results (similarity: {vector_results[0].get('score', 0):.2%} if available)")

print("\n" + "=" * 60)
print("✅ Vector Search Demo Complete!")
print("\n💡 Key Benefits:")
print("   • Understands meaning, not just keywords")
print("   • Works with natural language queries")
print("   • Better relevancy for complex questions")
print("=" * 60)
