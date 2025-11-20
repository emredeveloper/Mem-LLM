"""
COMPREHENSIVE TEST SUITE
========================
Tests all features of mem-llm package
"""

import json
import os
import sys
import time
from pathlib import Path

import pytest


# Color codes for better output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


# Default model used across tests (can be overridden via environment variable)
DEFAULT_MODEL = os.environ.get("MEM_LLM_TEST_MODEL", "granite4:tiny-h")

# Test results
test_results = {"passed": 0, "failed": 0, "warnings": 0, "details": []}


def ensure_ollama_available(agent, require_model=True):
    """Skip the calling test if Ollama or the target model is unavailable."""
    status = agent.check_setup()

    if not status.get("ollama_running"):
        print_warning("Ollama is not running - skipping test")
        pytest.skip("Ollama service is not running")

    if require_model and not status.get("model_ready"):
        print_warning(f"Model {status.get('target_model')} not found")
        available = status.get("available_models")
        if available:
            print_info(f"Available models: {available}")
        pytest.skip(f"Model {status.get('target_model')} is not available")

    return status


def run_test(name, func):
    """Run a single test"""
    try:
        print(f"\n{Colors.BOLD}TEST: {name}{Colors.END}")
        print("-" * 60)
        func()
        print_success(f"PASSED: {name}")
        test_results["passed"] += 1
        test_results["details"].append({"name": name, "status": "PASSED"})
        return True
    except AssertionError as e:
        print_error(f"FAILED: {name}")
        print_error(f"  Reason: {str(e)}")
        test_results["failed"] += 1
        test_results["details"].append({"name": name, "status": "FAILED", "error": str(e)})
        return False
    except Exception as e:
        print_error(f"ERROR: {name}")
        print_error(f"  Exception: {str(e)}")
        test_results["failed"] += 1
        test_results["details"].append({"name": name, "status": "ERROR", "error": str(e)})
        return False


# =============================================================================
# IMPORT TESTS
# =============================================================================


def test_imports():
    """Test if all modules can be imported"""
    global MemAgent, MemoryManager, OllamaClient, SQLMemoryManager

    from mem_llm import MemAgent

    print_success("MemAgent imported")

    from mem_llm import MemoryManager

    print_success("MemoryManager imported")

    from mem_llm import OllamaClient

    print_success("OllamaClient imported")

    try:
        from mem_llm import SQLMemoryManager

        print_success("SQLMemoryManager imported")
    except ImportError:
        print_warning("SQLMemoryManager not available (optional)")

    try:
        from mem_llm import MemoryTools, ToolExecutor

        print_success("Memory Tools imported")
    except ImportError:
        print_warning("Memory Tools not available (optional)")


# =============================================================================
# CORE FUNCTIONALITY TESTS
# =============================================================================


def test_agent_creation_json():
    """Test creating agent with JSON memory"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=False, memory_dir="test_json_mem")
    assert agent is not None, "Agent creation failed"
    assert agent.current_user is None, "Current user should be None initially"
    print_success("Agent created with JSON memory")


def test_agent_creation_sql():
    """Test creating agent with SQL memory"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=True, memory_dir="test_sql.db")
    assert agent is not None, "Agent creation failed"
    assert hasattr(agent.memory, "add_knowledge"), "SQL memory should have add_knowledge"
    print_success("Agent created with SQL memory")


def test_ollama_connection():
    """Test Ollama connection"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=False)
    status = ensure_ollama_available(agent, require_model=False)

    print_success("Ollama is running")

    if status["model_ready"]:
        print_success(f"Model {status['target_model']} is ready")
    else:
        print_warning(f"Model {status['target_model']} not found")
        available = status.get("available_models")
        if available:
            print_info(f"Available models: {available}")
        pytest.skip(f"Model {status['target_model']} is not available")


def test_user_management():
    """Test user management"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=False, memory_dir="test_user_mgmt")

    # Set user
    agent.set_user("test_user_1", name="Test User")
    assert agent.current_user == "test_user_1", "User not set correctly"
    print_success("User set successfully")

    # Get profile
    profile = agent.get_user_profile("test_user_1")
    assert profile is not None, "Profile should exist"
    print_success(f"Profile retrieved: {profile}")


