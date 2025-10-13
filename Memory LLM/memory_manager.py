"""
Memory Manager - Bellek Yönetim Sistemi
Kullanıcı etkileşimlerini saklar, günceller ve hatırlar.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class MemoryManager:
    """Kullanıcı etkileşimlerini ve bağlamı yöneten bellek sistemi"""
    
    def __init__(self, memory_dir: str = "memories"):
        """
        Args:
            memory_dir: Bellek dosyalarının saklanacağı dizin
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        self.conversations: Dict[str, List[Dict]] = {}
        self.user_profiles: Dict[str, Dict] = {}
        
    def _get_user_file(self, user_id: str) -> Path:
        """Kullanıcının bellek dosyasının yolunu döndürür"""
        return self.memory_dir / f"{user_id}.json"
    
    def load_memory(self, user_id: str) -> Dict:
        """
        Kullanıcının belleğini yükler
        
        Args:
            user_id: Kullanıcı kimliği
            
        Returns:
            Kullanıcının bellek verisi
        """
        user_file = self._get_user_file(user_id)
        
        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversations[user_id] = data.get('conversations', [])
                self.user_profiles[user_id] = data.get('profile', {})
                return data
        else:
            # Yeni kullanıcı için boş bellek oluştur
            self.conversations[user_id] = []
            self.user_profiles[user_id] = {
                'user_id': user_id,
                'first_seen': datetime.now().isoformat(),
                'preferences': {},
                'summary': {}
            }
            return {
                'conversations': [],
                'profile': self.user_profiles[user_id]
            }
    
    def save_memory(self, user_id: str) -> None:
        """
        Kullanıcının belleğini diske kaydeder
        
        Args:
            user_id: Kullanıcı kimliği
        """
        user_file = self._get_user_file(user_id)
        
        data = {
            'conversations': self.conversations.get(user_id, []),
            'profile': self.user_profiles.get(user_id, {}),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_interaction(self, user_id: str, user_message: str, 
                       bot_response: str, metadata: Optional[Dict] = None) -> None:
        """
        Yeni bir etkileşim kaydeder
        
        Args:
            user_id: Kullanıcı kimliği
            user_message: Kullanıcının mesajı
            bot_response: Botun cevabı
            metadata: Ek bilgiler (sipariş no, sorun türü vb.)
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'metadata': metadata or {}
        }
        
        self.conversations[user_id].append(interaction)
        self.save_memory(user_id)
    
    def update_profile(self, user_id: str, updates: Dict) -> None:
        """
        Kullanıcı profilini günceller
        
        Args:
            user_id: Kullanıcı kimliği
            updates: Güncellenecek bilgiler
        """
        if user_id not in self.user_profiles:
            self.load_memory(user_id)
        
        self.user_profiles[user_id].update(updates)
        self.save_memory(user_id)
    
    def get_recent_conversations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """
        Son N konuşmayı getirir
        
        Args:
            user_id: Kullanıcı kimliği
            limit: Getir​ilecek konuşma sayısı
            
        Returns:
            Son konuşmalar listesi
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)
        
        return self.conversations[user_id][-limit:]
    
    def search_memory(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Bellekte anahtar kelime araması yapar
        
        Args:
            user_id: Kullanıcı kimliği
            keyword: Aranacak kelime
            
        Returns:
            Eşleşen etkileşimler
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)
        
        results = []
        keyword_lower = keyword.lower()
        
        for interaction in self.conversations[user_id]:
            if (keyword_lower in interaction['user_message'].lower() or 
                keyword_lower in interaction['bot_response'].lower() or
                keyword_lower in str(interaction.get('metadata', {})).lower()):
                results.append(interaction)
        
        return results
    
    def get_summary(self, user_id: str) -> str:
        """
        Kullanıcının geçmiş etkileşimlerinin özetini oluşturur
        
        Args:
            user_id: Kullanıcı kimliği
            
        Returns:
            Özet metin
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)
        
        profile = self.user_profiles.get(user_id, {})
        conversations = self.conversations.get(user_id, [])
        
        if not conversations:
            return "Bu kullanıcı ile henüz bir etkileşim yok."
        
        summary_parts = [
            f"Kullanıcı ID: {user_id}",
            f"İlk görüşme: {profile.get('first_seen', 'Bilinmiyor')}",
            f"Toplam etkileşim: {len(conversations)}",
        ]
        
        # Son 3 etkileşimi ekle
        if conversations:
            summary_parts.append("\nSon etkileşimler:")
            for i, conv in enumerate(conversations[-3:], 1):
                timestamp = conv.get('timestamp', 'Bilinmiyor')
                user_msg = conv.get('user_message', '')[:50]
                summary_parts.append(f"{i}. {timestamp}: {user_msg}...")
        
        # Metadata özeti
        all_metadata = [c.get('metadata', {}) for c in conversations if c.get('metadata')]
        if all_metadata:
            summary_parts.append("\nKaydedilen bilgiler:")
            # Örnek: sipariş numaraları, sorunlar vb.
            for meta in all_metadata[-3:]:
                for key, value in meta.items():
                    summary_parts.append(f"  - {key}: {value}")
        
        return "\n".join(summary_parts)
    
    def clear_memory(self, user_id: str) -> None:
        """
        Kullanıcının belleğini tamamen siler

        Args:
            user_id: Kullanıcı kimliği
        """
        user_file = self._get_user_file(user_id)
        if user_file.exists():
            user_file.unlink()

        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self.user_profiles:
            del self.user_profiles[user_id]

    def search_conversations(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Konuşmalarda anahtar kelime arar (JSON versiyonu için)

        Args:
            user_id: Kullanıcı kimliği
            keyword: Aranacak kelime

        Returns:
            Eşleşen konuşmalar
        """
        if user_id not in self.conversations:
            self.load_memory(user_id)

        results = []
        keyword_lower = keyword.lower()

        for interaction in self.conversations.get(user_id, []):
            if (keyword_lower in interaction['user_message'].lower() or
                keyword_lower in interaction['bot_response'].lower()):
                results.append(interaction)

        return results

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Kullanıcı profilini getirir (JSON versiyonu için)

        Args:
            user_id: Kullanıcı kimliği

        Returns:
            Kullanıcı profili veya None
        """
        if user_id not in self.user_profiles:
            self.load_memory(user_id)

        return self.user_profiles.get(user_id)

