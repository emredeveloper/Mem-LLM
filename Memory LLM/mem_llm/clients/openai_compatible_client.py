"""
OpenAI-compatible LLM Client
============================

Client for local or remote servers that expose the OpenAI chat completions API.
Works with LM Studio, llama.cpp server, vLLM, LocalAI, text-generation-webui, and
similar runtimes.
"""

import json
import time
from typing import Dict, Iterator, List, Optional

import requests

from ..base_llm_client import BaseLLMClient


class OpenAICompatibleClient(BaseLLMClient):
    """Generic OpenAI-compatible chat completions client."""

    def __init__(
        self,
        model: str = "local-model",
        base_url: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model=model, **kwargs)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.chat_url = f"{self.base_url}/v1/chat/completions"
        self.models_url = f"{self.base_url}/v1/models"

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def check_connection(self) -> bool:
        try:
            response = requests.get(self.models_url, headers=self._headers(), timeout=5)
            if response.status_code == 200:
                return True

            # Some compatible servers expose chat without a models endpoint.
            response = requests.post(
                self.chat_url,
                headers=self._headers(),
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "ping"}],
                    "max_tokens": 1,
                    "temperature": 0,
                    "stream": False,
                },
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.debug(f"OpenAI-compatible connection check failed: {e}")
            return False

    def list_models(self) -> List[str]:
        try:
            response = requests.get(self.models_url, headers=self._headers(), timeout=5)
            if response.status_code != 200:
                return [self.model] if self.model else []

            data = response.json()
            models = data.get("data", [])
            names = [model.get("id", "") for model in models if model.get("id")]
            return names or ([self.model] if self.model else [])
        except Exception as e:
            self.logger.error(f"Failed to list OpenAI-compatible models: {e}")
            return [self.model] if self.model else []

    def _build_payload(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        stream: bool,
        **kwargs,
    ) -> Dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        for key in (
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "seed",
            "response_format",
        ):
            if key in kwargs:
                payload[key] = kwargs[key]

        return payload

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        self._validate_messages(messages)
        payload = self._build_payload(messages, temperature, max_tokens, stream=False, **kwargs)

        max_retries = kwargs.get("max_retries", 3)
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.chat_url,
                    headers=self._headers(),
                    json=payload,
                    timeout=kwargs.get("timeout", 120),
                )

                if response.status_code == 200:
                    response_data = response.json()
                    choices = response_data.get("choices", [])
                    if not choices:
                        self.logger.warning("No choices in OpenAI-compatible response")
                        return ""

                    message = choices[0].get("message", {})
                    return message.get("content", "").strip()

                error_msg = f"OpenAI-compatible API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", {})
                    if isinstance(error_detail, dict):
                        error_msg += f" - {error_detail.get('message', response.text)}"
                    else:
                        error_msg += f" - {error_detail}"
                except (ValueError, json.JSONDecodeError):
                    error_msg += f" - {response.text[:200]}"

                self.logger.error(error_msg)
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                raise ConnectionError(error_msg)

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2.0 * (2**attempt))
                    continue
                raise ConnectionError("OpenAI-compatible request timeout.")
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                raise ConnectionError(
                    f"Cannot connect to OpenAI-compatible server at {self.base_url}."
                ) from e

        raise ConnectionError("Failed to get response after maximum retries")

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> Iterator[str]:
        self._validate_messages(messages)
        payload = self._build_payload(messages, temperature, max_tokens, stream=True, **kwargs)

        try:
            response = requests.post(
                self.chat_url,
                headers=self._headers(),
                json=payload,
                stream=True,
                timeout=kwargs.get("timeout", 120),
            )

            if response.status_code != 200:
                raise ConnectionError(
                    f"OpenAI-compatible API error: {response.status_code} - {response.text[:200]}"
                )

            for line in response.iter_lines():
                if not line:
                    continue

                line_text = line.decode("utf-8").strip()
                if line_text.startswith("data: "):
                    line_text = line_text[6:]
                if line_text == "[DONE]":
                    break

                try:
                    chunk_data = json.loads(line_text)
                except json.JSONDecodeError:
                    continue

                choices = chunk_data.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot connect to OpenAI-compatible server at {self.base_url}."
            ) from e


class LlamaCppClient(OpenAICompatibleClient):
    """OpenAI-compatible client configured for llama.cpp server defaults."""

    def __init__(
        self,
        model: str = "llama.cpp",
        base_url: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model=model, base_url=base_url, api_key=api_key, **kwargs)
