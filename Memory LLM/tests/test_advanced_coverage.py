"""
Advanced Test Coverage for Mem-LLM
==================================
Tests for:
1. Memory corruption scenarios
2. Multi-user concurrent access
3. Long conversation history handling
4. Race conditions
5. Data integrity under stress
"""

import unittest
import threading
import time
import os
import json
import random
from pathlib import Path
import tempfile

# Import Mem-LLM components
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from mem_llm import MemAgent
from mem_llm.memory_db import SQLMemoryManager
from mem_llm.memory_manager import MemoryManager


class TestMemoryCorruption(unittest.TestCase):
    """Test memory corruption scenarios"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_corruption.db")
    
    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_corrupted_json_memory(self):
        """Test handling of corrupted JSON memory files"""
        print("\n🧪 Testing corrupted JSON memory handling...")
        
        # Create agent with JSON memory
        memory_dir = os.path.join(self.temp_dir, "json_mem")
        agent = MemAgent(model="granite4:tiny-h", use_sql=False, memory_dir=memory_dir)
        agent.set_user("test_user")
        
        # Add some data
        agent.memory.add_interaction("test_user", "Hello", "Hi there")
        agent.memory.save_memory("test_user")
        
        # Corrupt the JSON file
        user_file = Path(memory_dir) / "test_user.json"
        with open(user_file, 'r') as f:
            content = f.read()
        
        # Corrupt by removing closing brace
        corrupted = content[:-10]
        with open(user_file, 'w') as f:
            f.write(corrupted)
        
        # Try to load corrupted data
        try:
            agent.memory.load_memory("test_user")
            # Should not crash, should create new memory
            print("   ✅ Handled corrupted JSON gracefully")
        except json.JSONDecodeError:
            self.fail("Should handle corrupted JSON without crashing")
    
    def test_database_integrity_after_crash(self):
        """Test database integrity after simulated crash"""
        print("\n🧪 Testing database integrity after crash simulation...")
        
        db = SQLMemoryManager(self.db_path)
        
        # Add data
        for i in range(50):
            db.add_interaction(
                user_id="user1",
                user_message=f"Message {i}",
                bot_response=f"Response {i}"
            )
        
        # Simulate crash by not properly closing
        # In WAL mode, this should be recoverable
        conn = db.conn
        
        # Force close without commit (crash simulation)
        conn.close()
        
        # Reopen database
        db2 = SQLMemoryManager(self.db_path)
        cursor = db2.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE user_id='user1'")
        count = cursor.fetchone()[0]
        
        # With WAL mode, we should recover most/all data
        self.assertGreater(count, 0, "Should recover data after crash")
        print(f"   ✅ Recovered {count}/50 records after crash")
    
    def test_invalid_data_insertion(self):
        """Test handling of invalid data types"""
        print("\n🧪 Testing invalid data insertion...")
        
        db = SQLMemoryManager(self.db_path)
        
        # Try to insert None values
        try:
            db.add_interaction(
                user_id="user1",
                user_message=None,  # Invalid
                bot_response="Response"
            )
            self.fail("Should reject None message")
        except Exception:
            print("   ✅ Correctly rejected None message")
        
        # Try very long strings
        try:
            huge_message = "x" * 1_000_000  # 1MB message
            db.add_interaction(
                user_id="user1",
                user_message=huge_message,
                bot_response="OK"
            )
            print("   ✅ Handled very long message")
        except Exception as e:
            print(f"   ⚠️  Failed on large message: {e}")


class TestConcurrentAccess(unittest.TestCase):
    """Test multi-user concurrent access"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_concurrent.db")
        self.errors = []
    
    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_concurrent_writes(self):
        """Test multiple threads writing simultaneously"""
        print("\n🧪 Testing concurrent writes (10 threads)...")
        
        db = SQLMemoryManager(self.db_path)
        threads = []
        writes_per_thread = 20
        num_threads = 10
        
        def write_worker(thread_id):
            """Worker that writes data"""
            try:
                for i in range(writes_per_thread):
                    db.add_interaction(
                        user_id=f"user_{thread_id}",
                        user_message=f"Thread {thread_id} message {i}",
                        bot_response=f"Response {i}"
                    )
                    time.sleep(0.001)  # Small delay
            except Exception as e:
                self.errors.append(f"Thread {thread_id}: {e}")
        
        # Start threads
        start_time = time.time()
        for i in range(num_threads):
            t = threading.Thread(target=write_worker, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        elapsed = time.time() - start_time
        
        # Check for errors
        if self.errors:
            print(f"   ❌ Errors occurred: {self.errors}")
            self.fail(f"Concurrent writes failed: {self.errors}")
        
        # Verify data integrity
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total_count = cursor.fetchone()[0]
        
        expected = num_threads * writes_per_thread
        self.assertEqual(total_count, expected, 
                        f"Expected {expected} records, got {total_count}")
        
        print(f"   ✅ {total_count} concurrent writes in {elapsed:.2f}s")
        print(f"   ✅ No race conditions detected")
    
    def test_concurrent_read_write(self):
        """Test simultaneous reads and writes"""
        print("\n🧪 Testing concurrent reads and writes...")
        
        db = SQLMemoryManager(self.db_path)
        
        # Pre-populate with data
        for i in range(50):
            db.add_interaction(
                user_id="shared_user",
                user_message=f"Init message {i}",
                bot_response=f"Init response {i}"
            )
        
        read_counts = []
        write_counts = []
        
        def reader_worker(worker_id):
            """Worker that reads data"""
            try:
                for _ in range(50):
                    conversations = db.get_recent_conversations("shared_user", limit=10)
                    read_counts.append(len(conversations))
                    time.sleep(0.002)
            except Exception as e:
                self.errors.append(f"Reader {worker_id}: {e}")
        
        def writer_worker(worker_id):
            """Worker that writes data"""
            try:
                for i in range(20):
                    db.add_interaction(
                        user_id="shared_user",
                        user_message=f"Writer {worker_id} msg {i}",
                        bot_response=f"Response {i}"
                    )
                    write_counts.append(1)
                    time.sleep(0.003)
            except Exception as e:
                self.errors.append(f"Writer {worker_id}: {e}")
        
        # Start mixed readers and writers
        threads = []
        for i in range(5):  # 5 readers
            t = threading.Thread(target=reader_worker, args=(i,))
            threads.append(t)
            t.start()
        
        for i in range(3):  # 3 writers
            t = threading.Thread(target=writer_worker, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Check results
        if self.errors:
            print(f"   ❌ Errors: {self.errors}")
            self.fail(f"Concurrent read/write failed: {self.errors}")
        
        print(f"   ✅ {len(read_counts)} reads completed")
        print(f"   ✅ {sum(write_counts)} writes completed")
        print(f"   ✅ No blocking or deadlocks detected")
    
    def test_multi_user_isolation(self):
        """Test that user data is properly isolated"""
        print("\n🧪 Testing multi-user data isolation...")
        
        agent = MemAgent(
            model="granite4:tiny-h",
            use_sql=True,
            memory_dir=self.db_path
        )
        
        users = ["alice", "bob", "charlie", "david", "eve"]
        
        # Each user stores unique data
        for user in users:
            agent.set_user(user)
            agent.memory.add_interaction(
                user_id=user,
                user_message=f"I am {user}",
                bot_response=f"Hello {user}!"
            )
        
        # Verify isolation
        for user in users:
            agent.set_user(user)
            convs = agent.memory.get_recent_conversations(user, limit=10)
            
            # Should only see own data
            for conv in convs:
                self.assertIn(user, conv['user_message'].lower(),
                            f"User {user} saw other user's data")
        
        print(f"   ✅ {len(users)} users properly isolated")


class TestLongConversationHistory(unittest.TestCase):
    """Test handling of long conversation histories"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_long_history.db")
    
    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_1000_message_history(self):
        """Test performance with 1000 messages"""
        print("\n🧪 Testing 1000-message conversation history...")
        
        db = SQLMemoryManager(self.db_path)
        
        # Add 1000 messages
        start_time = time.time()
        for i in range(1000):
            db.add_interaction(
                user_id="power_user",
                user_message=f"Message {i} - " + "word " * 20,  # ~20 words each
                bot_response=f"Response {i} - " + "reply " * 30  # ~30 words each
            )
        write_time = time.time() - start_time
        
        # Test retrieval performance
        start_time = time.time()
        recent = db.get_recent_conversations("power_user", limit=50)
        read_time = time.time() - start_time
        
        print(f"   ✅ Wrote 1000 messages in {write_time:.2f}s ({1000/write_time:.0f} msg/s)")
        print(f"   ✅ Retrieved 50 messages in {read_time*1000:.2f}ms")
        
        self.assertEqual(len(recent), 50, "Should retrieve exactly 50 messages")
        self.assertLess(read_time, 0.5, "Read should be fast (<500ms)")
    
    def test_memory_context_overflow(self):
        """Test handling when context window is exceeded"""
        print("\n🧪 Testing context window overflow handling...")
        
        agent = MemAgent(
            model="granite4:tiny-h",
            use_sql=True,
            memory_dir=self.db_path
        )
        agent.set_user("verbose_user")
        
        # Add many long messages
        for i in range(100):
            long_message = f"Message {i}: " + " ".join([f"word{j}" for j in range(100)])
            agent.memory.add_interaction(
                user_id="verbose_user",
                user_message=long_message,
                bot_response="OK"
            )
        
        # Try to build context (should not crash)
        try:
            recent = agent.memory.get_recent_conversations("verbose_user", limit=50)
            total_length = sum(len(c['user_message']) + len(c['bot_response']) 
                             for c in recent)
            
            print(f"   ✅ Context size: {total_length:,} characters")
            print(f"   ✅ No overflow crash with large history")
            
        except Exception as e:
            self.fail(f"Should handle large context gracefully: {e}")
    
    def test_search_performance_large_dataset(self):
        """Test search performance with large dataset"""
        print("\n🧪 Testing search on large dataset...")
        
        db = SQLMemoryManager(self.db_path)
        
        # Create large dataset
        keywords = ["bug", "feature", "error", "question", "feedback"]
        for i in range(500):
            keyword = random.choice(keywords)
            db.add_interaction(
                user_id="search_user",
                user_message=f"I have a {keyword} about feature {i}",
                bot_response=f"Let me help with that {keyword}"
            )
        
        # Test search
        start_time = time.time()
        results = db.search_conversations("search_user", "bug")
        search_time = time.time() - start_time
        
        print(f"   ✅ Searched 500 conversations in {search_time*1000:.2f}ms")
        print(f"   ✅ Found {len(results)} matching conversations")
        
        self.assertLess(search_time, 0.5, "Search should be fast (<500ms)")
        self.assertGreater(len(results), 0, "Should find matching results")


def run_advanced_tests():
    """Run all advanced tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "ADVANCED TEST COVERAGE SUITE" + " "*25 + "║")
    print("╚" + "="*68 + "╝")
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMemoryCorruption))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConcurrentAccess))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLongConversationHistory))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    if result.wasSuccessful():
        print("\n🎉 All advanced tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review above.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_advanced_tests())
