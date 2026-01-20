"""Run a simple workflow with non-blocking agent calls."""

from mem_llm.mem_agent import MemAgent
from mem_llm.workflow import Step, Workflow

from demo_config import BACKEND, BASE_URL, MODEL


def main() -> None:
    agent = MemAgent(model=MODEL, backend=BACKEND, base_url=BASE_URL)
    agent.set_user("demo_user")

    workflow = Workflow("Quick Summary")
    workflow.add_step(
        Step(
            "Gather",
            agent=agent,
            action="List three facts about Python programming.",
            output_key="facts",
        )
    )
    workflow.add_step(
        Step(
            "Summarize",
            agent=agent,
            action="Summarize these facts in one sentence.",
            input_key="facts",
            output_key="summary",
        )
    )

    context = __import__("asyncio").run(workflow.run())
    print("Summary:", context.get("summary"))


if __name__ == "__main__":
    main()
