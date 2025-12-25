"""
Base LLM Client Interface
==========================

Abstract base class for all LLM client implementations.
Ensures consistent interface across different backends (Ollama, LM Studio)

Author: Cihat Emre Karataş
Version: 1.3.0
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients

    All LLM backends must implement these methods to ensure
    compatibility with MemAgent and other components.
    """

    def __init__(self, model: str = None, **kwargs):
        """
        Initialize LLM client

        Args:
            model: Model name/identifier
            **kwargs: Backend-specific configuration
        """
        self.model = model
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """
        Send chat request and return response

        Args:
            messages: List of messages in format:
                     [{"role": "system/user/assistant", "content": "..."}]
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional backend-specific parameters

        Returns:
            Model response text

        Raises:
            ConnectionError: If cannot connect to service
            ValueError: If invalid parameters
        """
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        """
        Check if LLM service is available and responding

        Returns:
            True if service is available, False otherwise
        """
        pass

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> Iterator[str]:
        """
        Send chat request and stream response chunks (optional, not all backends support)

        Args:
            messages: List of messages in format:
                     [{"role": "system/user/assistant", "content": "..."}]
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional backend-specific parameters

        Yields:
            Response text chunks as they arrive

        Raises:
            NotImplementedError: If backend doesn't support streaming
            ConnectionError: If cannot connect to service
            ValueError: If invalid parameters
        """
        # Default implementation: fall back to non-streaming
        response = self.chat(messages, temperature, max_tokens, **kwargs)
        yield response

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs,
    ) -> str:
        """
        Generate text from a simple prompt (convenience method)

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        # Convert to chat format
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self.chat(messages, temperature, max_tokens, **kwargs)

    def list_models(self) -> List[str]:
        """
        List available models (optional, not all backends support this)

        Returns:
            List of model names
        """
        return [self.model] if self.model else []

    def _format_messages_to_text(self, messages: List[Dict]) -> str:
        """
        Helper: Convert message list to text format

        Useful for backends that don't support chat format natively.

        Args:
            messages: Message list

        Returns:
            Formatted text prompt
        """
        result = []
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "").strip()
            if content:
                result.append(f"{role}: {content}")
        return "\n\n".join(result)

    def _validate_messages(self, messages: List[Dict]) -> bool:
        """
        Validate message format

        Args:
            messages: Messages to validate

        Returns:
            True if valid

        Raises:
            ValueError: If invalid format
        """
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")

        if not messages:
            raise ValueError("Messages list cannot be empty")

        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"Message {i} must be a dictionary")

            if "role" not in msg:
                raise ValueError(f"Message {i} missing 'role' field")

            if "content" not in msg:
                raise ValueError(f"Message {i} missing 'content' field")

            if msg["role"] not in ["system", "user", "assistant"]:
                raise ValueError(f"Message {i} has invalid role: {msg['role']}")

        return True

    def get_info(self) -> Dict[str, Any]:
        """
        Get client information

        Returns:
            Dictionary with client metadata
        """
        return {
            "backend": self.__class__.__name__,
            "model": self.model,
            "available": self.check_connection(),
        }

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(model='{self.model}')"
