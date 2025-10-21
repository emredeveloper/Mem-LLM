"""
Example 09: Data Export/Import
================================

Export and import conversations to:
- JSON files
- CSV files  
- SQLite databases
- PostgreSQL (optional)
- MongoDB (optional)
"""

import logging

# Suppress verbose logs
logging.getLogger('MemAgent').setLevel(logging.ERROR)
logging.getLogger('mem_llm').setLevel(logging.ERROR)

from mem_llm import MemAgent, DataExporter, DataImporter

print("\n" + "="*70)
print("DATA EXPORT/IMPORT - Simple Example")
print("="*70 + "\n")

# Create agent and add conversations
print("1️⃣  Creating conversations...\n")
agent = MemAgent(model="granite4:tiny-h", use_sql=True)
agent.set_user("john")

conversations = [
    "I'm John, a software engineer.",
    "I work with Python and JavaScript.",
    "Currently building microservices.",
    "Interested in cloud architecture.",
    "Using Docker and Kubernetes.",
]

for msg in conversations:
    agent.chat(msg)
    print(f"   💬 {msg}")

print(f"\n   ✅ Saved {len(conversations)} conversations\n")

# Export to different formats
print("2️⃣  Exporting data...\n")

exporter = DataExporter(agent.memory)

# Export to JSON
json_result = exporter.export_to_json("john", "exports/john.json")
print(f"   📄 JSON: {json_result['conversations']} conversations → {json_result['file']}")

# Export to CSV
csv_result = exporter.export_to_csv("john", "exports/john.csv")
print(f"   📊 CSV: {csv_result['conversations']} conversations → {csv_result['file']}")

# Export to SQLite
db_result = exporter.export_to_sqlite("john", "exports/john.db")
print(f"   🗄️  SQLite: {db_result['conversations']} conversations → {db_result['file']}")

print(f"\n   ✅ Export complete!\n")

# Import example
print("3️⃣  Importing data...\n")

# Create new agent
new_agent = MemAgent(model="granite4:tiny-h", use_sql=False, memory_dir="import_test")
importer = DataImporter(new_agent.memory)

# Import from JSON
import_result = importer.import_from_json("exports/john.json", user_id="john_copy")
print(f"   ✅ Imported {import_result['conversations']} conversations from JSON")

# Verify imported data
imported_convs = new_agent.memory.get_recent_conversations("john_copy", 10)
print(f"   ✅ Verified: {len(imported_convs)} conversations available\n")

# Database support info
print("="*70)
print("MULTI-DATABASE SUPPORT")
print("="*70 + "\n")

print("📦 Built-in Support:")
print("   ✅ JSON - Human readable, portable")
print("   ✅ CSV - Spreadsheet compatible")
print("   ✅ SQLite - Fast, local database\n")

print("🔌 Optional Support (install packages):")
print("   • PostgreSQL: pip install psycopg2-binary")
print("   • MongoDB: pip install pymongo\n")

print("💡 Usage Examples:")
print("   # PostgreSQL")
print('   exporter.export_to_postgresql("user", "postgresql://user:pass@localhost/db")')
print()
print("   # MongoDB")
print('   exporter.export_to_mongodb("user", "mongodb://localhost:27017/")')

print("\n" + "="*70)
print("✅ Done! Your data is portable and safe.")
print("="*70 + "\n")
