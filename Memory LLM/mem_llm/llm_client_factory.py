"""
LLM Client Factory
==================

Factory pattern for creating LLM clients.
Supports multiple backends with automatic detection.

Supported Backends:
- Ollama: Local Ollama service
- LM Studio: Local LM Studio server

Usage:
    # Create specific backend
    client = LLMClientFactory.create('ollama', model='llama3')

    # Auto-detect available backend
    client = LLMClientFactory.auto_detect()

    # Get all available backends
    backends = LLMClientFactory.get_available_backends()

Author: C. Emre Karataş
Version: 1.3.0
"""

import logging
from typing import Any, Dict, List, Optional

from .base_llm_client import BaseLLMClient
from .clients.lmstudio_client import LMStudioClient
from .clients.ollama_client import OllamaClient


class LLMClientFactory:
    """
    Factory for creating LLM clients

    Provides unified interface for creating different LLM backends.
    Supports auto-detection of available local services.
    """

    # Registry of supported backends
    BACKENDS = {
        "ollama": {
            "class": OllamaClient,
            "description": "Local Ollama service",
            "type": "local",
            "default_url": "http://localhost:11434",
            "default_model": "granite4:3b",
        },
        "lmstudio": {
            "class": LMStudioClient,
            "description": "LM Studio local server (OpenAI-compatible)",
            "type": "local",
            "default_url": "http://localhost:1234",
            "default_model": "local-model",
        },
    }

    @staticmethod
    def create(backend: str, model: Optional[str] = None, **kwargs) -> BaseLLMClient:
        """
        Create LLM client for specified backend

        Args:
            backend: Backend name ('ollama', 'lmstudio')
            model: Model name (uses default if None)
            **kwargs: Backend-specific configuration
                     - base_url: API endpoint (for local backends)
                     - temperature: Default temperature
                     - max_tokens: Default max tokens

        Returns:
            Configured LLM client

        Raises:
            ValueError: If backend is not supported

        Examples:
            # Ollama
            client = LLMClientFactory.create('ollama', model='llama3')

            # LM Studio
            client = LLMClientFactory.create(
                'lmstudio',
                model='llama-3-8b',
                base_url='http://localhost:1234'
            )
        """
        backend = backend.lower()

        if backend not in LLMClientFactory.BACKENDS:
            available = ", ".join(LLMClientFactory.BACKENDS.keys())
            raise ValueError(
                f"Unsupported backend: '{backend}'. " f"Available backends: {available}"
            )

        backend_info = LLMClientFactory.BACKENDS[backend]
        client_class = backend_info["class"]

        # Use default model if not specified
        if not model:
            model = backend_info.get("default_model")

        # Add default base_url for local backends if not provided
        if backend_info["type"] == "local" and "base_url" not in kwargs:
            kwargs["base_url"] = backend_info.get("default_url")

        # Create and return client
        try:
            return client_class(model=model, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create {backend} client: {str(e)}") from e

    @staticmethod
    def auto_detect(preferred_backends: Optional[List[str]] = None) -> Optional[BaseLLMClient]:
        """
        Auto-detect available LLM service

        Checks common local services and returns the first available one.
        Useful for applications that should work with any available backend.

        Args:
            preferred_backends: List of backends to check in order
                              (if None, checks all in default order)

        Returns:
            First available LLM client, or None if none available

        Example:
            # Try to find any available backend
            client = LLMClientFactory.auto_detect()
            if client:
                print(f"Using {client.get_info()['backend']}")
            else:
                print("No LLM service found")

            # Try specific backends in order
            client = LLMClientFactory.auto_detect(['lmstudio', 'ollama'])
        """
        logger = logging.getLogger("LLMClientFactory")

        # Default check order: local services first
        if preferred_backends is None:
            preferred_backends = ["ollama", "lmstudio"]

        for backend_name in preferred_backends:
            if backend_name not in LLMClientFactory.BACKENDS:
                logger.warning(f"Unknown backend in auto-detect: {backend_name}")
                continue

            backend_info = LLMClientFactory.BACKENDS[backend_name]

            # Skip cloud services in auto-detect (they require API keys)
            if backend_info["type"] == "cloud":
                logger.debug(f"Skipping cloud backend in auto-detect: {backend_name}")
                continue

            try:
                # Try to create client with defaults
                client = LLMClientFactory.create(backend_name)

                # Check if service is actually running
                if client.check_connection():
                    logger.info(f"✅ Detected {backend_name} at {backend_info.get('default_url')}")
                    return client
                else:
                    logger.debug(f"Service not running: {backend_name}")

            except Exception as e:
                logger.debug(f"Failed to detect {backend_name}: {e}")
                continue

        logger.warning("⚠️  No local LLM service detected")
        return None

    @staticmethod
    def get_available_backends() -> List[Dict[str, Any]]:
        """
        Get list of all supported backends with their info

        Returns:
            List of backend information dictionaries

        Example:
            backends = LLMClientFactory.get_available_backends()
            for backend in backends:
                print(f"{backend['name']}: {backend['description']}")
        """
        result = []

        for name, info in LLMClientFactory.BACKENDS.items():
            backend_dict = {
                "name": name,
                "description": info["description"],
                "type": info["type"],
                "default_model": info.get("default_model"),
                "requires_api_key": info.get("requires_api_key", False),
            }

            if info["type"] == "local":
                backend_dict["default_url"] = info.get("default_url")

            result.append(backend_dict)

        return result

    @staticmethod
    def check_backend_availability(backend: str, **kwargs) -> bool:
        """
        Check if a specific backend is available

        Args:
            backend: Backend name
            **kwargs: Configuration for creating the client

        Returns:
            True if backend is available and responding

        Example:
            # Check if Ollama is running
            if LLMClientFactory.check_backend_availability('ollama'):
                print("Ollama is available")

            # Check custom LM Studio URL
            if LLMClientFactory.check_backend_availability(
                'lmstudio',
                base_url='http://localhost:5000'
            ):
                print("LM Studio is available")
        """
        try:
            client = LLMClientFactory.create(backend, **kwargs)
            return client.check_connection()
        except Exception:
            return False

    @staticmethod
    def get_backend_info(backend: str) -> Dict[str, Any]:
        """
        Get information about a specific backend

        Args:
            backend: Backend name

        Returns:
            Backend information dictionary

        Raises:
            ValueError: If backend not found
        """
        if backend not in LLMClientFactory.BACKENDS:
            raise ValueError(f"Unknown backend: {backend}")

        info = LLMClientFactory.BACKENDS[backend].copy()
        # Remove class reference for JSON serialization
        info.pop("class", None)
        return info
