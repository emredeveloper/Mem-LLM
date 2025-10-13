"""
LLM Client - Local model integration with Ollama
Works with Granite4:tiny-h model
"""

import requests
import json
from typing import List, Dict, Optional


class OllamaClient:
    """Uses local LLM model with Ollama API"""
    
    def __init__(self, model: str = "granite4:tiny-h", 
                 base_url: str = "http://localhost:11434"):
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
        except:
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
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.7, max_tokens: int = 500) -> str:
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
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Connection error: {str(e)}"
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Chat format interaction
        
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
                "num_ctx": 2048,  # Context window
                "top_k": 40,  # Limit vocab
                "top_p": 0.9,  # Nucleus sampling
                "stop": ["\n\n\n", "---"]  # Stop sequences
            }
        }
        
        try:
            response = requests.post(self.chat_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '').strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Connection error: {str(e)}"
    
    def generate_with_memory_context(self, user_message: str, 
                                     memory_summary: str,
                                     recent_conversations: List[Dict]) -> str:
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
            messages.append({
                "role": "system",
                "content": f"User history:\n{memory_summary}"
            })
        
        # Add recent conversations
        for conv in recent_conversations[-3:]:
            messages.append({"role": "user", "content": conv.get('user_message', '')})
            messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        return self.chat(messages, temperature=0.7)

