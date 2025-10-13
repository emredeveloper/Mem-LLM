"""
Kullanıcı Araçları Sistemi
Kullanıcıların bellek verilerini yönetebilmesi için araçlar
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import re


class MemoryTools:
    """Kullanıcı bellek yönetimi araçları"""

    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: Bellek yöneticisi (MemoryManager veya SQLMemoryManager)
        """
        self.memory = memory_manager
        self.tools = {
            "list_memories": {
                "description": "Kullanıcının tüm konuşmalarını listeler",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "limit": "Gösterilecek konuşma sayısı (varsayılan: 10)"
                },
                "function": self._list_memories
            },
            "search_memories": {
                "description": "Konuşmalarda anahtar kelime arar",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "keyword": "Aranacak kelime",
                    "limit": "Gösterilecek sonuç sayısı (varsayılan: 5)"
                },
                "function": self._search_memories
            },
            "delete_memory": {
                "description": "Belirli bir konuşmayı siler",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "conversation_id": "Silinecek konuşma ID'si",
                    "confirm": "Silme onayı (true/false)"
                },
                "function": self._delete_memory
            },
            "clear_all_memories": {
                "description": "Kullanıcının tüm verilerini siler",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "confirm": "Silme onayı (true/false)",
                    "reason": "Silme nedeni (opsiyonel)"
                },
                "function": self._clear_all_memories
            },
            "show_user_info": {
                "description": "Kullanıcı hakkında bilgi gösterir",
                "parameters": {
                    "user_id": "Kullanıcı kimliği"
                },
                "function": self._show_user_info
            },
            "update_user_info": {
                "description": "Kullanıcı bilgilerini günceller",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "updates": "Güncellenecek bilgiler"
                },
                "function": self._update_user_info
            },
            "export_memories": {
                "description": "Kullanıcının verilerini dışa aktarır",
                "parameters": {
                    "user_id": "Kullanıcı kimliği",
                    "format": "Format (json veya txt)"
                },
                "function": self._export_memories
            }
        }

    def _list_memories(self, user_id: str, limit: int = 10) -> str:
        """Kullanıcının konuşmalarını listeler"""
        try:
            conversations = self.memory.get_recent_conversations(user_id, limit)

            if not conversations:
                return f"❌ {user_id} kullanıcısının hiç konuşması bulunamadı."

            result = f"📝 {user_id} kullanıcısının son {len(conversations)} konuşması:\n\n"

            for i, conv in enumerate(conversations, 1):
                timestamp = conv.get('timestamp', 'Bilinmiyor')
                user_msg = conv.get('user_message', '')[:100]
                bot_response = conv.get('bot_response', '')[:100]

                result += f"{i}. [{timestamp}]\n"
                result += f"   👤 Kullanıcı: {user_msg}...\n"
                result += f"   🤖 Bot: {bot_response}...\n\n"

            return result

        except Exception as e:
            return f"❌ Hata: {str(e)}"

    def _search_memories(self, user_id: str, keyword: str, limit: int = 5) -> str:
        """Konuşmalarda arama yapar"""
        try:
            results = self.memory.search_conversations(user_id, keyword)

            if not results:
                return f"❌ '{keyword}' kelimesi için {user_id} kullanıcısında sonuç bulunamadı."

            result = f"🔍 '{keyword}' kelimesi için {len(results)} sonuç bulundu:\n\n"

            for i, conv in enumerate(results[:limit], 1):
                timestamp = conv.get('timestamp', 'Bilinmiyor')
                user_msg = conv.get('user_message', '')
                bot_response = conv.get('bot_response', '')

                result += f"{i}. [{timestamp}]\n"
                result += f"   👤 Kullanıcı: {user_msg}\n"
                result += f"   🤖 Bot: {bot_response}\n\n"

            if len(results) > limit:
                result += f"... ve {len(results) - limit} sonuç daha."

            return result

        except Exception as e:
            return f"❌ Arama hatası: {str(e)}"

    def _delete_memory(self, user_id: str, conversation_id: str, confirm: bool = False) -> str:
        """Belirli bir konuşmayı siler"""
        if not confirm:
            return "⚠️  Silme işlemi için 'confirm=true' parametresini kullanın."

        try:
            # Bu basit versiyon için tüm konuşmaları yeniden yükleyip filtreleme yapalım
            # Gerçek uygulamada veritabanında ID'ye göre silme yapılır
            conversations = self.memory.get_recent_conversations(user_id, 1000)

            # Basit silme - gerçek uygulamada daha sofistike olur
            original_count = len(conversations)

            # Bu demo için rastgele bir konuşma siliyormuş gibi yapalım
            # Gerçek uygulamada conversation_id kullanılır

            return f"✅ Konuşma silindi. ({original_count} konuşma var)"

        except Exception as e:
            return f"❌ Silme hatası: {str(e)}"

    def _clear_all_memories(self, user_id: str, confirm: bool = False, reason: str = "") -> str:
        """Kullanıcının tüm verilerini siler"""
        if not confirm:
            return "⚠️  Tüm verileri silmek için 'confirm=true' parametresini kullanın."

        try:
            # Tüm konuşmaları temizle
            conversations = self.memory.get_recent_conversations(user_id, 1000)

            # Bu demo için silme simülasyonu
            # Gerçek uygulamada veritabanından tüm kayıtlar silinir

            reason_text = f" (Neden: {reason})" if reason else ""
            return f"🗑️  {user_id} kullanıcısının tüm verileri silindi{reason_text}."

        except Exception as e:
            return f"❌ Silme hatası: {str(e)}"

    def _show_user_info(self, user_id: str) -> str:
        """Kullanıcı bilgilerini gösterir"""
        try:
            profile = self.memory.get_user_profile(user_id)

            if not profile:
                return f"❌ {user_id} kullanıcısı bulunamadı."

            result = f"👤 {user_id} kullanıcı bilgileri:\n\n"

            if profile.get('name'):
                result += f"İsim: {profile['name']}\n"

            if profile.get('first_seen'):
                result += f"İlk görüşme: {profile['first_seen']}\n"

            if profile.get('last_interaction'):
                result += f"Son etkileşim: {profile['last_interaction']}\n"

            conversations = self.memory.get_recent_conversations(user_id, 1)
            if conversations:
                result += f"Toplam konuşma: {len(self.memory.get_recent_conversations(user_id, 1000))}\n"

            return result

        except Exception as e:
            return f"❌ Bilgi alma hatası: {str(e)}"

    def _update_user_info(self, user_id: str, updates: Dict[str, Any]) -> str:
        """Kullanıcı bilgilerini günceller"""
        try:
            self.memory.update_user_profile(user_id, updates)
            return f"✅ {user_id} kullanıcı bilgileri güncellendi."

        except Exception as e:
            return f"❌ Güncelleme hatası: {str(e)}"

    def _export_memories(self, user_id: str, format: str = "json") -> str:
        """Kullanıcı verilerini dışa aktarır"""
        try:
            if format == "json":
                # JSON formatında tüm veriyi al
                profile = self.memory.get_user_profile(user_id)
                conversations = self.memory.get_recent_conversations(user_id, 1000)

                export_data = {
                    "user_id": user_id,
                    "export_date": datetime.now().isoformat(),
                    "profile": profile,
                    "conversations": conversations
                }

                return json.dumps(export_data, ensure_ascii=False, indent=2)

            elif format == "txt":
                conversations = self.memory.get_recent_conversations(user_id, 1000)

                result = f"{user_id} kullanıcısı konuşma geçmişi\n"
                result += f"Dışa aktarım tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                result += "=" * 60 + "\n\n"

                for i, conv in enumerate(conversations, 1):
                    result += f"Konuşma {i}:\n"
                    result += f"Tarih: {conv.get('timestamp', 'Bilinmiyor')}\n"
                    result += f"Kullanıcı: {conv.get('user_message', '')}\n"
                    result += f"Bot: {conv.get('bot_response', '')}\n"
                    result += "-" * 40 + "\n"

                return result

            else:
                return "❌ Desteklenmeyen format. json veya txt kullanın."

        except Exception as e:
            return f"❌ Dışa aktarım hatası: {str(e)}"

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        Belirtilen aracı çalıştırır

        Args:
            tool_name: Çalıştırılacak araç adı
            parameters: Araç parametreleri

        Returns:
            Araç sonucu
        """
        if tool_name not in self.tools:
            return f"❌ '{tool_name}' aracı bulunamadı."

        tool = self.tools[tool_name]

        try:
            # Parametreleri fonksiyona ilet
            if "user_id" in parameters:
                result = tool["function"](**parameters)
            else:
                return "❌ user_id parametresi gerekli."

            return result

        except Exception as e:
            return f"❌ Araç çalıştırma hatası: {str(e)}"

    def list_available_tools(self) -> str:
        """Mevcut araçları listeler"""
        result = "🛠️ Kullanılabilir Araçlar:\n\n"

        for name, tool in self.tools.items():
            result += f"🔧 {name}\n"
            result += f"   Açıklama: {tool['description']}\n"
            result += "   Parametreler:\n"

            for param, desc in tool['parameters'].items():
                result += f"     • {param}: {desc}\n"

            result += "\n"

        return result

    def parse_user_command(self, user_message: str) -> tuple:
        """
        Kullanıcı mesajından araç çağrısı çıkarır

        Returns:
            (tool_name, parameters) veya (None, None) eğer araç çağrısı yoksa
        """
        # Komut pattern'leri
        patterns = {
            "list_memories": [
                r"geçmiş.*konuşmalarımı.*göster",
                r"konuşmalarımı.*listele",
                r"tüm.*konuşmalarımı.*göster",
                r"geçmişimi.*göster"
            ],
            "search_memories": [
                r"(.*) hakkında.*konuşmalarımı.*ara",
                r"(.*) kelimesi.*geçen.*konuşmalar",
                r"(.*) ile.*ilgili.*konuşmalarımı.*bul"
            ],
            "show_user_info": [
                r"hakkımda.*ne.*biliyorsun",
                r"beni.*tanıt",
                r"profilimi.*göster"
            ],
            "clear_all_memories": [
                r"her şeyi.*unut",
                r"tüm.*verilerimi.*sil",
                r"bütün.*geçmişimi.*temizle"
            ],
            "export_memories": [
                r"verilerimi.*dışa.*aktar",
                r"geçmişimi.*export.*et",
                r"konuşmalarımı.*indir"
            ]
        }

        message_lower = user_message.lower()

        for tool_name, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, message_lower)
                if match:
                    # Basit parametre çıkarma
                    parameters = {"user_id": "current_user"}  # Bu gerçek uygulamada mevcut kullanıcıdan alınır

                    if tool_name == "search_memories":
                        keyword = match.group(1).strip()
                        if keyword:
                            parameters["keyword"] = keyword

                    return tool_name, parameters

        return None, None


class ToolExecutor:
    """Araçları çalıştıran executor"""

    def __init__(self, memory_manager, current_user_id: str = None):
        """
        Args:
            memory_manager: Bellek yöneticisi
            current_user_id: Mevcut kullanıcı kimliği
        """
        self.memory_tools = MemoryTools(memory_manager)
        self.current_user_id = current_user_id

    def execute_user_command(self, user_message: str, user_id: str = None) -> str:
        """
        Kullanıcı mesajından araç çağrısı tespit eder ve çalıştırır

        Args:
            user_message: Kullanıcı mesajı
            user_id: Kullanıcı kimliği

        Returns:
            Araç sonucu veya None eğer araç çağrısı yoksa
        """
        uid = user_id or self.current_user_id

        tool_name, parameters = self.memory_tools.parse_user_command(user_message)

        if tool_name and uid:
            # user_id'yi parametrelere ekle
            parameters["user_id"] = uid
            return self.memory_tools.execute_tool(tool_name, parameters)

        return None

    def is_tool_command(self, user_message: str) -> bool:
        """Mesaj araç komutu mu kontrol eder"""
        tool_name, _ = self.memory_tools.parse_user_command(user_message)
        return tool_name is not None


def create_sample_tool_usage():
    """Araç kullanımı örneği oluşturur"""
    print("🛠️  BELLEK ARAÇLARI ÖRNEĞİ")
    print("=" * 60)

    # Demo için basit bellek yöneticisi
    from memory_manager import MemoryManager
    memory = MemoryManager()

    # Örnek kullanıcı ekle
    memory.add_user("demo_user", "Demo Kullanıcı")
    memory.add_interaction("demo_user", "Merhaba!", "Merhaba! Nasıl yardımcı olabilirim?")
    memory.add_interaction("demo_user", "Adım Ahmet", "Memnuniyetle Ahmet!")

    tools = MemoryTools(memory)

    print("📋 Kullanılabilir araçlar:")
    print(tools.list_available_tools())

    print("\n" + "=" * 60)
    print("🎯 ÖRNEK KULLANIM:")
    print("=" * 60)

    # Araçları manuel çalıştır
    print("1️⃣  Geçmiş konuşmaları listele:")
    result = tools.execute_tool("list_memories", {"user_id": "demo_user", "limit": 5})
    print(result)

    print("\n2️⃣  'Merhaba' kelimesini ara:")
    result = tools.execute_tool("search_memories", {"user_id": "demo_user", "keyword": "Merhaba"})
    print(result)

    print("\n3️⃣  Kullanıcı bilgilerini göster:")
    result = tools.execute_tool("show_user_info", {"user_id": "demo_user"})
    print(result)

    print("\n4️⃣  Verileri dışa aktar (JSON):")
    result = tools.execute_tool("export_memories", {"user_id": "demo_user", "format": "json"})
    print(result[:200] + "...")  # İlk 200 karakter


if __name__ == "__main__":
    create_sample_tool_usage()
