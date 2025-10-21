"""
Example 08: Conversation Summarization
======================================

Automatically summarize long conversation histories to save tokens and improve context.

Usage:
    python 08_conversation_summarization.py
"""

import sys
import logging
from pathlib import Path
 # No sys.path hack needed; use pip-installed mem-llm

# Suppress verbose logs
logging.getLogger('MemAgent').setLevel(logging.ERROR)
logging.getLogger('mem_llm').setLevel(logging.ERROR)

from mem_llm import MemAgent, ConversationSummarizer


print("\n" + "="*70)
print("CONVERSATION SUMMARIZATION - Simple Example")
print("="*70 + "\n")

# Create agent with SQL memory
print("1️⃣  Creating agent and having conversations...\n")
agent = MemAgent(model="granite4:tiny-h", use_sql=True)
agent.set_user("alice")

# Have some conversations
messages = [
    "Hi! I'm Alice, a Python developer from Seattle.",
    "I'm working on a machine learning project with scikit-learn.",
    "It's a customer churn prediction model using Random Forest.",
    "My accuracy is 78% but I want to improve it.",
    "I also enjoy hiking and photography in my free time."
]

print("💬 Chat History:")
for i, msg in enumerate(messages, 1):
    response = agent.chat(msg)
    print(f"   {i}. {msg}")

# Get conversations
conversations = agent.memory.get_recent_conversations("alice", 10)
print(f"\n✅ Saved {len(conversations)} conversations\n")

# Summarize
print("2️⃣  Generating summary...\n")
summarizer = ConversationSummarizer(agent.llm)
summary = summarizer.summarize_conversations(
    conversations,
    user_id="alice",
    include_facts=True
)

# Show results
print("📝 SUMMARY:")
print("-" * 70)
print(summary['summary'])
print("-" * 70)

if summary.get('key_facts'):
    print("\n🔑 KEY FACTS:")
    for fact in summary['key_facts'][:5]:  # Show max 5 facts
        print(f"   • {fact}")

# Show savings
original = "\n".join([f"{c['user_message']} {c['bot_response']}" for c in conversations])
stats = summarizer.get_summary_stats(original, summary['summary'])

print(f"\n� TOKEN SAVINGS:")
print(f"   Before: ~{stats['original_tokens_est']} tokens")
print(f"   After:  ~{stats['summary_tokens_est']} tokens")
print(f"   Saved:  ~{stats['tokens_saved']} tokens ({stats['compression_ratio']}% compression)")

print("\n" + "="*70)
print("✅ Done! Use summaries instead of full chat history to save tokens.")
print("="*70 + "\n")
