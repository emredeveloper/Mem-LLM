"""
Example 15: Response Metrics & Quality Analytics (v1.3.1+)
===========================================================

Track response quality, confidence, latency, and KB usage.

Quick Usage:
    response = agent.chat("Hello!", return_metrics=True)
    print(f"Confidence: {response.confidence:.2%}")
    print(f"Latency: {response.latency:.0f}ms")
    
    metrics = agent.get_response_metrics()  # Get aggregated stats
"""

from mem_llm import MemAgent, ChatResponse

# Create agent
agent = MemAgent(model="granite4:tiny-h", use_sql=False)
agent.set_user("alice")

print("=" * 60)
print("1. Basic Metrics")
print("=" * 60)

# Normal chat (returns string)
response_text = agent.chat("Hello, I'm Alice!")
print(f"Response: {response_text}\n")

# Chat with metrics (returns ChatResponse)
response_obj = agent.chat("What's your name?", return_metrics=True)
print(f"Confidence: {response_obj.confidence:.2%}")
print(f"Latency: {response_obj.latency:.0f}ms")
print(f"Source: {response_obj.source}")
print(f"Quality: {response_obj.get_quality_label()}\n")

print("=" * 60)
print("2. Analytics Dashboard")
print("=" * 60)

# Generate some interactions
queries = [
    "Hi, I'm looking for Python help",
    "How do I install packages?",
    "What's a virtual environment?",
    "My favorite food is pizza",
    "I live in Istanbul"
]

for query in queries:
    agent.chat(query)

# Get aggregated metrics
metrics = agent.get_response_metrics()
print(f"Total Responses: {metrics['total_responses']}")
print(f"Avg Latency: {metrics['avg_latency_ms']:.1f}ms")
print(f"Avg Confidence: {metrics['avg_confidence']:.2%}")
print(f"KB Usage Rate: {metrics['kb_usage_rate']:.1%}")

# Show profile summary
profile = agent.get_user_profile()
summary = profile.get('summary', {})
if summary:
    print(f"\nUser Summary:")
    print(f"  • Interactions: {summary.get('total_interactions', 0)}")
    print(f"  • Topics: {', '.join(summary.get('topics_of_interest', [])[:3])}")
    print(f"  • Engagement: {summary.get('engagement_level', 'N/A')}")

print("\n" + "=" * 60)
print("3. Export Metrics")
print("=" * 60)

# Export as JSON
json_export = agent.export_metrics(format="json")
print(f"JSON (first 200 chars):\n{json_export[:200]}...")

# Export as summary
summary_export = agent.export_metrics(format="summary")
print(f"\nSummary Format:\n{summary_export}")

print("\n" + "=" * 60)
print("✅ Complete!")
print("=" * 60)
