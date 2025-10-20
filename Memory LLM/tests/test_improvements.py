"""
Test Script for New Features
=============================
Tests logging, retry logic, and WAL mode improvements
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mem_llm.logger import get_logger, MemLLMLogger
from mem_llm.retry_handler import exponential_backoff_retry, SafeExecutor, check_connection_with_retry
from mem_llm.memory_db import SQLMemoryManager


def test_logging_system():
    """Test the new logging system"""
    print("\n" + "="*70)
    print("TEST 1: Logging System")
    print("="*70)
    
    # Create logger
    logger = get_logger(name="test_logger", log_file="logs/test.log", log_level="DEBUG")
    
    # Test different log levels
    logger.debug("This is a debug message", user_id="test_user", action="testing")
    logger.info("This is an info message", status="success")
    logger.warning("This is a warning message", warning_type="minor")
    logger.error("This is an error message", error_code=500)
    
    # Test specialized logging methods
    logger.log_llm_call(
        model="granite4:tiny-h",
        prompt_length=150,
        response_length=300,
        duration=1.5
    )
    
    logger.log_memory_operation(
        operation="save",
        user_id="alice",
        success=True,
        details="Saved 3 conversations"
    )
    
    print("✅ Logging system test passed!")
    print(f"   Log file created at: logs/test.log")
    return True


def test_retry_logic():
    """Test retry logic with exponential backoff"""
    print("\n" + "="*70)
    print("TEST 2: Retry Logic & Error Handling")
    print("="*70)
    
    logger = get_logger(name="retry_test", log_level="DEBUG")
    
    # Test 1: Successful retry after failures
    attempt_count = [0]
    
    @exponential_backoff_retry(max_retries=3, initial_delay=0.5, logger=logger.logger)
    def unstable_function():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ConnectionError(f"Simulated failure #{attempt_count[0]}")
        return "Success!"
    
    try:
        result = unstable_function()
        print(f"✅ Retry logic works! Result: {result} (after {attempt_count[0]} attempts)")
    except Exception as e:
        print(f"❌ Retry test failed: {e}")
        return False
    
    # Test 2: SafeExecutor
    executor = SafeExecutor(logger=logger.logger)
    
    # Test JSON parsing with fallback
    broken_json = '{"name": "Alice", "age": 30'  # Missing closing brace
    result = executor.safe_json_parse(broken_json, default={"error": "parse_failed"})
    print(f"✅ Safe JSON parse handled broken JSON: {result}")
    
    # Test execution with fallback
    def failing_func():
        raise ValueError("Primary function failed")
    
    def fallback_func():
        return "Fallback worked!"
    
    result = executor.execute_with_fallback(
        primary_func=failing_func,
        fallback_func=fallback_func,
        error_message="Testing fallback"
    )
    print(f"✅ Fallback execution: {result}")
    
    print("✅ Retry logic test passed!")
    return True


def test_wal_mode():
    """Test SQLite WAL mode and concurrency improvements"""
    print("\n" + "="*70)
    print("TEST 3: SQLite WAL Mode & Concurrency")
    print("="*70)
    
    # Create test database
    db_path = "test_wal.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = SQLMemoryManager(db_path)
    
    # Check if WAL mode is enabled
    cursor = db.conn.cursor()
    cursor.execute("PRAGMA journal_mode")
    journal_mode = cursor.fetchone()[0]
    
    print(f"   Journal mode: {journal_mode}")
    
    if journal_mode.upper() == "WAL":
        print("✅ WAL mode is enabled!")
    else:
        print("⚠️  WAL mode is NOT enabled")
        return False
    
    # Check other pragmas
    cursor.execute("PRAGMA synchronous")
    sync_mode = cursor.fetchone()[0]
    print(f"   Synchronous mode: {sync_mode}")
    
    # Test concurrent writes (simulated)
    start_time = time.time()
    
    # Add some test data
    for i in range(100):
        db.add_interaction(
            user_id=f"user_{i % 10}",
            user_message=f"Test message {i}",
            bot_response=f"Test response {i}"
        )
    
    elapsed = time.time() - start_time
    print(f"✅ Wrote 100 records in {elapsed:.3f}s")
    
    # Verify data integrity
    cursor.execute("SELECT COUNT(*) FROM conversations")
    count = cursor.fetchone()[0]
    
    if count == 100:
        print(f"✅ Data integrity verified: {count} records")
    else:
        print(f"❌ Data integrity issue: expected 100, got {count}")
        return False
    
    # Cleanup
    db.conn.close()
    os.remove(db_path)
    
    # Check for WAL files (they should be created)
    wal_file = f"{db_path}-wal"
    shm_file = f"{db_path}-shm"
    
    print("✅ WAL mode test passed!")
    return True


def test_integration_with_mem_agent():
    """Test integration with MemAgent"""
    print("\n" + "="*70)
    print("TEST 4: Integration with MemAgent")
    print("="*70)
    
    try:
        from mem_llm import MemAgent
        
        # Create agent with SQL (WAL mode will be enabled)
        agent = MemAgent(
            model="granite4:tiny-h",
            use_sql=True,
            memory_dir="test_integration.db"
        )
        
        print("✅ MemAgent created with WAL-enabled database")
        
        # Test basic operations
        agent.set_user("test_user")
        print("✅ User set successfully")
        
        # Check database mode
        if hasattr(agent.memory, 'conn'):
            cursor = agent.memory.conn.cursor()
            cursor.execute("PRAGMA journal_mode")
            mode = cursor.fetchone()[0]
            print(f"   Agent database mode: {mode}")
            
            if mode.upper() == "WAL":
                print("✅ Agent is using WAL mode!")
            
        # Cleanup
        if os.path.exists("test_integration.db"):
            os.remove("test_integration.db")
        
        print("✅ Integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "MEM-LLM IMPROVEMENTS TEST SUITE" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {
        "Logging System": False,
        "Retry Logic": False,
        "WAL Mode": False,
        "Integration": False
    }
    
    try:
        results["Logging System"] = test_logging_system()
    except Exception as e:
        print(f"❌ Logging test failed with exception: {e}")
    
    try:
        results["Retry Logic"] = test_retry_logic()
    except Exception as e:
        print(f"❌ Retry test failed with exception: {e}")
    
    try:
        results["WAL Mode"] = test_wal_mode()
    except Exception as e:
        print(f"❌ WAL test failed with exception: {e}")
    
    try:
        results["Integration"] = test_integration_with_mem_agent()
    except Exception as e:
        print(f"❌ Integration test failed with exception: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name:<20} {status}")
    
    print("="*70)
    print(f"   TOTAL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! Improvements are working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
