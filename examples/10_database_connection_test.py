"""
Example 10: Enterprise Database Migration
==========================================

Real-world scenario: Migrate customer service conversations to enterprise databases.

Use case: A company wants to:
1. Export conversation history from local SQLite
2. Import to PostgreSQL for analytics
3. Sync to MongoDB for real-time dashboard

Fill in your connection details and run to test.
"""

import logging

# Clean console output
logging.getLogger('MemAgent').setLevel(logging.ERROR)
logging.getLogger('mem_llm').setLevel(logging.ERROR)

from mem_llm import MemAgent, DataExporter, DataImporter

# ============================================================================
# CONFIGURATION - Fill in your connection details here
# ============================================================================

# PostgreSQL (for data analytics & reporting)
POSTGRESQL_ENABLED = False  # Set True to test
POSTGRESQL_URL = "postgresql://username:password@localhost:5432/dbname"

# MongoDB (for real-time dashboard & NoSQL flexibility)
MONGODB_ENABLED = False  # Set True to test
MONGODB_URL = "mongodb://localhost:27017/"
MONGODB_DATABASE = "customer_service"
MONGODB_COLLECTION = "support_chats"

# ============================================================================

def simulate_customer_service():
    """Simulate real customer service conversations"""
    print("📞 Simulating Customer Service Scenario...\n")
    
    # Use SQL directly - no JSON files
    agent = MemAgent(model="granite4:tiny-h", use_sql=True, db_path=":memory:")  # In-memory DB
    
    # Customer 1: Technical support
    agent.set_user("customer_001")
    print("👤 Customer #001 (Technical Issue):")
    agent.chat("My app keeps crashing on startup")
    agent.chat("I'm using iPhone 12, iOS 16.2")
    agent.chat("It started after the latest update")
    print("   ✅ 3 messages logged\n")
    
    # Customer 2: Billing inquiry
    agent.set_user("customer_002")
    print("👤 Customer #002 (Billing Issue):")
    agent.chat("I was charged twice this month")
    agent.chat("My card ending in 4532")
    agent.chat("Can you refund the duplicate charge?")
    print("   ✅ 3 messages logged\n")
    
    # Customer 3: Feature request
    agent.set_user("customer_003")
    print("👤 Customer #003 (Feature Request):")
    agent.chat("Can you add dark mode to the app?")
    agent.chat("My eyes hurt when using at night")
    print("   ✅ 2 messages logged\n")
    
    print("📊 Total: 3 customers, 8 conversations saved to SQLite\n")
    return agent


def test_postgresql():
    """Migration to PostgreSQL for analytics"""
    print("\n" + "="*70)
    print("SCENARIO 1: PostgreSQL Migration (Analytics & Reporting)")
    print("="*70 + "\n")
    
    print("🎯 Goal: Export conversations to PostgreSQL for BI tools\n")
    
    # Simulate conversations
    agent = simulate_customer_service()
    
    # Export all customers
    print("📤 Exporting to PostgreSQL...\n")
    exporter = DataExporter(agent.memory)
    
    total_exported = 0
    for customer_id in ["customer_001", "customer_002", "customer_003"]:
        result = exporter.export_to_postgresql(customer_id, POSTGRESQL_URL)
        
        if result['success']:
            total_exported += result['conversations']
            print(f"   ✅ {customer_id}: {result['conversations']} conversations")
        else:
            print(f"   ❌ {customer_id}: Failed - {result['error']}")
            return False
    
    if result.get('database_created'):
        print(f"\n   🆕 Database auto-created (ready for analytics!)")
    
    print(f"\n   📊 Total exported: {total_exported} conversations")
    print(f"   💡 Use Case: Connect Tableau/PowerBI for customer insights\n")
    
    # Verify import (in-memory, no JSON files)
    print("📥 Testing data retrieval...\n")
    new_agent = MemAgent(model="granite4:tiny-h", use_sql=True, db_path=":memory:")
    importer = DataImporter(new_agent.memory)
    
    result = importer.import_from_postgresql(POSTGRESQL_URL, "customer_001")
    if result['success']:
        print(f"   ✅ Data accessible: {result['conversations']} conversations retrieved")
        print(f"   ✅ Ready for SQL queries and analytics!\n")
    else:
        print(f"   ❌ Import failed: {result['error']}")
        return False
    
    print("="*70)
    print("✅ PostgreSQL migration successful!")
    print("="*70 + "\n")
    return True


