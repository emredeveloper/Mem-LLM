import asyncio
import os
import sys

# Add parent directory to path to import mem_llm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_llm import MemAgent
from mem_llm.workflow import Step, Workflow


async def main():
    print("🚀 Initializing MemAgent for LM STUDIO Demo...")

    # 1. Initialize agent specifically for LM Studio
    # This should auto-select "google/gemma-3-4b" if no model is provided
    try:
        agent = MemAgent(
            backend="lmstudio", check_connection=True  # We want to verify connection here
        )
        print(f"✅ Connected to LM Studio using model: {agent.model}")
    except Exception as e:
        print(f"❌ Failed to connect to LM Studio: {e}")
        print(
            "💡 Hint: Make sure LM Studio is running and the local server is started (default port 1234)."
        )
        return

    agent.set_user("lmstudio_user")

    # 2. Define Workflow
    workflow = Workflow("Creative Writing Flow")

    step1 = Step(
        name="Ideation",
        agent=agent,
        action="Generate a creative story idea about a robot exploring a magical forest. Keep it brief.",
        output_key="idea",
        description="Generating story idea...",
    )

    step2 = Step(
        name="Expansion",
        agent=agent,
        action="Take this idea and write the opening paragraph.",
        input_key="idea",
        output_key="story_opening",
        description="Writing opening...",
    )

    workflow.add_step(step1)
    workflow.add_step(step2)

    # 3. Run
    print("\n▶️  Running workflow...")
    context = await workflow.run()

    # 4. Results
    print("\n" + "=" * 50)
    print("✅ LM STUDIO WORKFLOW COMPLETE")
    print("=" * 50)

    print(f"\n💡 [Idea]:\n{context.get('idea')}")
    print(f"\n📖 [Story Opening]:\n{context.get('story_opening')}")


if __name__ == "__main__":
    asyncio.run(main())
