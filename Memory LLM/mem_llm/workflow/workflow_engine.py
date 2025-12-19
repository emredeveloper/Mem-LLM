import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

import yaml

from ..mem_agent import MemAgent

logger = logging.getLogger(__name__)


@dataclass
class WorkflowContext:
    """Shared context for a workflow execution."""

    data: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value


class Step:
    """A single step in a workflow."""

    def __init__(
        self,
        name: str,
        action: Union[str, Callable],
        agent: Optional[MemAgent] = None,
        tool_name: Optional[str] = None,
        tool_args: Optional[Dict[str, Any]] = None,
        input_key: Optional[str] = None,
        output_key: Optional[str] = None,
        description: str = "",
    ):
        self.name = name
        self.action = action  # Can be a prompt string (for agent) or a callable
        self.agent = agent
        self.tool_name = tool_name
        self.tool_args = tool_args
        self.input_key = input_key
        self.output_key = output_key
        self.description = description

    async def execute(self, context: WorkflowContext) -> Any:
        logger.info(f"Executing step: {self.name}")

        # Determine input
        input_data = None
        if self.input_key:
            input_data = context.get(self.input_key)

        result = None

        try:
            # Case 1: Agent Chat
            if self.agent and isinstance(self.action, str):
                prompt = self.action
                if input_data:
                    prompt = f"{prompt}\n\nContext: {input_data}"

                # Execute agent chat
                # Note: Assuming synchronous chat for now unless we use a wrapper,
                # but let's wrap in existing loop if needed or just call blocking
                # To be true async, MemAgent needs async methods, but we can run in executor.
                # For now, we'll call it directly (blocking) as MemAgent is primarily sync
                # (though it has some async tools support).
                agent_label = self.agent.agent_id if hasattr(self.agent, "agent_id") else "Agent"
                logger.info(f" Agent {agent_label} thinking...")
                result = self.agent.chat(prompt)

            # Case 2: Tool Execution
            elif self.tool_name:
                # We need a tool registry.
                # If agent has one, use it.
                registry = None
                if self.agent and hasattr(self.agent, "tool_registry"):
                    registry = self.agent.tool_registry

                if registry:
                    args = self.tool_args or {}
                    # Interpolate args from context if needed?
                    # For simplicity v1: direct args or injected input
                    if input_data and "input" not in args:
                        # Heuristic: if input is available and not specified, maybe inject it?
                        # Or rely on user to specify args.
                        pass

                    logger.info(f" Calling tool {self.tool_name}")
                    result = registry.execute(self.tool_name, **args)
                else:
                    raise ValueError("Tool execution requested but no registry available via agent")

            # Case 3: Custom Callable
            elif callable(self.action):
                if asyncio.iscoroutinefunction(self.action):
                    result = await self.action(context)
                else:
                    result = self.action(context)

            else:
                raise ValueError(f"Invalid step configuration for {self.name}")

            # Store output
            if self.output_key and result is not None:
                context.set(self.output_key, result)

            # Record history
            context.history.append(
                {
                    "step": self.name,
                    "status": "success",
                    "output": str(result)[:200] + "..."
                    if result and len(str(result)) > 200
                    else result,
                }
            )

            return result

        except Exception as e:
            logger.error(f"Step {self.name} failed: {e}")
            context.history.append({"step": self.name, "status": "error", "error": str(e)})
            raise e


class Workflow:
    """A sequence of steps."""

    def __init__(self, name: str, steps: List[Step] = None):
        self.name = name
        self.steps = steps or []

    def add_step(self, step: Step):
        self.steps.append(step)

    async def run(self, initial_data: Dict[str, Any] = None) -> WorkflowContext:
        context = WorkflowContext(data=initial_data or {})
        logger.info(f"Starting workflow: {self.name}")

        for step in self.steps:
            await step.execute(context)

        logger.info(f"Workflow {self.name} completed.")
        return context

    async def run_generator(self, initial_data: Dict[str, Any] = None):
        """Run workflow and yield events for each step."""
        context = WorkflowContext(data=initial_data or {})
        yield {"type": "start", "workflow": self.name}

        for step in self.steps:
            yield {"type": "step_start", "step": step.name, "description": step.description}
            try:
                result = await step.execute(context)
                # If output is large, we might truncate for the event, or send full
                output_str = (
                    str(result)[:500] + "..." if result and len(str(result)) > 500 else str(result)
                )
                yield {"type": "step_complete", "step": step.name, "output": output_str}
            except Exception as e:
                yield {"type": "step_error", "step": step.name, "error": str(e)}
                raise e

        yield {"type": "complete", "results": context.data}

    @classmethod
    def from_yaml(cls, file_path: str, agents: Dict[str, MemAgent]) -> "Workflow":
        """Load a workflow from a YAML file."""
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        workflow = cls(name=data.get("name", "Untitled Workflow"))

        for step_data in data.get("steps", []):
            agent_name = step_data.get("agent")
            agent = agents.get(agent_name) if agent_name else None

            step = Step(
                name=step_data.get("name"),
                action=step_data.get("action"),
                agent=agent,
                tool_name=step_data.get("tool"),
                tool_args=step_data.get("args"),
                input_key=step_data.get("input"),
                output_key=step_data.get("output"),
                description=step_data.get("description", ""),
            )
            workflow.add_step(step)

        return workflow
