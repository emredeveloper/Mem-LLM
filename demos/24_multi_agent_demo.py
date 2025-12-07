"""
Multi-Agent System - Comprehensive Demo
========================================

Demonstrates all Phase 1 features:
- BaseAgent with role-based behavior
- AgentRegistry for centralized management
- CommunicationHub for messaging
- Direct messaging and broadcast channels

Author: C. Emre Karataş
Version: 2.2.0
"""

import sys
from pathlib import Path

# Add Memory LLM to path - must be before other imports
sys.path.insert(0, str(Path(__file__).parent.parent / "Memory LLM"))

from mem_llm.multi_agent import AgentRegistry, AgentRole, BaseAgent, CommunicationHub  # noqa: E402


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    print_section("🤖 Multi-Agent System Demo - Phase 1 Complete")

    # ========================================================================
    # PART 1: Agent Creation & Registry
    # ========================================================================
    print_section("Part 1: Creating Agents & Registry")

    print("\n📋 Creating Agent Registry...")
    registry = AgentRegistry()

    print("🤖 Creating Specialized Agents...")

    # Create agents with different roles
    researcher = BaseAgent(
        name="Research Bot",
        role=AgentRole.RESEARCHER,
        model="granite4:3b",
    )

    analyst = BaseAgent(
        name="Data Analyst",
        role=AgentRole.ANALYST,
        model="granite4:3b",
    )

    writer = BaseAgent(
        name="Content Writer",
        role=AgentRole.WRITER,
        model="granite4:3b",
    )

    # Register agents
    print("\n✅ Registering agents...")
    registry.register(researcher)
    registry.register(analyst)
    registry.register(writer)

    # Show registry stats
    stats = registry.get_stats()
    print("\n📊 Registry Stats:")
    print(f"   Total Agents: {stats['total_agents']}")
    print(f"   By Role: {stats['by_role']}")

    # ========================================================================
    # PART 2: Communication Hub Setup
    # ========================================================================
    print_section("Part 2: Communication Hub")

    print("\n📡 Creating Communication Hub...")
    hub = CommunicationHub()

    # Register agents in hub
    print("✅ Registering agents in communication hub...")
    hub.register_agent(researcher.agent_id)
    hub.register_agent(analyst.agent_id)
    hub.register_agent(writer.agent_id)

    # ========================================================================
    # PART 3: Direct Messaging
    # ========================================================================
    print_section("Part 3: Direct Agent-to-Agent Messaging")

    print(f"\n📤 {researcher.name} → {analyst.name}")
    msg1 = researcher.send_message(
        analyst.agent_id, "I found interesting AI trends data. Can you analyze it?"
    )
    hub.send_message(msg1)
    print(f"   Message: '{msg1.content}'")

    print(f"\n📤 {analyst.name} → {writer.name}")
    msg2 = analyst.send_message(writer.agent_id, "Analysis complete. Please write a summary.")
    hub.send_message(msg2)
    print(f"   Message: '{msg2.content}'")

    # Check messages
    print(f"\n📥 {analyst.name} checking inbox...")
    analyst_msgs = hub.get_messages(analyst.agent_id)
    print(f"   Received {len(analyst_msgs)} message(s)")
    for msg in analyst_msgs:
        print(f"   From {msg.sender_id[:16]}...: '{msg.content}'")

    print(f"\n📥 {writer.name} checking inbox...")
    writer_msgs = hub.get_messages(writer.agent_id)
    print(f"   Received {len(writer_msgs)} message(s)")
    for msg in writer_msgs:
        print(f"   From {msg.sender_id[:16]}...: '{msg.content}'")

    # ========================================================================
    # PART 4: Broadcast Channels
    # ========================================================================
    print_section("Part 4: Broadcast Messaging")

    # Subscribe to channels
    print("\n🔔 Setting up broadcast channels...")
    hub.subscribe(researcher.agent_id, "ai-news")
    hub.subscribe(analyst.agent_id, "ai-news")
    hub.subscribe(writer.agent_id, "ai-news")
    print("   All agents subscribed to 'ai-news' channel")

    # Broadcast message
    print(f"\n📢 {researcher.name} broadcasting to 'ai-news'...")
    delivered = hub.broadcast(
        researcher.agent_id, "Breaking: New multi-agent framework released!", channel="ai-news"
    )
    print(f"   Delivered to {delivered} agents")

    # Check broadcast messages
    print(f"\n📥 {analyst.name} checking broadcast messages...")
    analyst_broadcast = hub.get_messages(analyst.agent_id)
    if analyst_broadcast:
        print(f"   Received: '{analyst_broadcast[0].content}'")

    print(f"\n📥 {writer.name} checking broadcast messages...")
    writer_broadcast = hub.get_messages(writer.agent_id)
    if writer_broadcast:
        print(f"   Received: '{writer_broadcast[0].content}'")

    # ========================================================================
    # PART 5: Agent Task Processing
    # ========================================================================
    print_section("Part 5: Agent Task Processing (Role-Based)")

    print(f"\n🔬 {researcher.name} (RESEARCHER role):")
    research_task = "What are the top 3 AI trends in 2025?"
    print(f"   Task: {research_task}")
    research_result = researcher.process(research_task)
    print(f"   Response: {research_result[:150]}...")

    print(f"\n📊 {analyst.name} (ANALYST role):")
    analysis_task = "Analyze the importance of multi-agent systems"
    print(f"   Task: {analysis_task}")
    analysis_result = analyst.process(analysis_task)
    print(f"   Response: {analysis_result[:150]}...")

    print(f"\n✍️  {writer.name} (WRITER role):")
    writing_task = "Write a brief intro about AI agents"
    print(f"   Task: {writing_task}")
    writing_result = writer.process(writing_task)
    print(f"   Response: {writing_result[:150]}...")

    # ========================================================================
    # PART 6: Statistics & Health Check
    # ========================================================================
    print_section("Part 6: System Statistics")

    # Registry stats
    print("\n📊 Registry Statistics:")
    reg_stats = registry.get_stats()
    print(f"   Total Agents: {reg_stats['total_agents']}")
    print(f"   Roles: {list(reg_stats['by_role'].keys())}")
    print(f"   Status: {list(reg_stats['by_status'].keys())}")

    # Communication stats
    print("\n📡 Communication Hub Statistics:")
    comm_stats = hub.get_stats()
    print(f"   Registered Agents: {comm_stats['registered_agents']}")
    print(f"   Queued Messages: {comm_stats['total_queued_messages']}")
    print(f"   Active Channels: {comm_stats['channels']}")

    # Health check
    print("\n🏥 Health Check:")
    health = registry.health_check()
    print(f"   ✅ Healthy Agents: {health['healthy_count']}")
    print(f"   ⚠️  Unhealthy Agents: {health['unhealthy_count']}")

    # Agent info
    print("\n🤖 Agent Details:")
    for agent in registry.get_all():
        info = agent.get_info()
        print(f"\n   {info['name']}:")
        print(f"      ID: {info['agent_id'][:16]}...")
        print(f"      Role: {info['role']}")
        print(f"      Status: {info['status']}")
        print(f"      Conversations: {info['conversation_count']}")

    print_section("✅ Demo Complete!")
    print("\n🎉 All Phase 1 features demonstrated successfully!")
    print("\nFeatures Shown:")
    print("  ✅ BaseAgent with role-based behavior")
    print("  ✅ AgentRegistry for centralized management")
    print("  ✅ CommunicationHub for messaging")
    print("  ✅ Direct agent-to-agent messaging")
    print("  ✅ Broadcast channels with subscriptions")
    print("  ✅ Task processing with LLM integration")
    print("  ✅ Statistics and health monitoring")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
