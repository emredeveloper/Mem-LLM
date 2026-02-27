import os
import uuid
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mem_llm.workflow.workflow_engine import Step, Workflow


class MockAgent:
    def __init__(self, name="MockAgent"):
        self.name = name
        self.chat = MagicMock(return_value="Mock response")
        self.agent_id = "agent_123"


@pytest.mark.asyncio
async def test_simple_workflow_execution():
    def step1_action(context):
        return "Hello"

    async def step2_action(context):
        val = context.get("greeting")
        return f"{val} World"

    workflow = Workflow("Test Flow")
    workflow.add_step(Step(name="Start", action=step1_action, output_key="greeting"))
    workflow.add_step(Step(name="End", action=step2_action, output_key="result"))

    context = await workflow.run()

    assert context.get("greeting") == "Hello"
    assert context.get("result") == "Hello World"
    assert len(context.history) == 2
    assert context.history[0]["step"] == "Start"
    assert context.history[0]["status"] == "success"


@pytest.mark.asyncio
async def test_agent_integration():
    agent = MockAgent()

    workflow = Workflow("Agent Flow")
    step = Step(name="Ask Agent", action="What is AI?", agent=agent, output_key="answer")
    workflow.add_step(step)

    context = await workflow.run()

    assert context.get("answer") == "Mock response"
    agent.chat.assert_called_once()
    args, _ = agent.chat.call_args
    assert "What is AI?" in args[0]


@pytest.mark.asyncio
async def test_yaml_workflow_loading():
    yaml_content = """
    name: YAML Flow
    steps:
      - name: Step 1
        action: "Analyze this"
        agent: agent_a
        input: initial_input
        output: analysis
      - name: Step 2
        action: "Summarize"
        agent: agent_a
        input: analysis
        output: summary
    """

    agent = MockAgent("Agent A")
    agents = {"agent_a": agent}

    root = Path(__file__).resolve().parents[1] / ".tmp"
    root.mkdir(parents=True, exist_ok=True)
    temp_path = root / f"workflow_{uuid.uuid4().hex[:8]}.yaml"
    temp_path.write_text(yaml_content, encoding="utf-8")

    try:
        workflow = Workflow.from_yaml(str(temp_path), agents)
        assert workflow.name == "YAML Flow"
        assert len(workflow.steps) == 2
        assert workflow.steps[0].name == "Step 1"
        assert workflow.steps[0].agent == agent

        context = await workflow.run({"initial_input": "Data"})
        assert context.get("analysis") == "Mock response"
        assert context.get("summary") == "Mock response"

    finally:
        os.remove(temp_path)
