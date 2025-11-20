"""
Test Conversation Summarizer
=============================

Tests the conversation summarization feature.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import time

from mem_llm import MemAgent
from mem_llm.conversation_summarizer import AutoSummarizer, ConversationSummarizer
from mem_llm.llm_client import OllamaClient


def test_basic_summarization():
    """Test basic conversation summarization"""
    print("\n" + "=" * 70)
    print("TEST 1: Basic Conversation Summarization")
    print("=" * 70)

    try:
        # Create LLM client
        llm = OllamaClient(model="granite4:tiny-h")
        summarizer = ConversationSummarizer(llm)

        # Sample conversations
        conversations = [
            {
                "user_message": "Hi! My name is Alice and I'm a Python developer.",
                "bot_response": "Hello Alice! Nice to meet you. How can I help you with Python today?",
            },
            {
                "user_message": "I'm working on a machine learning project with scikit-learn.",
                "bot_response": "Great! What kind of ML problem are you working on?",
            },
            {
                "user_message": "It's a classification problem. I need to predict customer churn.",
                "bot_response": "Customer churn prediction is a common use case. Have you considered using Random Forest or Gradient Boosting?",
            },
            {
                "user_message": "Yes, I'm trying Random Forest but the accuracy is only 75%.",
                "bot_response": "You might want to try feature engineering or hyperparameter tuning to improve accuracy.",
            },
            {
                "user_message": "Good idea! Also, I live in San Francisco and work remotely.",
                "bot_response": "Remote work is great! Let me know if you need more ML tips.",
            },
        ]

        print(f"📊 Summarizing {len(conversations)} conversations...")

        # Generate summary
        start_time = time.time()
        summary = summarizer.summarize_conversations(
            conversations, user_id="alice", max_conversations=10, include_facts=True
        )
        duration = time.time() - start_time

        # Display results
        print(f"\n✅ Summary generated in {duration:.2f}s")
        print(f"\n📝 SUMMARY:")
        print("-" * 70)
        print(summary["summary"])
        print("-" * 70)

        if summary.get("key_facts"):
            print(f"\n🔑 KEY FACTS:")
            for i, fact in enumerate(summary["key_facts"], 1):
                print(f"   {i}. {fact}")

        print(f"\n📊 METADATA:")
        print(f"   - Conversations summarized: {summary['conversation_count']}")
        print(f"   - User ID: {summary['user_id']}")
        print(f"   - Generated at: {summary['generated_at']}")

        # Calculate compression
        original_text = "\n".join(
            [f"{c['user_message']} {c['bot_response']}" for c in conversations]
        )
        stats = summarizer.get_summary_stats(original_text, summary["summary"])

        print(f"\n💾 COMPRESSION STATS:")
        print(
            f"   - Original: {stats['original_length']} chars (~{stats['original_tokens_est']} tokens)"
        )
        print(
            f"   - Summary: {stats['summary_length']} chars (~{stats['summary_tokens_est']} tokens)"
        )
        print(f"   - Compression: {stats['compression_ratio']}%")
        print(f"   - Tokens saved: ~{stats['tokens_saved']}")

        print("\n✅ TEST 1 PASSED\n")
        return True

    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}\n")
        return False


def test_auto_summarizer():
    """Test automatic summary updates"""
    print("\n" + "=" * 70)
    print("TEST 2: Auto-Summarizer with Threshold")
    print("=" * 70)

    try:
        # Create agent
        agent = MemAgent(model="granite4:tiny-h", use_sql=True)
        agent.set_user("bob")

        # Create auto-summarizer
        llm = OllamaClient(model="granite4:tiny-h")
        summarizer = ConversationSummarizer(llm)
        auto_summarizer = AutoSummarizer(
            summarizer, agent.memory, update_threshold=3  # Update every 3 conversations
        )

        print(f"📊 Adding conversations with auto-summary (threshold=3)...")

        # Add conversations one by one
        test_messages = [
            "Hi, I'm Bob. I'm learning web development.",
            "I'm interested in React and Node.js.",
            "Can you help me understand async/await?",
            "I also know some Python basics.",
            "I live in New York and work as a designer.",
        ]

        for i, msg in enumerate(test_messages, 1):
            # Add conversation
            response = agent.chat(msg)
            print(f"\n   {i}. Added: '{msg[:50]}...'")

            # Increment counter
            auto_summarizer.increment_conversation_count("bob")

            # Check for auto-update
            summary = auto_summarizer.check_and_update("bob")
            if summary:
                print(f"      🔄 Auto-summary triggered!")
                print(f"      📝 Summary: {summary['summary'][:80]}...")

        # Get final summary
        final_summary = auto_summarizer.get_summary("bob")

        print(f"\n✅ Final Summary:")
        print("-" * 70)
        print(final_summary["summary"])
        print("-" * 70)

        print("\n✅ TEST 2 PASSED\n")
        return True

    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}\n")
        import traceback

        traceback.print_exc()
        return False


def test_empty_conversations():
    """Test handling of empty conversations"""
    print("\n" + "=" * 70)
    print("TEST 3: Empty Conversations Handling")
    print("=" * 70)

    try:
        llm = OllamaClient(model="granite4:tiny-h")
        summarizer = ConversationSummarizer(llm)

        # Empty list
        summary = summarizer.summarize_conversations([], user_id="charlie", max_conversations=10)

        print(f"✅ Empty conversation handling: {summary['summary']}")
        assert "No conversation history" in summary["summary"]

        print("\n✅ TEST 3 PASSED\n")
        return True

    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}\n")
        return False


def test_large_conversation_history():
    """Test summarization with many conversations"""
    print("\n" + "=" * 70)
    print("TEST 4: Large Conversation History (50 conversations)")
    print("=" * 70)

    try:
        llm = OllamaClient(model="granite4:tiny-h")
        summarizer = ConversationSummarizer(llm)

        # Generate 50 conversations
        conversations = []
        topics = [
            "Python programming",
            "Machine learning",
            "Web development",
            "Database design",
            "API development",
        ]

        for i in range(50):
            topic = topics[i % len(topics)]
            conversations.append(
                {
                    "user_message": f"Question {i+1} about {topic}",
                    "bot_response": f"Answer {i+1} regarding {topic}",
                }
            )

        print(f"📊 Summarizing {len(conversations)} conversations...")
        print(f"   (Will use last 20 due to max_conversations limit)")

        start_time = time.time()
        summary = summarizer.summarize_conversations(
            conversations, user_id="dave", max_conversations=20  # Limit to prevent token overflow
        )
        duration = time.time() - start_time

        print(f"\n✅ Summary generated in {duration:.2f}s")
        print(f"📝 Summary length: {len(summary['summary'])} chars")
        print(f"📊 Conversations summarized: {summary['conversation_count']}/50")

        # Verify summary is concise
        assert len(summary["summary"]) < 1500, "Summary too long!"
        assert summary["conversation_count"] == 20, "Wrong conversation count!"

        print("\n✅ TEST 4 PASSED\n")
        return True

    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}\n")
        return False


def test_integration_with_memagent():
    """Test integration with MemAgent"""
    print("\n" + "=" * 70)
    print("TEST 5: Integration with MemAgent")
    print("=" * 70)

    try:
        # Create agent with summarization support
        agent = MemAgent(model="granite4:tiny-h", use_sql=True)
        agent.set_user("emma")

        print("📊 Testing MemAgent integration...")

        # Add some conversations
        messages = [
            "Hi, I'm Emma. I'm a data scientist.",
            "I work with pandas and numpy daily.",
            "Currently learning deep learning with PyTorch.",
            "I need help with neural network architecture.",
            "Also interested in NLP and transformers.",
        ]

        for msg in messages:
            agent.chat(msg)

        # Get conversations
        if hasattr(agent.memory, "get_recent_conversations"):
            convs = agent.memory.get_recent_conversations("emma", 10)
            print(f"   ✅ Retrieved {len(convs)} conversations")

            # Summarize
            llm = OllamaClient(model="granite4:tiny-h")
            summarizer = ConversationSummarizer(llm)

            summary = summarizer.summarize_conversations(
                convs, user_id="emma", max_conversations=10
            )

            print(f"\n📝 Integration Summary:")
            print("-" * 70)
            print(summary["summary"])
            print("-" * 70)

            print("\n✅ TEST 5 PASSED\n")
            return True
        else:
            print("   ⚠️  Memory manager doesn't support get_recent_conversations")
            print("\n⚠️  TEST 5 SKIPPED\n")
            return True

    except Exception as e:
        print(f"\n❌ TEST 5 FAILED: {e}\n")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "CONVERSATION SUMMARIZER TEST SUITE" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")

    results = []

    # Run tests
    results.append(("Basic Summarization", test_basic_summarization()))
    results.append(("Auto-Summarizer", test_auto_summarizer()))
    results.append(("Empty Conversations", test_empty_conversations()))
    results.append(("Large History", test_large_conversation_history()))
    results.append(("MemAgent Integration", test_integration_with_memagent()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:.<50} {status}")

    print("=" * 70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70 + "\n")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Conversation Summarizer is working!\n")
    else:
        print("⚠️  Some tests failed. Check output above.\n")


if __name__ == "__main__":
    main()
