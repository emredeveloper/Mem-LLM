"""
Example 10: Database Export
===========================

Export conversations to PostgreSQL and MongoDB.

Quick Usage:
    exporter = DataExporter(agent.memory)
    exporter.export_to_postgresql("user_id", "postgresql://...")
    exporter.export_to_mongodb("user_id", "mongodb://...")
"""

from mem_llm import MemAgent, DataExporter

# Configure your database URLs
POSTGRESQL_URL = "postgresql://user:pass@localhost:5432/db"
MONGODB_URL = "mongodb://localhost:27017/"

print("=" * 60)
print("Database Export")
print("=" * 60)

# Create agent
agent = MemAgent(model="granite4:tiny-h", use_sql=True, db_path=":memory:")
agent.set_user("customer_001")

conversations = [
    "My app keeps crashing",
    "I'm using iPhone 12, iOS 16.2",
    "Tried reinstalling but same issue"
]

print("\n💬 Adding conversations:")
for msg in conversations:
    agent.chat(msg)
    print(f"  {msg}")

# Export
print("\n📤 Exporting to databases...")
exporter = DataExporter(agent.memory)

# PostgreSQL
try:
    pg_result = exporter.export_to_postgresql("customer_001", POSTGRESQL_URL)
    if pg_result['success']:
        print(f"✅ PostgreSQL: {pg_result['conversations']} conversations")
    else:
        print(f"❌ PostgreSQL: {pg_result['error']}")
except Exception as e:
    print(f"⚠️  PostgreSQL: {e}")

# MongoDB
try:
    mongo_result = exporter.export_to_mongodb("customer_001", MONGODB_URL)
    if mongo_result['success']:
        print(f"✅ MongoDB: {mongo_result['conversations']} conversations")
    else:
        print(f"❌ MongoDB: {mongo_result['error']}")
except Exception as e:
    print(f"⚠️  MongoDB: {e}")

print("\n" + "=" * 60)
