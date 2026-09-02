"""Provider-neutral response models for LLM backends."""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMToolCall:
    """A normalized function/tool call emitted by a model."""

    name: str
    arguments: Any = field(default_factory=dict)
    id: Optional[str] = None
    type: str = "function"
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class LLMUsage:
    """Normalized token usage reported by a provider."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    reasoning_tokens: int = 0
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class LLMResponse:
    """A provider-neutral, lossless-enough chat response envelope."""

    content: str = ""
    reasoning: Optional[str] = None
    tool_calls: List[LLMToolCall] = field(default_factory=list)
    usage: Optional[LLMUsage] = None
    finish_reason: Optional[str] = None
    model: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def has_tool_calls(self) -> bool:
        """Return whether the model requested at least one tool call."""
        return bool(self.tool_calls)


def parse_openai_chat_response(
    response_data: Dict[str, Any], default_model: Optional[str] = None
) -> LLMResponse:
    """Normalize an OpenAI-compatible chat-completions response."""
    choices = response_data.get("choices") or []
    choice = choices[0] if choices and isinstance(choices[0], dict) else {}
    message = choice.get("message") or {}
    if not isinstance(message, dict):
        message = {}

    content = message.get("content") or ""
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)

    reasoning = None
    for key in ("reasoning_content", "reasoning", "thinking"):
        value = message.get(key)
        if value:
            reasoning = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            break

    tool_calls = []
    for raw_call in message.get("tool_calls") or []:
        if not isinstance(raw_call, dict):
            continue
        function = raw_call.get("function") or {}
        if not isinstance(function, dict):
            function = {}

        arguments = function.get("arguments", {})
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                # Preserve non-JSON arguments instead of dropping provider output.
                pass

        tool_calls.append(
            LLMToolCall(
                id=raw_call.get("id"),
                type=raw_call.get("type", "function"),
                name=function.get("name", ""),
                arguments=arguments,
                raw=raw_call,
            )
        )

    usage_data = response_data.get("usage") or {}
    usage = None
    if isinstance(usage_data, dict) and usage_data:
        completion_details = usage_data.get("completion_tokens_details") or {}
        if not isinstance(completion_details, dict):
            completion_details = {}
        usage = LLMUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0) or 0,
            completion_tokens=usage_data.get("completion_tokens", 0) or 0,
            total_tokens=usage_data.get("total_tokens", 0) or 0,
            reasoning_tokens=completion_details.get("reasoning_tokens", 0) or 0,
            raw=usage_data,
        )

    return LLMResponse(
        content=content.strip(),
        reasoning=reasoning,
        tool_calls=tool_calls,
        usage=usage,
        finish_reason=choice.get("finish_reason"),
        model=response_data.get("model") or default_model,
        raw=response_data,
    )
