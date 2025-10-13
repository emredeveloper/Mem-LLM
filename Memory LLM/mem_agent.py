"""
Mem-Agent: Unified Powerful System
==================================

A powerful Mem-Agent that combines all features in a single system.

Features:
- ✅ SQL and JSON memory support
- ✅ Prompt templates system
- ✅ Knowledge base integration
- ✅ User tools system
- ✅ Configuration management
- ✅ Advanced logging
- ✅ Production-ready structure

Usage:
```python
from mem_agent import MemAgent

# Simple usage
agent = MemAgent()

# Advanced usage
agent = MemAgent(
    config_file="config.yaml",
    use_sql=True,
    load_knowledge_base=True
)
```
"""

from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import logging
import json
import os

# Core dependencies
from memory_manager import MemoryManager
from llm_client import OllamaClient

# Advanced features (optional)
try:
    from memory_db import SQLMemoryManager
    from prompt_templates import prompt_manager
    from knowledge_loader import KnowledgeLoader
    from config_manager import get_config
    from memory_tools import ToolExecutor, MemoryTools
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False
    print("⚠️  Gelişmiş özellikler mevcut değil (ek paketler yükleyin)")


class MemAgent:
    """
    Güçlü ve birleşik Mem-Agent sistemi

    Tüm özellikleri tek bir yerde toplayan production-ready asistan.
    """

    def __init__(self,
                 model: str = "granite4:tiny-h",
                 config_file: Optional[str] = None,
                 use_sql: bool = True,
                 memory_dir: Optional[str] = None,
                 load_knowledge_base: bool = True,
                 ollama_url: str = "http://localhost:11434"):
        """
        Args:
            model: Kullanılacak LLM modeli
            config_file: Yapılandırma dosyası (opsiyonel)
            use_sql: SQL veritabanı kullan (True) veya JSON (False)
            memory_dir: Bellek dizini
            load_knowledge_base: Bilgi bankasını otomatik yükle
            ollama_url: Ollama API URL'i
        """

        # Yapılandırma yükleme
        self.config = None
        if ADVANCED_AVAILABLE and config_file:
            try:
                self.config = get_config(config_file)
            except Exception:
                print("⚠️  Config dosyası yüklenemedi, varsayılan ayarlar kullanılacak")

        # Kullanım modu belirleme
        self.usage_mode = "business"  # varsayılan
        if self.config:
            self.usage_mode = self.config.get("usage_mode", "business")
        elif config_file:
            # Config dosyası varsa ama yüklenemedi
            self.usage_mode = "business"
        else:
            # Config dosyası yoksa
            self.usage_mode = "personal"

        # Loglama kurulumu
        self._setup_logging()

        # Bellek sistemi seçimi
        if use_sql and ADVANCED_AVAILABLE:
            # SQL bellek (gelişmiş)
            db_path = memory_dir or self.config.get("memory.db_path", "memories.db") if self.config else "memories.db"
            self.memory = SQLMemoryManager(db_path)
            self.logger.info(f"SQL bellek sistemi aktif: {db_path}")
        else:
            # JSON bellek (basit)
            json_dir = memory_dir or self.config.get("memory.json_dir", "memories") if self.config else "memories"
            self.memory = MemoryManager(json_dir)
            self.logger.info(f"JSON bellek sistemi aktif: {json_dir}")

        # LLM istemcisi
        self.llm = OllamaClient(model, ollama_url)
        self.logger.info(f"LLM istemcisi hazır: {model}")

        # Gelişmiş özellikler (eğer mevcutsa)
        if ADVANCED_AVAILABLE:
            self._setup_advanced_features(load_knowledge_base)
        else:
            print("⚠️  Gelişmiş özellikler için ek paketler yükleyin")

        # Aktif kullanıcı ve sistem promptu
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # Araç sistemi (her zaman mevcut)
        self.tool_executor = ToolExecutor(self.memory)

        self.logger.info("MemAgent başarıyla başlatıldı")

    # === BİRLEŞİK SİSTEM METODLARI ===

    def _setup_logging(self) -> None:
        """Loglama sistemini kurar"""
        log_config = {}
        if ADVANCED_AVAILABLE and hasattr(self, 'config') and self.config:
            log_config = self.config.get("logging", {})

        if log_config.get("enabled", True):
            logging.basicConfig(
                level=getattr(logging, log_config.get("level", "INFO")),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_config.get("file", "mem_agent.log")),
                    logging.StreamHandler()
                ]
            )

        self.logger = logging.getLogger("MemAgent")

    def _setup_advanced_features(self, load_knowledge_base: bool) -> None:
        """Gelişmiş özellikleri kurar"""
        # Bilgi bankası yükleme (kullanım moduna göre)
        if load_knowledge_base:
            kb_loader = KnowledgeLoader(self.memory)

            # Config'den KB ayarlarını al
            if hasattr(self, 'config') and self.config:
                kb_config = self.config.get("knowledge_base", {})

                # Kullanım moduna göre varsayılan KB seç
                if self.usage_mode == "business":
                    default_kb = kb_config.get("default_kb", "business_tech_support")
                else:  # personal
                    default_kb = kb_config.get("default_kb", "personal_learning")

                try:
                    if default_kb == "ecommerce":
                        count = kb_loader.load_default_ecommerce_kb()
                        self.logger.info(f"E-ticaret bilgi bankası yüklendi: {count} kayıt")
                    elif default_kb == "tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Teknik destek bilgi bankası yüklendi: {count} kayıt")
                    elif default_kb == "business_tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Kurumsal teknik destek bilgi bankası yüklendi: {count} kayıt")
                    elif default_kb == "personal_learning":
                        # Kişisel öğrenme için basit KB
                        count = kb_loader.load_default_ecommerce_kb()  # Geçici olarak aynı KB'yi kullan
                        self.logger.info(f"Kişisel öğrenme bilgi bankası yüklendi: {count} kayıt")
                except Exception as e:
                    self.logger.error(f"Bilgi bankası yükleme hatası: {e}")

        # Sistem promptu yükleme (kullanım moduna göre)
        if hasattr(self, 'config') and self.config:
            prompt_config = self.config.get("prompt", {})

            # Kullanım moduna göre varsayılan şablon seç
            if self.usage_mode == "business":
                default_template = "business_customer_service"
            else:  # personal
                default_template = "personal_assistant"

            template_name = prompt_config.get("template", default_template)
            variables = prompt_config.get("variables", {})

            # Business modu için ek değişkenler
            if self.usage_mode == "business":
                business_config = self.config.get("business", {})
                variables.update({
                    "company_name": business_config.get("company_name", "Şirketimiz"),
                    "founded_year": business_config.get("founded_year", "2010"),
                    "employee_count": business_config.get("employee_count", "100+"),
                    "industry": business_config.get("industry", "Teknoloji")
                })
            else:  # personal
                personal_config = self.config.get("personal", {})
                variables.update({
                    "user_name": personal_config.get("user_name", "Kullanıcı"),
                    "timezone": personal_config.get("timezone", "Europe/Istanbul")
                })

            try:
                variables['current_date'] = datetime.now().strftime("%Y-%m-%d")
                self.current_system_prompt = prompt_manager.render_prompt(template_name, **variables)
                self.logger.info(f"Prompt şablonu yüklendi: {template_name} (Mod: {self.usage_mode})")
            except Exception as e:
                self.logger.error(f"Prompt şablonu yükleme hatası: {e}")
                self.current_system_prompt = f"Sen {self.usage_mode} modunda yardımsever bir asistansın."

    def check_setup(self) -> Dict[str, Any]:
        """Sistem kurulumunu kontrol eder"""
        ollama_running = self.llm.check_connection()
        models = self.llm.list_models()
        model_exists = self.llm.model in models

        # Bellek istatistikleri
        try:
            if hasattr(self.memory, 'get_statistics'):
                stats = self.memory.get_statistics()
            else:
                # JSON bellek için basit istatistik
                stats = {
                    "total_users": 0,
                    "total_interactions": 0,
                    "knowledge_base_entries": 0
                }
        except Exception:
            stats = {
                "total_users": 0,
                "total_interactions": 0,
                "knowledge_base_entries": 0
            }

        return {
            "ollama_running": ollama_running,
            "available_models": models,
            "target_model": self.llm.model,
            "model_ready": model_exists,
            "memory_backend": "SQL" if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager) else "JSON",
            "total_users": stats.get('total_users', 0),
            "total_interactions": stats.get('total_interactions', 0),
            "kb_entries": stats.get('knowledge_base_entries', 0),
            "status": "ready" if (ollama_running and model_exists) else "not_ready"
        }

    def set_user(self, user_id: str, name: Optional[str] = None) -> None:
        """
        Aktif kullanıcıyı ayarlar

        Args:
            user_id: Kullanıcı kimliği
            name: Kullanıcı adı (opsiyonel)
        """
        self.current_user = user_id

        # SQL bellek için kullanıcı ekleme
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
            self.memory.add_user(user_id, name)

        # Kullanıcı adını güncelle (eğer verilmişse)
        if name:
            if hasattr(self.memory, 'update_user_profile'):
                self.memory.update_user_profile(user_id, {"name": name})

        self.logger.debug(f"Aktif kullanıcı ayarlandı: {user_id}")

    def chat(self, message: str, user_id: Optional[str] = None,
             metadata: Optional[Dict] = None) -> str:
        """
        Kullanıcı ile sohbet eder

        Args:
            message: Kullanıcının mesajı
            user_id: Kullanıcı kimliği (opsiyonel)
            metadata: Ek bilgiler

        Returns:
            Botun cevabı
        """
        # Kullanıcıyı belirle
        if user_id:
            self.set_user(user_id)
        elif not self.current_user:
            return "Hata: Kullanıcı kimliği belirtilmedi."

        user_id = self.current_user

        # Önce araç komutlarını kontrol et
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            return tool_result

        # Bilgi bankası araması (eğer SQL kullanılıyorsa)
        kb_context = ""
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager) and hasattr(self, 'config') and self.config:
            if self.config.get("response.use_knowledge_base", True):
                try:
                    kb_results = self.memory.search_knowledge(
                        query=message,
                        limit=self.config.get("knowledge_base.search_limit", 5)
                    )

                    if kb_results:
                        kb_context = "\n\nİlgili Bilgiler:\n"
                        for i, result in enumerate(kb_results, 1):
                            kb_context += f"{i}. S: {result['question']}\n   C: {result['answer']}\n"
                except Exception as e:
                    self.logger.error(f"Bilgi bankası arama hatası: {e}")

        # Geçmiş konuşmaları al
        messages = []
        if self.current_system_prompt:
            messages.append({"role": "system", "content": self.current_system_prompt})

        # Bellek geçmişini ekle
        try:
            if hasattr(self.memory, 'get_recent_conversations'):
                recent_limit = self.config.get("response.recent_conversations_limit", 5) if hasattr(self, 'config') and self.config else 5
                recent_convs = self.memory.get_recent_conversations(user_id, recent_limit)

                for conv in reversed(recent_convs):
                    messages.append({"role": "user", "content": conv.get('user_message', '')})
                    messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        except Exception as e:
            self.logger.error(f"Bellek geçmişi yükleme hatası: {e}")

        # Bilgi bankası bağlamını ekle
        if kb_context:
            messages.append({
                "role": "system",
                "content": f"Kullanıcının sorusuna cevap verirken bu bilgileri kullanabilirsin:{kb_context}"
            })

        # Şimdiki mesajı ekle
        messages.append({"role": "user", "content": message})

        # LLM'den cevap al
        try:
            response = self.llm.chat(
                messages=messages,
                temperature=self.config.get("llm.temperature", 0.7) if hasattr(self, 'config') and self.config else 0.7,
                max_tokens=self.config.get("llm.max_tokens", 500) if hasattr(self, 'config') and self.config else 500
            )
        except Exception as e:
            self.logger.error(f"LLM cevap alma hatası: {e}")
            response = "Üzgünüm, şu anda cevap veremiyorum. Lütfen daha sonra tekrar deneyin."

        # Etkileşimi kaydet
        try:
            if hasattr(self.memory, 'add_interaction'):
                self.memory.add_interaction(
                    user_id=user_id,
                    user_message=message,
                    bot_response=response,
                    metadata=metadata
                )
        except Exception as e:
            self.logger.error(f"Etkileşim kaydetme hatası: {e}")

        return response

    def add_knowledge(self, category: str, question: str, answer: str,
                     keywords: Optional[List[str]] = None, priority: int = 0) -> int:
        """Bilgi bankasına yeni kayıt ekler"""
        if not ADVANCED_AVAILABLE or not isinstance(self.memory, SQLMemoryManager):
            return 0

        try:
            kb_id = self.memory.add_knowledge(category, question, answer, keywords, priority)
            self.logger.info(f"Yeni bilgi eklendi: {category} - {kb_id}")
            return kb_id
        except Exception as e:
            self.logger.error(f"Bilgi ekleme hatası: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Genel istatistikleri döndürür"""
        try:
            if hasattr(self.memory, 'get_statistics'):
                return self.memory.get_statistics()
            else:
                # JSON bellek için basit istatistik
                return {
                    "total_users": 0,
                    "total_interactions": 0,
                    "memory_backend": "JSON"
                }
        except Exception as e:
            self.logger.error(f"İstatistik alma hatası: {e}")
            return {}

    def search_history(self, keyword: str, user_id: Optional[str] = None) -> List[Dict]:
        """Kullanıcı geçmişinde arama yapar"""
        uid = user_id or self.current_user
        if not uid:
            return []

        try:
            if hasattr(self.memory, 'search_conversations'):
                return self.memory.search_conversations(uid, keyword)
            else:
                return []
        except Exception as e:
            self.logger.error(f"Geçmiş arama hatası: {e}")
            return []

    def show_user_info(self, user_id: Optional[str] = None) -> str:
        """Kullanıcı bilgilerini gösterir"""
        uid = user_id or self.current_user
        if not uid:
            return "Kullanıcı kimliği belirtilmedi."

        try:
            if hasattr(self.memory, 'get_user_profile'):
                profile = self.memory.get_user_profile(uid)
                if profile:
                    return f"Kullanıcı: {uid}\nİsim: {profile.get('name', 'Bilinmiyor')}\nİlk görüşme: {profile.get('first_seen', 'Bilinmiyor')}"
                else:
                    return f"Kullanıcı {uid} bulunamadı."
            else:
                return "Bu özellik mevcut değil."
        except Exception as e:
            return f"Hata: {str(e)}"

    def export_memory(self, user_id: Optional[str] = None, format: str = "json") -> str:
        """Kullanıcı verilerini dışa aktarır"""
        uid = user_id or self.current_user
        if not uid:
            return "Kullanıcı kimliği belirtilmedi."

        try:
            if hasattr(self.memory, 'get_recent_conversations') and hasattr(self.memory, 'get_user_profile'):
                conversations = self.memory.get_recent_conversations(uid, 1000)
                profile = self.memory.get_user_profile(uid)

                if format == "json":
                    export_data = {
                        "user_id": uid,
                        "export_date": datetime.now().isoformat(),
                        "profile": profile,
                        "conversations": conversations
                    }
                    return json.dumps(export_data, ensure_ascii=False, indent=2)
                elif format == "txt":
                    result = f"{uid} kullanıcısı konuşma geçmişi\n"
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
                    return "Desteklenmeyen format. json veya txt kullanın."
            else:
                return "Bu özellik mevcut değil."
        except Exception as e:
            return f"Dışa aktarım hatası: {str(e)}"

    def clear_user_data(self, user_id: Optional[str] = None, confirm: bool = False) -> str:
        """Kullanıcının verilerini siler"""
        uid = user_id or self.current_user
        if not uid:
            return "Kullanıcı kimliği belirtilmedi."

        if not confirm:
            return "Verileri silmek için confirm=True parametresini kullanın."

        try:
            if hasattr(self.memory, 'clear_memory'):
                self.memory.clear_memory(uid)
                return f"{uid} kullanıcısının tüm verileri silindi."
            else:
                return "Bu özellik mevcut değil."
        except Exception as e:
            return f"Silme hatası: {str(e)}"

    def list_available_tools(self) -> str:
        """Mevcut araçları listeler"""
        if ADVANCED_AVAILABLE:
            return self.tool_executor.memory_tools.list_available_tools()
        else:
            return "Araçlar sistemi mevcut değil."

    def close(self) -> None:
        """Kaynakları temizler"""
        if hasattr(self.memory, 'close'):
            self.memory.close()
        self.logger.info("MemAgent kapatıldı")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

