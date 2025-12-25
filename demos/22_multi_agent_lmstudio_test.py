"""
Multi-Agent System - LM Studio Test
====================================

Tests multi-agent features with LM Studio backend.
"""

import sys
from pathlib import Path

# Add Memory LLM to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Memory LLM"))

from mem_llm.multi_agent import (
    AgentRegistry,
    AgentRole,
    BaseAgent,
    CommunicationHub,
)


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    print_section("🧪 Multi-Agent LM Studio Test")

    # ========================================================================
    # Test 1: Agent Creation with LM Studio
    # ========================================================================
    print_section("Test 1: Creating Agents with LM Studio Backend")

    print("\n🤖 Creating agents with LM Studio...")
    try:
        researcher = BaseAgent(
            name="LM Studio Researcher",
            role=AgentRole.RESEARCHER,
            backend="lmstudio",
            model="google/gemma-3-4b",
        )
        print(f"✅ Created: {researcher.name}")

        analyst = BaseAgent(
            name="LM Studio Analyst",
            role=AgentRole.ANALYST,
            backend="lmstudio",
            model="local-model",
        )
        print(f"✅ Created: {analyst.name}")

    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        return

    # ========================================================================
    # Test 2: Registry
    # ========================================================================
    print_section("Test 2: Agent Registry")

    registry = AgentRegistry()
    registry.register(researcher)
    registry.register(analyst)

    stats = registry.get_stats()
    print(f"\n📊 Registry Stats:")
    print(f"   Total Agents: {stats['total_agents']}")
    print(f"   By Role: {stats['by_role']}")

    # ========================================================================
    # Test 3: Communication
    # ========================================================================
    print_section("Test 3: Inter-Agent Communication")

    hub = CommunicationHub()
    hub.register_agent(researcher.agent_id)
    hub.register_agent(analyst.agent_id)

    # Direct message
    print(f"\n📤 {researcher.name} → {analyst.name}")
    msg = researcher.send_message(
        analyst.agent_id,
        "Can you analyze this data?"
    )
    hub.send_message(msg)
    print(f"   Message sent: '{msg.content}'")

    # Check inbox
    print(f"\n📥 {analyst.name} checking inbox...")
    messages = hub.get_messages(analyst.agent_id)
    print(f"   Received {len(messages)} message(s)")
    for m in messages:
        print(f"   From {m.sender_id[:16]}...: '{m.content}'")

    # ========================================================================
    # Test 4: Task Processing with LM Studio
    # ========================================================================
    print_section("Test 4: Task Processing with LM Studio")

    print(f"\n🔬 {researcher.name} processing task...")
    task = "What are the benefits of multi-agent systems?"
    print(f"   Task: {task}")

    try:
        result = researcher.process(task)
        print(f"   ✅ Response received ({len(result)} chars)")
        print(f"   Preview: {result[:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # ========================================================================
    # Test 5: Broadcast
    # ========================================================================
    print_section("Test 5: Broadcast Messaging")

    hub.subscribe(researcher.agent_id, "updates")
    hub.subscribe(analyst.agent_id, "updates")

    print(f"\n📢 Broadcasting to 'updates' channel...")
    delivered = hub.broadcast(
        researcher.agent_id,
        "LM Studio integration working!",
        channel="updates"
    )
    print(f"   Delivered to {delivered} agents")

    print_section("✅ LM Studio Test Complete!")


if __name__ == "__main__":
    print("\n⚠️  Make sure LM Studio is running on http://localhost:1234")
    print("   and a model is loaded before running this test.\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
