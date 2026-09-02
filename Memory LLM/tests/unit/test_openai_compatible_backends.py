from mem_llm import LLMClientFactory, LLMResponse, MemAgent
from mem_llm.clients import LlamaCppClient, LMStudioClient, OpenAICompatibleClient


def test_openai_compatible_backend_registered():
    backends = LLMClientFactory.get_available_backends()
    names = {backend["name"] for backend in backends}

    assert "openai-compatible" in names
    assert "llamacpp" in names


def test_create_openai_compatible_client_offline():
    client = LLMClientFactory.create(
        "openai-compatible",
        model="test-model",
        base_url="http://127.0.0.1:9999",
        api_key="test-key",
    )

    assert isinstance(client, OpenAICompatibleClient)
    assert client.model == "test-model"
    assert client.base_url == "http://127.0.0.1:9999"


def test_create_llamacpp_alias_client_offline():
    client = LLMClientFactory.create(
        "llama-cpp",
        base_url="http://127.0.0.1:8080",
    )

    assert isinstance(client, LlamaCppClient)
    assert client.model == "llama.cpp"


def test_mem_agent_llamacpp_default_model_alias():
    agent = MemAgent(backend="llamacpp", use_sql=False, check_connection=False)

    assert agent.backend == "llamacpp"
    assert agent.model == "llama.cpp"
    assert isinstance(agent.llm, LlamaCppClient)


def test_mem_agent_openai_compatible_default_model_alias():
    agent = MemAgent(backend="openai-compatible", use_sql=False, check_connection=False)

    assert agent.backend == "openai-compatible"
    assert agent.model == "local-model"
    assert isinstance(agent.llm, OpenAICompatibleClient)


class _FakeResponse:
    status_code = 200
    text = ""

    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_lmstudio_native_tool_call_response_is_preserved(monkeypatch):
    response_data = {
        "id": "chatcmpl-test",
        "model": "mem-llm-lfm2.5",
        "choices": [
            {
                "index": 0,
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "content": "",
                    "reasoning_content": "I should use the weather tool.",
                    "tool_calls": [
                        {
                            "id": "call-weather",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"city":"Istanbul"}',
                            },
                        }
                    ],
                },
            }
        ],
        "usage": {
            "prompt_tokens": 97,
            "completion_tokens": 69,
            "total_tokens": 166,
            "completion_tokens_details": {"reasoning_tokens": 55},
        },
    }
    posted = {}

    def fake_post(url, json, timeout):
        posted.update({"url": url, "json": json, "timeout": timeout})
        return _FakeResponse(response_data)

    monkeypatch.setattr("mem_llm.clients.lmstudio_client.requests.post", fake_post)
    client = LMStudioClient(model="mem-llm-lfm2.5")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"],
                },
            },
        }
    ]

    result = client.chat_response(
        [{"role": "user", "content": "Use the weather tool for Istanbul."}],
        tools=tools,
        tool_choice="auto",
        max_retries=1,
    )

    assert isinstance(result, LLMResponse)
    assert result.content == ""
    assert result.reasoning == "I should use the weather tool."
    assert result.finish_reason == "tool_calls"
    assert result.model == "mem-llm-lfm2.5"
    assert result.has_tool_calls
    assert result.tool_calls[0].id == "call-weather"
    assert result.tool_calls[0].name == "get_weather"
    assert result.tool_calls[0].arguments == {"city": "Istanbul"}
    assert result.usage.prompt_tokens == 97
    assert result.usage.reasoning_tokens == 55
    assert posted["json"]["tools"] == tools
    assert posted["json"]["tool_choice"] == "auto"


def test_lmstudio_chat_remains_text_compatible(monkeypatch):
    response_data = {
        "model": "test-model",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": " OK ",
                    "reasoning_content": "Short reasoning",
                    "tool_calls": [],
                },
            }
        ],
    }

    monkeypatch.setattr(
        "mem_llm.clients.lmstudio_client.requests.post",
        lambda *args, **kwargs: _FakeResponse(response_data),
    )

    client = LMStudioClient(model="test-model")
    assert client.chat([{"role": "user", "content": "Say OK"}], max_retries=1) == "OK"


def test_lmstudio_no_choices_still_returns_response_envelope(monkeypatch):
    monkeypatch.setattr(
        "mem_llm.clients.lmstudio_client.requests.post",
        lambda *args, **kwargs: _FakeResponse({"model": "test-model", "choices": []}),
    )

    client = LMStudioClient(model="test-model")
    result = client.chat_response([{"role": "user", "content": "Hello"}], max_retries=1)

    assert isinstance(result, LLMResponse)
    assert result.content == ""
    assert result.model == "test-model"
