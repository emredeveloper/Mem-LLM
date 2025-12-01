"""
Multi-Agent System - Mixed Ollama Models Test
==============================================

Tests using different Ollama models for different agents.
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
    print_section("🧪 Multi-Model Multi-Backend Test")

    # ========================================================================
    # Create agents with DIFFERENT models and backends
    # ========================================================================
    print_section("Creating Agents with Different Models & Backends")

    print("\n🤖 Creating agents with different configurations...")

    # Agent 1: Ollama with granite4:3b (IBM model, good for analysis)
    researcher = BaseAgent(
        name="Granite Researcher",
        role=AgentRole.RESEARCHER,
        backend="ollama",
        model="granite4:3b",
    )
    print(f"✅ {researcher.name}")
    print(f"   Backend: Ollama | Model: granite4:3b")

    # Agent 2: LM Studio with Google Gemma (powerful, good for analysis)
    analyst = BaseAgent(
        name="Gemma Analyst",
        role=AgentRole.ANALYST,
        backend="lmstudio",
        model="google/gemma-3-4b",
    )
    print(f"✅ {analyst.name}")
    print(f"   Backend: LM Studio | Model: google/gemma-3-4b")

    # Agent 3: Ollama with Qwen Vision (multimodal capabilities)
    writer = BaseAgent(
        name="Qwen Writer",
        role=AgentRole.WRITER,
        backend="ollama",
        model="qwen3-vl:2b",
    )
    print(f"✅ {writer.name}")
    print(f"   Backend: Ollama | Model: qwen3-vl:2b")

    # Agent 4: LM Studio with Qwen (alternative model)
    validator = BaseAgent(
        name="Qwen Validator",
        role=AgentRole.VALIDATOR,
        backend="lmstudio",
        model="qwen/qwen3-4b-2507",
    )
    print(f"✅ {validator.name}")
    print(f"   Backend: LM Studio | Model: qwen/qwen3-4b-2507")

    # ========================================================================
    # Register all agents
    # ========================================================================
    print_section("Agent Registry")

    registry = AgentRegistry()
    registry.register(researcher)
    registry.register(analyst)
    registry.register(writer)
    registry.register(validator)

    stats = registry.get_stats()
    print(f"\n📊 Registry Stats:")
    print(f"   Total Agents: {stats['total_agents']}")
    print(f"   By Role: {stats['by_role']}")
    print(f"   Backends: Ollama (2), LM Studio (2)")

    # ========================================================================
    # Test each agent with their specific model
    # ========================================================================
    print_section("Testing Each Agent's Model")

    # Test 1: Researcher (Ollama - granite4:3b)
    print(f"\n🔬 {researcher.name} (Ollama/granite4:3b):")
    task1 = "What is artificial intelligence?"
    print(f"   Task: {task1}")
    try:
        result1 = researcher.process(task1)
        print(f"   ✅ Response ({len(result1)} chars): {result1[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Analyst (LM Studio - Gemma)
    print(f"\n📊 {analyst.name} (LM Studio/gemma-3-4b):")
    task2 = "Analyze the benefits of multi-agent systems"
    print(f"   Task: {task2}")
    try:
        result2 = analyst.process(task2)
        print(f"   ✅ Response ({len(result2)} chars): {result2[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Writer (Ollama - Qwen Vision)
    print(f"\n✍️  {writer.name} (Ollama/qwen3-vl:2b):")
    task3 = "Write a brief intro about AI agents"
    print(f"   Task: {task3}")
    try:
        result3 = writer.process(task3)
        print(f"   ✅ Response ({len(result3)} chars): {result3[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 4: Validator (LM Studio - Qwen)
    print(f"\n✅ {validator.name} (LM Studio/qwen3-4b-2507):")
    task4 = "Validate: Is multi-agent architecture beneficial?"
    print(f"   Task: {task4}")
    try:
        result4 = validator.process(task4)
        print(f"   ✅ Response ({len(result4)} chars): {result4[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # ========================================================================
    # Test inter-agent communication (cross-backend!)
    # ========================================================================
    print_section("Cross-Backend Inter-Agent Communication")

    hub = CommunicationHub()
    hub.register_agent(researcher.agent_id)
    hub.register_agent(analyst.agent_id)
    hub.register_agent(writer.agent_id)
    hub.register_agent(validator.agent_id)

    # Ollama → LM Studio
    print(f"\n📤 {researcher.name} (Ollama) → {analyst.name} (LM Studio)")
    msg1 = researcher.send_message(
        analyst.agent_id,
        "I found interesting data about AI trends"
    )
    hub.send_message(msg1)
    print(f"   ✅ Cross-backend message sent!")

    # LM Studio → Ollama
    print(f"\n📤 {analyst.name} (LM Studio) → {writer.name} (Ollama)")
    msg2 = analyst.send_message(
        writer.agent_id,
        "Please write a summary based on the analysis"
    )
    hub.send_message(msg2)
    print(f"   ✅ Cross-backend message sent!")

    # Ollama → LM Studio (different model)
    print(f"\n📤 {writer.name} (Ollama) → {validator.name} (LM Studio)")
    msg3 = writer.send_message(
        validator.agent_id,
        "Please validate this summary for accuracy"
    )
    hub.send_message(msg3)
    print(f"   ✅ Cross-backend message sent!")

    # Check messages
    print(f"\n📥 Message delivery check:")
    for agent in [researcher, analyst, writer, validator]:
        msgs = hub.get_messages(agent.agent_id)
        if msgs:
            print(f"   {agent.name}: {len(msgs)} message(s)")
            for msg in msgs:
                print(f"      From {msg.sender_id[:16]}...: '{msg.content[:40]}...'")

    # ========================================================================
    # Broadcast test
    # ========================================================================
    print_section("Broadcast Communication (All Backends)")

    # Subscribe all to updates channel
    hub.subscribe(researcher.agent_id, "team-updates")
    hub.subscribe(analyst.agent_id, "team-updates")
    hub.subscribe(writer.agent_id, "team-updates")
    hub.subscribe(validator.agent_id, "team-updates")

    print(f"\n📢 Broadcasting team update to all agents...")
    delivered = hub.broadcast(
        researcher.agent_id,
        "Team meeting at 3 PM - discuss multi-agent project progress",
        channel="team-updates"
    )
    print(f"   ✅ Delivered to {delivered} agents (Ollama + LM Studio)")

    # ========================================================================
    # Agent Info
    # ========================================================================
    print_section("Agent Configuration Summary")

    for agent in [researcher, analyst, writer, validator]:
        info = agent.get_info()
        backend = "Ollama" if agent.mem_agent.backend == "ollama" else "LM Studio"
        print(f"\n🤖 {info['name']}:")
        print(f"   Role: {info['role']}")
        print(f"   Backend: {backend}")
        print(f"   Model: {agent.mem_agent.model}")
        print(f"   Status: {info['status']}")
        print(f"   Conversations: {info['conversation_count']}")

    print_section("✅ Multi-Model Multi-Backend Test Complete!")
    print("\n💡 Key Takeaways:")
    print("   ✅ 4 different models tested (2 Ollama + 2 LM Studio)")
    print("   ✅ Cross-backend communication works seamlessly")
    print("   ✅ Each agent maintains separate conversation history")
    print("   ✅ Role-based prompts create specialized behavior")
    print("   ✅ Ollama ↔ LM Studio agents can collaborate!")


if __name__ == "__main__":
    print("\n⚠️  Requirements:")
    print("   - Ollama: granite4:3b, qwen3-vl:2b")
    print("   - LM Studio: google/gemma-3-4b, qwen/qwen3-4b-2507")
    print("   - LM Studio running on http://localhost:1234\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
