"""
Test Suite for Data Export/Import System
Tests JSON, CSV, SQLite, PostgreSQL, and MongoDB support
"""

import csv
import json
import os
import shutil
import sqlite3

# Add parent directory to path
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mem_llm import MemAgent
from mem_llm.data_export_import import DataExporter, DataImporter
from mem_llm.memory_db import SQLMemoryManager
from mem_llm.memory_manager import MemoryManager


class TestDataExportImport(unittest.TestCase):
    """Test data export and import functionality"""

    def setUp(self):
        """Set up test environment"""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Create memory manager with test data
        self.memory = MemoryManager(memory_dir=self.test_dir)
        self.user_id = "test_user"

        # Add test conversations
        self.test_conversations = [
            ("Hello!", "Hi! How can I help you?"),
            ("What's Python?", "Python is a programming language."),
            ("Tell me about AI", "AI is artificial intelligence."),
        ]

        for user_msg, bot_msg in self.test_conversations:
            self.memory.add_conversation(self.user_id, user_msg, bot_msg, metadata={"test": True})

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_export_to_json(self):
        """Test JSON export"""
        print("\n🧪 TEST 1: JSON Export")

        exporter = DataExporter(self.memory)
        output_file = os.path.join(self.test_dir, "export.json")

        result = exporter.export_to_json(self.user_id, output_file)

        # Verify export
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)
        self.assertTrue(os.path.exists(output_file))

        # Verify content
        with open(output_file, "r") as f:
            data = json.load(f)

        self.assertEqual(data["user_id"], self.user_id)
        self.assertEqual(len(data["conversations"]), 3)
        self.assertIn("export_date", data)

        print(f"   ✅ Exported {result['conversations']} conversations")
        print(f"   ✅ File size: {result['size_bytes']} bytes")

    def test_import_from_json(self):
        """Test JSON import"""
        print("\n🧪 TEST 2: JSON Import")

        # Export first
        exporter = DataExporter(self.memory)
        export_file = os.path.join(self.test_dir, "export.json")
        exporter.export_to_json(self.user_id, export_file)

        # Create new memory manager
        new_memory = MemoryManager(memory_dir=os.path.join(self.test_dir, "import"))
        importer = DataImporter(new_memory)

        # Import
        result = importer.import_from_json(export_file, user_id="imported_user")

        # Verify import
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)

        # Verify data
        conversations = new_memory.get_recent_conversations("imported_user", 10)
        self.assertEqual(len(conversations), 3)

        print(f"   ✅ Imported {result['conversations']} conversations")
        print(f"   ✅ Data integrity: OK")

    def test_export_to_csv(self):
        """Test CSV export"""
        print("\n🧪 TEST 3: CSV Export")

        exporter = DataExporter(self.memory)
        output_file = os.path.join(self.test_dir, "export.csv")

        result = exporter.export_to_csv(self.user_id, output_file)

        # Verify export
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)
        self.assertTrue(os.path.exists(output_file))

        # Verify content
        with open(output_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)
        self.assertIn("timestamp", rows[0])
        self.assertIn("user_message", rows[0])

        print(f"   ✅ Exported {result['conversations']} conversations to CSV")
        print(f"   ✅ File size: {result['size_bytes']} bytes")

    def test_import_from_csv(self):
        """Test CSV import"""
        print("\n🧪 TEST 4: CSV Import")

        # Export first
        exporter = DataExporter(self.memory)
        export_file = os.path.join(self.test_dir, "export.csv")
        exporter.export_to_csv(self.user_id, export_file)

        # Create new memory manager
        new_memory = MemoryManager(memory_dir=os.path.join(self.test_dir, "csv_import"))
        importer = DataImporter(new_memory)

        # Import
        result = importer.import_from_csv(export_file, user_id="csv_user")

        # Verify import
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)

        # Verify data
        conversations = new_memory.get_recent_conversations("csv_user", 10)
        self.assertEqual(len(conversations), 3)

        print(f"   ✅ Imported {result['conversations']} conversations from CSV")

    def test_export_to_sqlite(self):
        """Test SQLite export"""
        print("\n🧪 TEST 5: SQLite Export")

        exporter = DataExporter(self.memory)
        db_file = os.path.join(self.test_dir, "export.db")

        result = exporter.export_to_sqlite(self.user_id, db_file)

        # Verify export
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)
        self.assertTrue(os.path.exists(db_file))

        # Verify database content
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (self.user_id,))
        count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count, 3)

        print(f"   ✅ Exported {result['conversations']} conversations to SQLite")
        print(f"   ✅ Database size: {result['size_bytes']} bytes")

    def test_import_from_sqlite(self):
        """Test SQLite import"""
        print("\n🧪 TEST 6: SQLite Import")

        # Export first
        exporter = DataExporter(self.memory)
        export_db = os.path.join(self.test_dir, "export.db")
        exporter.export_to_sqlite(self.user_id, export_db)

        # Create new memory manager
        new_memory = MemoryManager(memory_dir=os.path.join(self.test_dir, "sqlite_import"))
        importer = DataImporter(new_memory)

        # Import
        result = importer.import_from_sqlite(export_db, user_id=self.user_id)

        # Verify import
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)

        # Verify data
        conversations = new_memory.get_recent_conversations(self.user_id, 10)
        self.assertEqual(len(conversations), 3)

        print(f"   ✅ Imported {result['conversations']} conversations from SQLite")

    def test_json_roundtrip(self):
        """Test complete JSON export-import cycle"""
        print("\n🧪 TEST 7: JSON Roundtrip (Export → Import)")

        # Export
        exporter = DataExporter(self.memory)
        export_file = os.path.join(self.test_dir, "roundtrip.json")
        export_result = exporter.export_to_json(self.user_id, export_file)

        # Import to new memory
        new_memory = MemoryManager(memory_dir=os.path.join(self.test_dir, "roundtrip"))
        importer = DataImporter(new_memory)
        import_result = importer.import_from_json(export_file)

        # Verify
        self.assertTrue(export_result["success"])
        self.assertTrue(import_result["success"])

        # Compare original and imported data
        original = self.memory.get_recent_conversations(self.user_id, 10)
        imported = new_memory.get_recent_conversations(self.user_id, 10)

        self.assertEqual(len(original), len(imported))

        for orig, imp in zip(original, imported):
            self.assertEqual(orig["user_message"], imp["user_message"])
            self.assertEqual(orig["bot_response"], imp["bot_response"])

        print(f"   ✅ Roundtrip successful: {len(original)} conversations")
        print(f"   ✅ Data integrity: 100%")

    def test_sql_memory_export(self):
        """Test export with SQLMemoryManager"""
        print("\n🧪 TEST 8: SQL Memory Manager Export")

        # Create SQL memory manager
        db_path = os.path.join(self.test_dir, "sql_test.db")
        sql_memory = SQLMemoryManager(db_path)

        # Add test data
        for user_msg, bot_msg in self.test_conversations:
            sql_memory.add_conversation(
                "sql_user", user_msg, bot_msg, metadata={"source": "sql_test"}
            )

        # Export
        exporter = DataExporter(sql_memory)
        export_file = os.path.join(self.test_dir, "sql_export.json")
        result = exporter.export_to_json("sql_user", export_file)

        # Close SQL connection before cleanup
        sql_memory.close()

        # Verify
        self.assertTrue(result["success"])
        self.assertEqual(result["conversations"], 3)

        print(f"   ✅ SQL memory export: {result['conversations']} conversations")

    def test_error_handling(self):
        """Test error handling"""
        print("\n🧪 TEST 9: Error Handling")

        exporter = DataExporter(self.memory)
        importer = DataImporter(self.memory)

        # Test import from non-existent file
        result = importer.import_from_json("/non/existent/file.json")
        self.assertFalse(result["success"])
        print("   ✅ Missing import file handled")

        # Test import from invalid SQLite file
        result = importer.import_from_sqlite("/fake/database.db", self.user_id)
        self.assertFalse(result["success"])
        print("   ✅ Invalid database handled")

        print("   ✅ Error handling works correctly")


