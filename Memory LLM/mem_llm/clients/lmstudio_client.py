"""
LM Studio LLM Client
====================

Client for LM Studio local inference server.
LM Studio uses OpenAI-compatible API format.

Features:
- OpenAI-compatible API
- Fast local inference
- Easy model switching
- GPU acceleration support

Installation:
1. Download LM Studio from https://lmstudio.ai
2. Load a model
3. Start local server (default: http://localhost:1234)

Author: Cihat Emre Karataş
Version: 1.3.0
"""

import json
import time
from typing import Dict, Iterator, List

import requests

from ..base_llm_client import BaseLLMClient


class LMStudioClient(BaseLLMClient):
    """
    LM Studio client implementation

    LM Studio provides an OpenAI-compatible API for local models.
    This client works with any model loaded in LM Studio.

    Usage:
        client = LMStudioClient(
            model="local-model",  # or specific model name
            base_url="http://localhost:1234"
        )
        response = client.chat([{"role": "user", "content": "Hello!"}])
    """

    def __init__(
        self, model: str = "local-model", base_url: str = "http://localhost:1234", **kwargs
    ):
        """
        Initialize LM Studio client

        Args:
            model: Model identifier (use "local-model" for default loaded model)
            base_url: LM Studio server URL (default: http://localhost:1234)
            **kwargs: Additional configuration
        """
        super().__init__(model=model, **kwargs)
        self.base_url = base_url.rstrip("/")
        self.chat_url = f"{self.base_url}/v1/chat/completions"
        self.models_url = f"{self.base_url}/v1/models"

        self.logger.debug(f"Initialized LM Studio client: {base_url}, model: {model}")

    def check_connection(self) -> bool:
        """
        Check if LM Studio server is running

        Returns:
            True if server is available
        """
        try:
            response = requests.get(self.models_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.debug(f"LM Studio connection check failed: {e}")
            return False

    def list_models(self) -> List[str]:
        """
        List available models in LM Studio

        Returns:
            List of model identifiers
        """
        try:
            response = requests.get(self.models_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                return [model.get("id", "") for model in models if model.get("id")]
            return []
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return []

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """
        Send chat request to LM Studio

        Uses OpenAI-compatible chat completions endpoint.

        Args:
            messages: Message history in OpenAI format
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional OpenAI-compatible parameters
                     - top_p: Nucleus sampling (0.0-1.0)
                     - frequency_penalty: (-2.0 to 2.0)
                     - presence_penalty: (-2.0 to 2.0)
                     - stream: Enable streaming (bool)

        Returns:
            Model response text

        Raises:
            ConnectionError: If cannot connect to LM Studio
            ValueError: If invalid parameters
        """
        # Validate messages
        self._validate_messages(messages)

        # Build OpenAI-compatible payload
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": kwargs.get("stream", False),
        }

        # Add optional parameters
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]
        if "frequency_penalty" in kwargs:
            payload["frequency_penalty"] = kwargs["frequency_penalty"]
        if "presence_penalty" in kwargs:
            payload["presence_penalty"] = kwargs["presence_penalty"]
        if "stop" in kwargs:
            payload["stop"] = kwargs["stop"]

        # Send request with retry logic
        max_retries = kwargs.get("max_retries", 3)
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.chat_url, json=payload, timeout=kwargs.get("timeout", 120)
                )

                if response.status_code == 200:
                    response_data = response.json()

                    # Extract content from OpenAI format
                    choices = response_data.get("choices", [])
                    if not choices:
                        self.logger.warning("No choices in LM Studio response")
                        if attempt < max_retries - 1:
                            time.sleep(1.0 * (2**attempt))
                            continue
                        return ""

                    # Get the message content
                    message = choices[0].get("message", {})
                    content = message.get("content", "").strip()

                    if not content:
                        self.logger.warning("Empty content in LM Studio response")
                        if attempt < max_retries - 1:
                            time.sleep(1.0 * (2**attempt))
                            continue

                    # Log usage statistics if available
                    usage = response_data.get("usage", {})
                    if usage:
                        self.logger.debug(
                            f"LM Studio usage - "
                            f"prompt: {usage.get('prompt_tokens', 0)} tokens, "
                            f"completion: {usage.get('completion_tokens', 0)} tokens, "
                            f"total: {usage.get('total_tokens', 0)} tokens"
                        )

                    return content

                else:
                    error_msg = f"LM Studio API error: {response.status_code}"
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
                self.logger.warning(
                    f"LM Studio request timeout (attempt {attempt + 1}/{max_retries})"
                )
                if attempt < max_retries - 1:
                    time.sleep(2.0 * (2**attempt))
                    continue
                raise ConnectionError("LM Studio request timeout. Check if server is running.")

            except requests.exceptions.ConnectionError as e:
                self.logger.warning(
                    f"Cannot connect to LM Studio (attempt {attempt + 1}/{max_retries})"
                )
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                raise ConnectionError(
                    f"Cannot connect to LM Studio at {self.base_url}. "
                    "Make sure LM Studio is running and server is started."
                ) from e

            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                raise

        raise ConnectionError("Failed to get response after maximum retries")

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> Iterator[str]:
        """
        Send chat request to LM Studio with streaming response

        Uses OpenAI-compatible streaming format.

        Args:
            messages: Message history in OpenAI format
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional OpenAI-compatible parameters

        Yields:
            Response text chunks as they arrive

        Raises:
            ConnectionError: If cannot connect to LM Studio
            ValueError: If invalid parameters
        """
        # Validate messages
        self._validate_messages(messages)

        # Build OpenAI-compatible payload
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,  # Enable streaming
        }

        # Add optional parameters
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]
        if "frequency_penalty" in kwargs:
            payload["frequency_penalty"] = kwargs["frequency_penalty"]
        if "presence_penalty" in kwargs:
            payload["presence_penalty"] = kwargs["presence_penalty"]
        if "stop" in kwargs:
            payload["stop"] = kwargs["stop"]

        try:
            response = requests.post(
                self.chat_url,
                json=payload,
                stream=True,  # Enable streaming
                timeout=kwargs.get("timeout", 120),
            )

            if response.status_code == 200:
                # Process OpenAI-compatible streaming response
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode("utf-8")

                        # Skip empty lines
                        if not line_text.strip():
                            continue

                        # OpenAI format uses "data: " prefix
                        if line_text.startswith("data: "):
                            line_text = line_text[6:]  # Remove "data: " prefix

                        # Check for stream end
                        if line_text.strip() == "[DONE]":
                            break

                        try:
                            chunk_data = json.loads(line_text)

                            # Extract content from OpenAI format
                            choices = chunk_data.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")

                                if content:
                                    yield content

                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Failed to parse streaming chunk: {e}")
                            continue
            else:
                error_msg = f"LM Studio API error: {response.status_code}"
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
                raise ConnectionError(error_msg)

        except requests.exceptions.Timeout:
            raise ConnectionError("LM Studio request timeout. Check if server is running.")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot connect to LM Studio at {self.base_url}. "
                "Make sure LM Studio is running and server is started."
            ) from e
        except Exception as e:
            self.logger.error(f"Unexpected error in streaming: {e}")
            raise

    def get_model_info(self) -> Dict:
        """
        Get information about currently loaded model

        Returns:
            Dictionary with model information
        """
        try:
            response = requests.get(self.models_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])

                # Find our model or return first one
                for model in models:
                    if model.get("id") == self.model:
                        return model

                # Return first model if ours not found
                return models[0] if models else {}
            return {}
        except Exception as e:
            self.logger.error(f"Failed to get model info: {e}")
            return {}

    def get_info(self) -> Dict:
        """
        Get comprehensive client information

        Returns:
            Dictionary with client and model metadata
        """
        base_info = super().get_info()

        # Add LM Studio specific info
        if self.check_connection():
            model_info = self.get_model_info()
            base_info["model_details"] = model_info
            base_info["available_models"] = self.list_models()

        return base_info
