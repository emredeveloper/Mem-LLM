"""
Example 09: Data Export/Import
================================
Export and import conversations to JSON, CSV, SQLite.
"""

from mem_llm import MemAgent, DataExporter, DataImporter

print("\n" + "="*50)
print("DATA EXPORT/IMPORT")
print("="*50 + "\n")

# Create agent and add conversations
agent = MemAgent(model="granite4:tiny-h", use_sql=True)
agent.set_user("john")

conversations = [
    "I'm John, a software engineer.",
    "I work with Python and JavaScript.",
    "Currently building microservices."
]

for msg in conversations:
    agent.chat(msg)
    print(f"Chat: {msg}")

print(f"\nSaved: {len(conversations)} conversations\n")

# Export
exporter = DataExporter(agent.memory)

json_result = exporter.export_to_json("john", "exports/john.json")
print(f"JSON: {json_result['file']}")

csv_result = exporter.export_to_csv("john", "exports/john.csv")
print(f"CSV: {csv_result['file']}")

db_result = exporter.export_to_sqlite("john", "exports/john.db")
print(f"SQLite: {db_result['file']}")

# Import
new_agent = MemAgent(model="granite4:tiny-h", use_sql=False, memory_dir="import_test")
importer = DataImporter(new_agent.memory)

import_result = importer.import_from_json("exports/john.json", user_id="john_copy")
print(f"\nImported: {import_result['conversations']} conversations")

print("\n" + "="*50 + "\n")
