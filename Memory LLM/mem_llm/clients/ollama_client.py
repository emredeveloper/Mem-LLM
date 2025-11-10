"""
Ollama LLM Client
=================

Client for local Ollama service.
Supports all Ollama models (Llama3, Granite, Qwen3, DeepSeek, etc.)

Author: C. Emre Karataş
Version: 1.3.0
"""

import requests
import time
import json
from typing import List, Dict, Optional, Iterator
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_llm_client import BaseLLMClient


class OllamaClient(BaseLLMClient):
    """
    Ollama LLM client implementation
    
    Supports:
    - All Ollama models
    - Chat and generate modes
    - Thinking mode detection (Qwen3, DeepSeek)
    - Automatic retry with exponential backoff
    """
    
    def __init__(self, 
                 model: str = "granite4:3b",
                 base_url: str = "http://localhost:11434",
                 **kwargs):
        """
        Initialize Ollama client
        
        Args:
            model: Model name (e.g., "llama3", "granite4:3b")
            base_url: Ollama API URL
            **kwargs: Additional configuration
        """
        super().__init__(model=model, **kwargs)
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
        self.tags_url = f"{base_url}/api/tags"
        
        self.logger.debug(f"Initialized Ollama client: {base_url}, model: {model}")
    
    def check_connection(self) -> bool:
        """
        Check if Ollama service is running
        
        Returns:
            True if service is available
        """
        try:
            response = requests.get(self.tags_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.debug(f"Ollama connection check failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """
        List available Ollama models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(self.tags_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return []
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             temperature: float = 0.7, 
             max_tokens: int = 2000,
             **kwargs) -> str:
        """
        Send chat request to Ollama
        
        Args:
            messages: Message history
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional Ollama-specific options
            
        Returns:
            Model response text
            
        Raises:
            ConnectionError: If cannot connect to Ollama
            ValueError: If invalid parameters
        """
        # Validate messages
        self._validate_messages(messages)
        
        # Build payload
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": kwargs.get("num_ctx", 4096),
                "top_k": kwargs.get("top_k", 40),
                "top_p": kwargs.get("top_p", 0.9),
                "num_thread": kwargs.get("num_thread", 8)
            }
        }
        
        # Disable thinking mode for thinking-enabled models
        # (Qwen3, DeepSeek) to get direct answers
        if any(name in self.model.lower() for name in ['qwen', 'deepseek', 'qwq']):
            payload["options"]["enable_thinking"] = False
        
        # Send request with retry logic
        max_retries = kwargs.get("max_retries", 3)
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.chat_url, 
                    json=payload, 
                    timeout=kwargs.get("timeout", 120)
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    message = response_data.get('message', {})
                    
                    # Get content - primary response field
                    result = message.get('content', '').strip()
                    
                    # Fallback: Extract from thinking if content is empty
                    if not result and message.get('thinking'):
                        result = self._extract_from_thinking(message.get('thinking', ''))
                    
                    if not result:
                        self.logger.warning("Empty response from Ollama")
                        if attempt < max_retries - 1:
                            time.sleep(1.0 * (2 ** attempt))
                            continue
                    
                    return result
                else:
                    error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    if attempt < max_retries - 1:
                        time.sleep(1.0 * (2 ** attempt))
                        continue
                    raise ConnectionError(error_msg)
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Ollama request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2.0 * (2 ** attempt))
                    continue
                raise ConnectionError("Ollama request timeout. Check if service is running.")
                
            except requests.exceptions.ConnectionError as e:
                self.logger.warning(f"Cannot connect to Ollama (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2 ** attempt))
                    continue
                raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}. Make sure service is running.") from e
                
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2 ** attempt))
                    continue
                raise
        
        raise ConnectionError("Failed to get response after maximum retries")
    
    def _extract_from_thinking(self, thinking: str) -> str:
        """
        Extract actual answer from thinking process
        
        Some models output reasoning process instead of direct answer.
        This extracts the final answer from that process.
        
        Args:
            thinking: Thinking process text
            
        Returns:
            Extracted answer
        """
        if not thinking:
            return ""
        
        # Try to find answer after common separators
        for separator in ['\n\nAnswer:', '\n\nFinal answer:', 
                         '\n\nResponse:', '\n\nSo the answer is:',
                         '\n\n---\n', '\n\nOkay,', '\n\nTherefore,']:
            if separator in thinking:
                parts = thinking.split(separator)
                if len(parts) > 1:
                    return parts[-1].strip()
        
        # Fallback: Get last meaningful paragraph
        paragraphs = [p.strip() for p in thinking.split('\n\n') if p.strip()]
        if paragraphs:
            last_para = paragraphs[-1]
            # Avoid meta-commentary
            if not any(word in last_para.lower() 
                      for word in ['wait', 'hmm', 'let me', 'thinking', 'okay']):
                return last_para
        
        # If nothing else works, return the whole thinking
        return thinking
    
    def chat_stream(self, 
                    messages: List[Dict[str, str]], 
                    temperature: float = 0.7, 
                    max_tokens: int = 2000,
                    **kwargs) -> Iterator[str]:
        """
        Send chat request to Ollama with streaming response
        
        Args:
            messages: Message history
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional Ollama-specific options
            
        Yields:
            Response text chunks as they arrive
            
        Raises:
            ConnectionError: If cannot connect to Ollama
            ValueError: If invalid parameters
        """
        # Validate messages
        self._validate_messages(messages)
        
        # Build payload
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,  # Enable streaming
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": kwargs.get("num_ctx", 4096),
                "top_k": kwargs.get("top_k", 40),
                "top_p": kwargs.get("top_p", 0.9),
                "num_thread": kwargs.get("num_thread", 8)
            }
        }
        
        # Disable thinking mode for thinking-enabled models
        if any(name in self.model.lower() for name in ['qwen', 'deepseek', 'qwq']):
            payload["options"]["enable_thinking"] = False
        
        try:
            response = requests.post(
                self.chat_url,
                json=payload,
                stream=True,  # Enable streaming
                timeout=kwargs.get("timeout", 120)
            )
            
            if response.status_code == 200:
                # Process streaming response
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk_data = json.loads(line.decode('utf-8'))
                            
                            # Get message content
                            message = chunk_data.get('message', {})
                            content = message.get('content', '')
                            
                            if content:
                                yield content
                            
                            # Check if this is the final chunk
                            if chunk_data.get('done', False):
                                break
                                
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Failed to parse streaming chunk: {e}")
                            continue
            else:
                error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise ConnectionError(error_msg)
                
        except requests.exceptions.Timeout:
            raise ConnectionError("Ollama request timeout. Check if service is running.")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}. Make sure service is running.") from e
        except Exception as e:
            self.logger.error(f"Unexpected error in streaming: {e}")
            raise
    
    def generate_with_memory_context(self, 
                                    user_message: str, 
                                    memory_summary: str,
                                    recent_conversations: List[Dict]) -> str:
        """
        Generate response with memory context
        
        This is a specialized method for MemAgent integration.
        
        Args:
            user_message: User's message
            memory_summary: Summary of past interactions
            recent_conversations: Recent conversation history
            
        Returns:
            Context-aware response
        """
        # Build system prompt
        system_prompt = """You are a helpful customer service assistant.
You can remember past conversations with users.
Give short, clear and professional answers.
Use past interactions intelligently."""
        
        # Build message history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add memory summary
        if memory_summary and memory_summary != "No interactions with this user yet.":
            messages.append({
                "role": "system",
                "content": f"User history:\n{memory_summary}"
            })
        
        # Add recent conversations (last 3)
        for conv in recent_conversations[-3:]:
            messages.append({"role": "user", "content": conv.get('user_message', '')})
            messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        return self.chat(messages, temperature=0.7)