def test_basic_chat():
    """Test basic chat functionality"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=False, memory_dir="test_chat")
    agent.set_user("chat_user")

    # Check if Ollama is running
    ensure_ollama_available(agent)

    response = agent.chat("Hello, my name is Alice")
    assert response is not None, "Response should not be None"
    assert len(response) > 0, "Response should not be empty"
    print_success(f"Chat response received: {response[:50]}...")


def test_memory_persistence():
    """Test if memory is saved and loaded correctly"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=False, memory_dir="test_persistence")
    agent.set_user("persist_user")

    # Check if Ollama is running
    ensure_ollama_available(agent)

    # Add interaction
    agent.chat("My favorite color is blue")

    # Create new agent with same memory
    agent2 = MemAgent(model=DEFAULT_MODEL, use_sql=False, memory_dir="test_persistence")
    agent2.set_user("persist_user")

    # Check conversation history
    if hasattr(agent2.memory, "get_recent_conversations"):
        convs = agent2.memory.get_recent_conversations("persist_user", limit=10)
        assert len(convs) >= 1, "Conversation should be persisted"
        print_success(f"Memory persisted: {len(convs)} conversation(s)")


def test_knowledge_base_sql():
    """Test knowledge base functionality (SQL only)"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=True, memory_dir="test_kb.db")

    # Add knowledge
    kb_id = agent.add_knowledge(
        category="test",
        question="What is the capital of France?",
        answer="The capital of France is Paris.",
        keywords=["france", "capital", "paris"],
    )

    assert kb_id > 0, "Knowledge entry should be added"
    print_success(f"Knowledge added with ID: {kb_id}")

    # Search knowledge
    results = agent.memory.search_knowledge("capital france")
    assert len(results) > 0, "Knowledge search should return results"
    print_success(f"Knowledge search found {len(results)} result(s)")


def test_user_profile_extraction():
    """Test automatic user profile extraction"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=True, memory_dir="test_profile.db")
    agent.set_user("profile_user", name="John")

    # Check if Ollama is running
    ensure_ollama_available(agent)

    # Share personal info
    agent.chat("My name is John")
    time.sleep(0.5)
    agent.chat("My favorite food is pizza")
    time.sleep(0.5)
    agent.chat("I live in London")

    # Check profile
    profile = agent.get_user_profile("profile_user")
    print_info(f"Profile: {profile}")

    # At least name should be set
    assert profile.get("name") == "John", "Name should be extracted"
    print_success("User profile extraction working")


def test_statistics():
    """Test statistics gathering"""
    agent = MemAgent(model=DEFAULT_MODEL, use_sql=True, memory_dir="test_stats.db")
    agent.set_user("stats_user")

    # Check if Ollama is running
    ensure_ollama_available(agent)

    # Add some interactions
    agent.chat("Hello")
    agent.chat("How are you?")

    # Get statistics
    stats = agent.get_statistics()
    assert "total_users" in stats, "Statistics should have total_users"
    assert "total_interactions" in stats, "Statistics should have total_interactions"
    print_success(f"Statistics: {stats}")


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================


def main():
    print_header("MEM-LLM COMPREHENSIVE TEST SUITE")

    # Import tests
    run_test("Module Imports", test_imports)

    # Core functionality tests
    run_test("Agent Creation (JSON)", test_agent_creation_json)
    run_test("Agent Creation (SQL)", test_agent_creation_sql)
    run_test("Ollama Connection", test_ollama_connection)
    run_test("User Management", test_user_management)
    run_test("Basic Chat", test_basic_chat)
    run_test("Memory Persistence", test_memory_persistence)
    run_test("Knowledge Base (SQL)", test_knowledge_base_sql)
    run_test("User Profile Extraction", test_user_profile_extraction)
    run_test("Statistics", test_statistics)

    # Print summary
    print_header("TEST SUMMARY")
    print(f"{Colors.GREEN}Passed:  {test_results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed:  {test_results['failed']}{Colors.END}")
    print(f"{Colors.YELLOW}Warnings: {test_results['warnings']}{Colors.END}")

    total = test_results["passed"] + test_results["failed"]
    success_rate = (test_results["passed"] / total * 100) if total > 0 else 0

    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")

    # Save results
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    print_info("Results saved to test_results.json")

    # Return exit code
    return 0 if test_results["failed"] == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
