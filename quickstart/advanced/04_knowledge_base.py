"""
Advanced Example 4: Knowledge Base
===================================
Vector search and knowledge base - Semantic search & RAG
"""

from mem_llm import MemAgent

# Agent with knowledge base
agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    use_sql=False,
    enable_kb=True  # ⚠️ Enable Knowledge Base
)
agent.set_user("kb_user")

# ============================================================================
# 1️⃣ Adding Documents
# ============================================================================
print("📚 Adding documents to knowledge base...")
print("-" * 50)

documents = [
    "Python is a high-level programming language known for its simplicity.",
    "JavaScript is the language of the web, used for frontend and backend.",
    "Machine Learning is a subset of AI focused on learning from data.",
    "Deep Learning uses neural networks with multiple layers.",
    "Natural Language Processing helps computers understand human language."
]

for doc in documents:
    agent.add_document(doc)
    print(f"  ✅ Added: {doc[:50]}...")

# ============================================================================
# 2️⃣ Vector Search
# ============================================================================
print("\n\n🔍 Vector Search:")
print("-" * 50)

query = "Tell me about programming languages"
print(f"\nQuery: {query}")
print("\nTop matches:")

# Semantic search
results = agent.search_documents(query, limit=2)
for i, (doc, score) in enumerate(results, 1):
    print(f"  {i}. [{score:.2f}] {doc[:60]}...")

# ============================================================================
# 3️⃣ RAG (Retrieval-Augmented Generation)
# ============================================================================
print("\n\n🤖 RAG Response:")
print("-" * 50)

# LLM uses knowledge base automatically
response = agent.chat("What programming languages do you know about?")
print(f"\n{response}")

# ============================================================================
# 4️⃣ Statistics
# ============================================================================
print("\n\n📊 Knowledge Base Stats:")
print("-" * 50)

stats = agent.get_kb_stats()
print(f"  Documents: {stats.get('document_count', 0)}")
print(f"  Total chunks: {stats.get('chunk_count', 0)}")

print("\n✅ Knowledge base demo complete!")
