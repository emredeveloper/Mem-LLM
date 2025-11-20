"""
Demo for v2.1.4 Features: Conversation Analytics and Config Presets

This demo shows how to:
1. Use Config Presets to quickly initialize specialized agents
2. Generate conversation data
3. Analyze conversations using the new Analytics module
4. Export analytics reports
"""

import os
import sys
from datetime import datetime, timedelta

# Add project root to path to import mem_llm
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.join(parent_dir, "Memory LLM")
sys.path.append(project_root)

from mem_llm import ConfigPresets, ConversationAnalytics, MemAgent


def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_config_presets():
    print_header("1. Config Presets Demo")

    presets = ConfigPresets()
    print(f"Available presets: {', '.join(presets.list_presets())}")

    # 1. Create a Code Assistant Agent
    print("\nInitializing 'code_assistant' agent...")
    # Note: name and user_id are not direct init params, but we can set user_id later
    coder = MemAgent(
        preset="code_assistant",
    )
    coder.set_user("demo_user")

    print(f"Agent Preset: code_assistant")
    # Access config from preset_config as it's not stored on the LLM client instance
    print(f"Temperature: {coder.preset_config.get('temperature')}")
    print(f"Max Tokens: {coder.preset_config.get('max_tokens')}")
    print(f"System Prompt: {coder.current_system_prompt[:50]}...")

    # 2. Create a Creative Writer Agent
    print("\nInitializing 'creative_writer' agent...")
    writer = MemAgent(
        preset="creative_writer",
    )
    writer.set_user("demo_user")

    print(f"Agent Preset: creative_writer")
    print(f"Temperature: {writer.preset_config.get('temperature')}")

    # 3. Custom Preset
    print("\nCreating a custom preset 'pirate_bot'...")
    custom_config = {
        "temperature": 0.8,
        "max_tokens": 100,
        "system_prompt": "You are a pirate. Always speak like a pirate. Yarr!",
        "tools_enabled": False,
        "description": "A pirate bot",
    }
    presets.save_custom_preset("pirate_bot", custom_config)

    print("Initializing agent with custom 'pirate_bot' preset...")
    pirate = MemAgent(
        preset="pirate_bot",
    )
    pirate.set_user("demo_user")
    print(f"System Prompt: {pirate.current_system_prompt}")

    # Cleanup
    presets.delete_custom_preset("pirate_bot")
    print("Custom preset deleted.")


def demo_analytics():
    print_header("2. Conversation Analytics Demo")

    user_id = "analytics_demo_user"
    # Use JSON backend for analytics demo (ConversationAnalytics works with MemoryManager)
    agent = MemAgent(use_sql=False)
    agent.set_user(user_id)

    # Clear previous memory for this demo
    agent.memory.clear_memory(user_id)

    print("Generating sample conversation data...")

    # Simulate some conversations with timestamps
    conversations = [
        ("Hello, how are you?", "I'm doing well, thank you! How can I help you today?"),
        (
            "I need help with Python programming.",
            "Sure! Python is a great language. What specifically do you need help with?",
        ),
        (
            "How do I define a function?",
            "You can define a function using the `def` keyword. Here's an example:\n\n```python\ndef my_func():\n    pass\n```",
        ),
        (
            "Thanks! What about lists?",
            "Lists are mutable sequences in Python. You can create them with square brackets `[]`.",
        ),
        ("Tell me a joke.", "Why do programmers prefer dark mode? Because light attracts bugs!"),
        (
            "That's funny. Can you explain recursion?",
            "Recursion is when a function calls itself. It's useful for tree traversal and mathematical problems.",
        ),
        ("I'm tired, goodbye.", "Goodbye! Have a great rest."),
    ]

    # Manually inject conversations to simulate history
    # In a real app, you would just use agent.chat()
    memory_data = agent.memory.load_memory(user_id)

    base_time = datetime.now() - timedelta(days=2)

    for i, (user_msg, bot_msg) in enumerate(conversations):
        # Spread conversations over time
        timestamp = base_time + timedelta(hours=i * 2)

        # Add to internal state
        if user_id not in agent.memory.conversations:
            agent.memory.conversations[user_id] = []

        agent.memory.conversations[user_id].append(
            {"user_message": user_msg, "bot_response": bot_msg, "timestamp": timestamp.isoformat()}
        )

    agent.memory.save_memory(user_id)
    print(f"Added {len(conversations)} conversations to memory.")

    # Initialize Analytics
    analytics = ConversationAnalytics(agent.memory)

    # 1. Get Stats
    print("\n--- General Statistics ---")
    stats = analytics.get_conversation_stats(user_id)
    for k, v in stats.items():
        print(f"{k}: {v}")

    # 2. Topic Distribution
    print("\n--- Topic Distribution ---")
    topics = analytics.get_topic_distribution(user_id)
    for topic, count in topics.items():
        print(f"{topic}: {count}")

    # 3. Engagement Metrics
    print("\n--- Engagement Metrics ---")
    engagement = analytics.get_engagement_metrics(user_id)
    for k, v in engagement.items():
        print(f"{k}: {v}")

    # 4. Time Distribution
    print("\n--- Time Distribution ---")
    time_dist = analytics.get_time_distribution(user_id)
    print(time_dist)

    # 5. Export Report
    print("\n--- Exporting Report ---")
    report_md = analytics.export_report(user_id, format="markdown")

    print("\nPreview of report:")
    print("-" * 20)
    print(report_md[:300] + "...\n(truncated)")
    print("-" * 20)


if __name__ == "__main__":
    try:
        demo_config_presets()
        demo_analytics()
        print("\nDemo completed successfully!")
    except ImportError as e:
        print(f"\nError: {e}")
        print(
            "Please make sure you have installed the package or are running this from the correct directory."
        )
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback

        traceback.print_exc()