class TestMultiDatabaseSupport(unittest.TestCase):
    """Test PostgreSQL and MongoDB support (if available)"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.memory = MemoryManager(memory_dir=self.test_dir)
        self.user_id = "db_test_user"

        # Add test data
        for i in range(5):
            self.memory.add_conversation(
                self.user_id, f"Question {i+1}", f"Answer {i+1}", metadata={"index": i}
            )

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)

    def test_postgresql_support(self):
        """Test PostgreSQL export (if psycopg2 available)"""
        print("\n🧪 TEST 10: PostgreSQL Support")

        try:
            import psycopg2

            print("   ℹ️  psycopg2 installed - testing PostgreSQL")

            exporter = DataExporter(self.memory)

            # Note: This would need actual PostgreSQL connection
            # Just test the method exists and handles missing connection gracefully
            result = exporter.export_to_postgresql(
                self.user_id, "postgresql://invalid:invalid@localhost/test"
            )

            self.assertIn("success", result)
            print("   ✅ PostgreSQL export method available")

        except ImportError:
            print("   ⚠️  psycopg2 not installed - skipping PostgreSQL test")
            print("   💡 Install: pip install psycopg2-binary")

    def test_mongodb_support(self):
        """Test MongoDB export (if pymongo available)"""
        print("\n🧪 TEST 11: MongoDB Support")

        try:
            import pymongo

            print("   ℹ️  pymongo installed - testing MongoDB")

            exporter = DataExporter(self.memory)

            # Note: This would need actual MongoDB connection
            # Just test the method exists and handles missing connection gracefully
            result = exporter.export_to_mongodb(self.user_id, "mongodb://invalid:27017/")

            self.assertIn("success", result)
            print("   ✅ MongoDB export method available")

        except ImportError:
            print("   ⚠️  pymongo not installed - skipping MongoDB test")
            print("   💡 Install: pip install pymongo")


def run_tests():
    """Run all tests with nice output"""
    print("\n" + "=" * 70)
    print("DATA EXPORT/IMPORT TEST SUITE")
    print("=" * 70)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestDataExportImport))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiDatabaseSupport))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")

    print("=" * 70 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
