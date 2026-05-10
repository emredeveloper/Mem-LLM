from mem_llm import LLMClientFactory, MemAgent
from mem_llm.clients import LlamaCppClient, OpenAICompatibleClient


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
