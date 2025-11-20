"""
Quickstart: Conversation Analytics (v2.1.4)
===========================================
Analyze user engagement, topics, and activity patterns.
"""

from mem_llm import ConversationAnalytics, MemAgent

print("📊 Conversation Analytics Demo\n")

# Create agent with JSON backend (Analytics requires JSON)
agent = MemAgent(use_sql=False)
agent.set_user("demo_user")

print("💬 Having some conversations...")
# Simulate conversations
agent.chat("Hello! I'm learning Python programming.")
agent.chat("Can you help me understand data structures?")
agent.chat("I love working with lists and dictionaries.")
agent.chat("What about machine learning?")

# Initialize analytics
analytics = ConversationAnalytics(agent.memory)

# 1. Get conversation statistics
print("\n📈 Statistics:")
stats = analytics.get_conversation_stats("demo_user")
print(f"   Total messages: {stats['total_messages']}")
print(f"   Average length: {stats['avg_message_length']} chars")

# 2. Analyze topics
print("\n🏷️  Topics discussed:")
topics = analytics.get_topic_distribution("demo_user")
for topic, count in list(topics.items())[:5]:  # Show top 5
    print(f"   - {topic}: {count}")

# 3. Engagement metrics
print("\n🎯 Engagement:")
engagement = analytics.get_engagement_metrics("demo_user")
print(f"   Score: {engagement['engagement_score']}")
print(f"   Active days: {engagement['active_days']}")

print("\n✅ Analytics complete!")
