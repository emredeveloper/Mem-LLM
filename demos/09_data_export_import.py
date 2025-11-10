"""
Example 9: Data Export/Import
===============================

Export and import conversations to JSON, CSV, SQLite.

Quick Usage:
    exporter = DataExporter(agent.memory)
    exporter.export_to_json("user_id", "output.json")
    
    importer = DataImporter(new_agent.memory)
    importer.import_from_json("output.json", user_id="new_user")
"""

from mem_llm import MemAgent, DataExporter, DataImporter

print("=" * 60)
print("Data Export/Import")
print("=" * 60)

# Create agent and add conversations
agent = MemAgent(model="granite4:tiny-h", use_sql=True)
agent.set_user("john")

conversations = [
    "I'm John, a software engineer.",
    "I work with Python and JavaScript.",
    "Currently building microservices."
]

print("\n💬 Adding conversations:")
for msg in conversations:
    agent.chat(msg)
    print(f"  {msg}")

# Export
print("\n📤 Exporting...")
exporter = DataExporter(agent.memory)

json_result = exporter.export_to_json("john", "exports/john.json")
print(f"✅ JSON: {json_result['file']}")

csv_result = exporter.export_to_csv("john", "exports/john.csv")
print(f"✅ CSV: {csv_result['file']}")

db_result = exporter.export_to_sqlite("john", "exports/john.db")
print(f"✅ SQLite: {db_result['file']}")

# Import
print("\n📥 Importing...")
new_agent = MemAgent(model="granite4:tiny-h", use_sql=False, memory_dir="import_test")
importer = DataImporter(new_agent.memory)

import_result = importer.import_from_json("exports/john.json", user_id="john_copy")
print(f"✅ Imported: {import_result['conversations']} conversations")

print("\n" + "=" * 60)
