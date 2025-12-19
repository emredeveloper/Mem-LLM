"""
LLM Client - Local model integration with Ollama
Works with Granite4:tiny-h model
"""

import time
from typing import Dict, List, Optional

import requests


class OllamaClient:
    """Uses local LLM model with Ollama API"""

    def __init__(self, model: str = "granite4:3b", base_url: str = "http://localhost:11434"):
        """
        Args:
            model: Model name to use
            base_url: Ollama API URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"

    def check_connection(self) -> bool:
        """
        Checks if Ollama service is running

        Returns:
            Is service running?
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """
        List available models

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception:
            return []

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """
        Generate simple text

        Args:
            prompt: User prompt (not AI system prompt)
            system_prompt: AI system prompt
            temperature: Creativity level (0-1)
            max_tokens: Maximum token count

        Returns:
            Model output
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        if system_prompt:
            payload["system"] = system_prompt

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, json=payload, timeout=60)
                if response.status_code == 200:
                    return response.json().get("response", "").strip()
                else:
                    if attempt < max_retries - 1:
                        time.sleep(1.0 * (2**attempt))  # Exponential backoff
                        continue
                    return f"Error: {response.status_code} - {response.text}"
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2.0 * (2**attempt))
                    continue
                return "Error: Request timeout. Please check if Ollama is running."
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                return "Error: Cannot connect to Ollama. Make sure Ollama service is running."
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2**attempt))
                    continue
                return f"Connection error: {str(e)}"

    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2000
    ) -> str:
        """
        Chat format interaction - Compatible with ALL Ollama models

        Args:
            messages: Message history [{"role": "user/assistant/system", "content": "..."}]
            temperature: Creativity level
            max_tokens: Maximum token count

        Returns:
            Model response
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 4096,  # Context window
                "top_k": 40,  # Limit vocab
                "top_p": 0.9,  # Nucleus sampling
                "num_thread": 8,  # Parallel processing
            },
        }

        # For thinking-enabled models (like qwen3), disable thinking mode
        # to get direct answers instead of reasoning process
        if "qwen" in self.model.lower() or "deepseek" in self.model.lower():
            payload["options"]["enable_thinking"] = False

        try:
            response = requests.post(self.chat_url, json=payload, timeout=120)
            if response.status_code == 200:
                response_data = response.json()
                message = response_data.get("message", {})

                # Get content - primary response field
                result = message.get("content", "").strip()

                # Fallback: If content is empty but thinking exists
                # This happens when thinking mode couldn't be disabled
                if not result and message.get("thinking"):
                    thinking = message.get("thinking", "")

                    # Try to extract the actual answer from thinking process
                    # Usually the answer is at the end after reasoning
                    if thinking:
                        # Split by common patterns that indicate final answer
                        for separator in [
                            "\n\nAnswer:",
                            "\n\nFinal answer:",
                            "\n\nResponse:",
                            "\n\nSo the answer is:",
                            "\n\n---\n",
                            "\n\nOkay,",
                        ]:
                            if separator in thinking:
                                parts = thinking.split(separator)
                                if len(parts) > 1:
                                    result = parts[-1].strip()
                                    break

                        # If no separator found, try to get last meaningful paragraph
                        if not result:
                            paragraphs = [p.strip() for p in thinking.split("\n\n") if p.strip()]
                            if paragraphs:
                                # Take the last paragraph as likely answer
                                last_para = paragraphs[-1]
                                # Avoid meta-commentary like "Wait, let me think..."
                                if not any(
                                    word in last_para.lower()
                                    for word in ["wait", "hmm", "let me", "thinking", "okay"]
                                ):
                                    result = last_para

                return result
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Connection error: {str(e)}"

    def generate_with_memory_context(
        self, user_message: str, memory_summary: str, recent_conversations: List[Dict]
    ) -> str:
        """
        Generate response with memory context

        Args:
            user_message: User's message
            memory_summary: User memory summary
            recent_conversations: Recent conversations

        Returns:
            Context-aware response
        """
        # Create system prompt
        system_prompt = """You are a helpful customer service assistant.
You can remember past conversations with users.
Give short, clear and professional answers.
Use past interactions intelligently."""

        # Create message history
        messages = [{"role": "system", "content": system_prompt}]

        # Add memory summary
        if memory_summary and memory_summary != "No interactions with this user yet.":
            messages.append({"role": "system", "content": f"User history:\n{memory_summary}"})

        # Add recent conversations
        for conv in recent_conversations[-3:]:
            messages.append({"role": "user", "content": conv.get("user_message", "")})
            messages.append({"role": "assistant", "content": conv.get("bot_response", "")})

        # Add current message
        messages.append({"role": "user", "content": user_message})

        return self.chat(messages, temperature=0.7)