def test_mongodb():
    """Sync to MongoDB for real-time dashboard"""
    print("\n" + "="*70)
    print("SCENARIO 2: MongoDB Sync (Real-time Dashboard)")
    print("="*70 + "\n")
    
    print("🎯 Goal: Sync conversations to MongoDB for live support dashboard\n")
    
    # Simulate conversations
    agent = simulate_customer_service()
    
    # Export all customers
    print("📤 Syncing to MongoDB...\n")
    exporter = DataExporter(agent.memory)
    
    total_synced = 0
    for customer_id in ["customer_001", "customer_002", "customer_003"]:
        result = exporter.export_to_mongodb(
            customer_id,
            MONGODB_URL,
            database=MONGODB_DATABASE,
            collection=MONGODB_COLLECTION
        )
        
        if result['success']:
            total_synced += result['conversations']
            print(f"   ✅ {customer_id}: {result['conversations']} conversations")
        else:
            print(f"   ❌ {customer_id}: Failed - {result['error']}")
            return False
    
    if result.get('database_created'):
        print(f"\n   🆕 Database: '{MONGODB_DATABASE}' created")
    if result.get('collection_created'):
        print(f"   🆕 Collection: '{MONGODB_COLLECTION}' created")
    
    print(f"\n   📊 Total synced: {total_synced} conversations")
    print(f"   💡 Use Case: Real-time support queue, agent performance metrics\n")
    
    # Verify access (in-memory, no JSON files)
    print("📥 Testing dashboard data access...\n")
    new_agent = MemAgent(model="granite4:tiny-h", use_sql=True, db_path=":memory:")
    importer = DataImporter(new_agent.memory)
    
    result = importer.import_from_mongodb(
        MONGODB_URL,
        "customer_002",
        database=MONGODB_DATABASE,
        collection=MONGODB_COLLECTION
    )
    
    if result['success']:
        print(f"   ✅ Data accessible: {result['conversations']} conversations")
        print(f"   ✅ Ready for real-time dashboard queries!\n")
    else:
        print(f"   ❌ Import failed: {result['error']}")
        return False
    
    print("="*70)
    print("✅ MongoDB sync successful!")
    print("="*70 + "\n")
    return True


def main():
    """Run enterprise database migration scenarios"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "ENTERPRISE DATABASE MIGRATION" + " "*23 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("� Scenario: Customer service data migration to enterprise databases\n")
    print("�📋 Configuration:")
    print(f"   PostgreSQL (Analytics): {'ENABLED ✅' if POSTGRESQL_ENABLED else 'DISABLED ❌'}")
    print(f"   MongoDB (Dashboard): {'ENABLED ✅' if MONGODB_ENABLED else 'DISABLED ❌'}\n")
    
    if not POSTGRESQL_ENABLED and not MONGODB_ENABLED:
        print("⚠️  No databases enabled! This is a real-world migration scenario.\n")
        print("💡 Setup Instructions:")
        print("\n1️⃣  Install Database Drivers:")
        print("   pip install mem-llm[postgresql]  # For PostgreSQL")
        print("   pip install mem-llm[mongodb]     # For MongoDB")
        print("   pip install mem-llm[databases]   # For both")
        
        print("\n2️⃣  Configure Connection Strings:")
        print("   Edit this file (10_database_connection_test.py):")
        print("   - POSTGRESQL_ENABLED = True")
        print("   - POSTGRESQL_URL = 'postgresql://user:pass@host:5432/dbname'")
        print("   - MONGODB_ENABLED = True")
        print("   - MONGODB_URL = 'mongodb://localhost:27017/'")
        
        print("\n3️⃣  Real-World Benefits:")
        print("   PostgreSQL → SQL queries, BI tools, complex analytics")
        print("   MongoDB → Real-time dashboard, flexible schema, high throughput")
        
        print("\n4️⃣  Run Migration:")
        print("   python 10_database_connection_test.py\n")
        return
    
    results = []
    
    # PostgreSQL migration
    if POSTGRESQL_ENABLED:
        try:
            success = test_postgresql()
            results.append(("PostgreSQL Migration", success))
        except Exception as e:
            print(f"\n❌ PostgreSQL error: {e}")
            print(f"💡 Check: PostgreSQL running? Correct credentials?\n")
            results.append(("PostgreSQL Migration", False))
    
    # MongoDB sync
    if MONGODB_ENABLED:
        try:
            success = test_mongodb()
            results.append(("MongoDB Sync", success))
        except Exception as e:
            print(f"\n❌ MongoDB error: {e}")
            print(f"💡 Check: MongoDB running? Connection accessible?\n")
            results.append(("MongoDB Sync", False))
    
    # Final summary
    print("\n" + "="*70)
    print("MIGRATION SUMMARY")
    print("="*70)
    for scenario, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {scenario}: {status}")
    
    print("\n💡 Next Steps:")
    if all(success for _, success in results):
        print("   ✅ All migrations successful!")
        print("   → Connect your BI tools to PostgreSQL")
        print("   → Build real-time dashboard with MongoDB")
        print("   → Scale your customer service analytics")
    else:
        print("   ⚠️  Some migrations failed - check configuration")
        print("   → Verify database servers are running")
        print("   → Double-check connection credentials")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
