"""
LLM Client - Ollama ile yerel model entegrasyonu
Granite4:tiny-h modeli ile çalışır
"""

import requests
import json
from typing import List, Dict, Optional


class OllamaClient:
    """Ollama API ile yerel LLM modelini kullanır"""
    
    def __init__(self, model: str = "granite4:tiny-h", 
                 base_url: str = "http://localhost:11434"):
        """
        Args:
            model: Kullanılacak model adı
            base_url: Ollama API URL'i
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
        
    def check_connection(self) -> bool:
        """
        Ollama servisinin çalıştığını kontrol eder
        
        Returns:
            Servis çalışıyor mu?
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """
        Mevcut modelleri listeler
        
        Returns:
            Model isimleri listesi
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
        Basit metin üretimi yapar
        
        Args:
            prompt: Kullanıcı promptu (AI system promptu değil)
            system_prompt: AI sistem promptu
            temperature: Yaratıcılık derecesi (0-1)
            max_tokens: Maksimum token sayısı
            
        Returns:
            Model çıktısı
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
                return f"Hata: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Bağlantı hatası: {str(e)}"
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Konuşma formatında etkileşim
        
        Args:
            messages: Mesaj geçmişi [{"role": "user/assistant/system", "content": "..."}]
            temperature: Yaratıcılık derecesi
            max_tokens: Maksimum token sayısı
            
        Returns:
            Model cevabı
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(self.chat_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '').strip()
            else:
                return f"Hata: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Bağlantı hatası: {str(e)}"
    
    def generate_with_memory_context(self, user_message: str, 
                                     memory_summary: str,
                                     recent_conversations: List[Dict]) -> str:
        """
        Bellek bağlamı ile cevap üretir
        
        Args:
            user_message: Kullanıcının mesajı
            memory_summary: Kullanıcı bellek özeti
            recent_conversations: Son konuşmalar
            
        Returns:
            Bağlam farkındalığı olan cevap
        """
        # Sistem promptu oluştur
        system_prompt = """Sen yardımsever bir müşteri hizmetleri asistanısın. 
Kullanıcılarla yaptığın geçmiş konuşmaları hatırlayabiliyorsun.
Kısa, net ve profesyonel cevaplar ver.
Geçmiş etkileşimleri akıllıca kullan."""
        
        # Mesaj geçmişini oluştur
        messages = [{"role": "system", "content": system_prompt}]
        
        # Bellek özetini ekle
        if memory_summary and memory_summary != "Bu kullanıcı ile henüz bir etkileşim yok.":
            messages.append({
                "role": "system",
                "content": f"Kullanıcı geçmişi:\n{memory_summary}"
            })
        
        # Son konuşmaları ekle
        for conv in recent_conversations[-3:]:
            messages.append({"role": "user", "content": conv.get('user_message', '')})
            messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        
        # Şimdiki mesajı ekle
        messages.append({"role": "user", "content": user_message})
        
        return self.chat(messages, temperature=0.7)

