import asyncio
import os
import sys

# Add parent directory to path to import mem_llm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_llm import MemAgent
from mem_llm.workflow import Step, Workflow


async def main():
    print("🚀 Initializing MemAgent for Workflow Demo...")
    # Initialize agent (auto-detects backend)
    agent = MemAgent(auto_detect_backend=True)
    agent.set_user("demo_user")  # Fix: User ID is required for chat

    # Define a Workflow
    # Scenario: "Deep Research"
    # Step 1: Research a topic
    # Step 2: Summarize the research into a tweet

    print("\n📦 Building 'Deep Research' Workflow...")
    workflow = Workflow("Deep Research Flow")

    # Step 1: Research
    # We pass the input topic via context
    step1 = Step(
        name="Research Phase",
        agent=agent,
        action="You are a researcher. Provide 3 key facts about the following topic:",
        input_key="topic",  # Reads 'topic' from workflow context
        output_key="facts",  # Saves response to 'facts' in context
        description="Gathering facts...",
    )

    # Step 2: Summarize
    # We chain the output of Step 1 ('facts') as input here
    step2 = Step(
        name="Summarization Phase",
        agent=agent,
        action="You are a social media manager. Write a catchy tweet based on these facts:",
        input_key="facts",  # Reads 'facts' (output of Step 1)
        output_key="tweet",  # Saves response to 'tweet'
        description="Drafting tweet...",
    )

    workflow.add_step(step1)
    workflow.add_step(step2)

    # Run the workflow
    topic = "The Future of Artificial Intelligence"
    print(f"\n▶️  Running workflow on topic: '{topic}'")

    context = await workflow.run(initial_data={"topic": topic})

    # Display results
    print("\n" + "=" * 50)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 50)

    print(f"\n📄 [Step 1 Output] Facts about '{topic}':")
    print("-" * 30)
    print(context.get("facts"))

    print(f"\n🐦 [Step 2 Output] Generated Tweet:")
    print("-" * 30)
    print(context.get("tweet"))

    print("\n" + "=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
