"""
Example 08: Conversation Summarization
=======================================
Summarize conversations to save tokens.
"""

from mem_llm import MemAgent, ConversationSummarizer

print("\n" + "="*50)
print("CONVERSATION SUMMARIZATION")
print("="*50 + "\n")

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

for msg in messages:
    agent.chat(msg)
    print(f"Chat: {msg}")

# Get and summarize conversations
conversations = agent.memory.get_recent_conversations("alice", 10)
print(f"\nSaved: {len(conversations)} conversations")

summarizer = ConversationSummarizer(agent.llm)
summary = summarizer.summarize_conversations(conversations, user_id="alice")

print(f"\nSummary:\n{summary['summary']}")

# Show savings
original = "\n".join([f"{c['user_message']} {c['bot_response']}" for c in conversations])
stats = summarizer.get_summary_stats(original, summary['summary'])
print(f"\nToken savings: {stats['tokens_saved']} ({stats['compression_ratio']}% compression)")

print("\n" + "="*50 + "\n")
