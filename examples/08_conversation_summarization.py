"""
Example 8: Conversation Summarization
=======================================

Summarize long conversations to save tokens.

Quick Usage:
    summarizer = ConversationSummarizer(agent.llm)
    summary = summarizer.summarize_conversations(conversations, user_id="alice")
"""

from mem_llm import MemAgent, ConversationSummarizer

print("=" * 60)
print("Conversation Summarization")
print("=" * 60)

# Create agent and chat
agent = MemAgent(model="granite4:tiny-h", use_sql=True)
agent.set_user("alice")

messages = [
    "Hi! I'm Alice, a Python developer from Seattle.",
    "I'm working on a machine learning project.",
    "It's a customer churn prediction model.",
    "My accuracy is 78% but I want to improve it.",
    "I also enjoy hiking and photography."
]

print("\n💬 Conversation:")
for msg in messages:
    print(f"  User: {msg}")
    agent.chat(msg)

# Get conversations
conversations = agent.memory.get_recent_conversations("alice", 10)
print(f"\n📊 Saved: {len(conversations)} conversations")

# Summarize
print("\n📝 Summarizing...")
summarizer = ConversationSummarizer(agent.llm)
summary = summarizer.summarize_conversations(conversations, user_id="alice")

print(f"\nSummary:\n{summary['summary']}")

# Show savings
original = "\n".join([f"{c['user_message']} {c['bot_response']}" for c in conversations])
stats = summarizer.get_summary_stats(original, summary['summary'])
print(f"\n💾 Token savings: {stats['tokens_saved']} ({stats['compression_ratio']}% compression)")

print("\n" + "=" * 60)
