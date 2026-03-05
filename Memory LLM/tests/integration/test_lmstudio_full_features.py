"""High-coverage LM Studio integration tests for core Mem-LLM features."""

import json
import os
import shutil
import uuid
from pathlib import Path

import pytest

from mem_llm import MemAgent


def _model_name() -> str:
    return os.environ.get("MEM_LLM_LMSTUDIO_MODEL", "qwen3.5-2b")


def _workspace_tmp_dir() -> Path:
    root = Path(__file__).resolve().parents[1] / ".tmp"
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"lmstudio_full_{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.mark.integration
@pytest.mark.slow
class TestLMStudioFullFeatures:
    """Exercise major library capabilities using only LM Studio backend."""

    def test_chat_and_stream_work(self):
        tmp_dir = _workspace_tmp_dir()
        agent = MemAgent(
            backend="lmstudio",
            model=_model_name(),
            base_url="http://localhost:1234",
            use_sql=False,
            memory_dir=str(tmp_dir / "json_memory"),
            check_connection=True,
            load_knowledge_base=False,
        )
        try:
            user_id = f"lmstudio_full_{uuid.uuid4().hex[:8]}"
            agent.set_user(user_id)

            response = agent.chat("Give a short greeting.")
            assert isinstance(response, str)
            assert len(response) > 0

            chunks = list(agent.chat_stream("Write only one sentence.", user_id=user_id))
            assert len(chunks) > 0
            assert len("".join(chunks)) > 0
        finally:
            agent.close()
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_memory_profile_history_and_metrics(self):
        tmp_dir = _workspace_tmp_dir()
        agent = MemAgent(
            backend="lmstudio",
            model=_model_name(),
            base_url="http://localhost:1234",
            use_sql=False,
            memory_dir=str(tmp_dir / "json_memory"),
            check_connection=True,
            load_knowledge_base=False,
        )
        try:
            user_id = f"lmstudio_mem_{uuid.uuid4().hex[:8]}"
            agent.set_user(user_id, name="Test User")

            _ = agent.chat("My name is Test User.")
            _ = agent.chat("Write one more line.")

            profile = agent.get_user_profile(user_id)
            assert isinstance(profile, dict)

            history = agent.search_history("Test", user_id=user_id)
            assert isinstance(history, list)

            exported = agent.export_memory(user_id=user_id, format="json")
            parsed = json.loads(exported)
            assert parsed["user_id"] == user_id
            assert "conversations" in parsed

            metrics_json = agent.export_metrics(format="json")
            metrics = json.loads(metrics_json)
            assert metrics["total_responses"] >= 1
        finally:
            agent.close()
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_tools_info_statistics_and_sql_kb(self):
        tmp_dir = _workspace_tmp_dir()
        db_path = tmp_dir / "memories.db"
        agent = MemAgent(
            backend="lmstudio",
            model=_model_name(),
            base_url="http://localhost:1234",
            use_sql=True,
            db_path=str(db_path),
            check_connection=True,
            enable_tools=True,
            load_knowledge_base=False,
        )
        try:
            user_id = f"lmstudio_sql_{uuid.uuid4().hex[:8]}"
            agent.set_user(user_id)
            _ = agent.chat("Give a short answer.")

            tools_text = agent.list_available_tools()
            assert isinstance(tools_text, str)
            assert len(tools_text) > 0

            info = agent.get_info()
            assert info["backend"] == "lmstudio"
            assert info["llm_available"] is True

            stats = agent.get_statistics()
            assert isinstance(stats, dict)

            kb_id = agent.add_knowledge(
                category="lmstudio_test",
                question="What is 2+2?",
                answer="4",
                keywords=["math", "test"],
                priority=1,
            )
            assert isinstance(kb_id, int)
            assert kb_id >= 0
        finally:
            agent.close()
            shutil.rmtree(tmp_dir, ignore_errors=True)
