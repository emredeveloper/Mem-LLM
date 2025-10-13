# BU DOSYA ARTIK KULLANILMIYOR - BİRLEŞİK SİSTEM KULLANIN
# Lütfen mem_agent.py dosyasını kullanın


class MemAgentPro:
    """
    Production-ready bellek asistanı
    
    Özellikler:
    - SQL veritabanı desteği
    - Yapılandırma dosyası
    - Prompt şablonları
    - Bilgi bankası entegrasyonu
    - Gelişmiş loglama
    """
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Args:
            config_file: Yapılandırma dosyası yolu
        """
        # Yapılandırma yükle
        self.config = get_config(config_file)
        
        # Loglama kurulumu
        self._setup_logging()
        
        # Bellek yöneticisi
        db_path = self.config.get_db_path()
        self.memory = SQLMemoryManager(db_path)
        self.logger.info(f"SQL bellek yöneticisi başlatıldı: {db_path}")
        
        # LLM istemcisi
        llm_config = self.config.get_llm_config()
        self.llm = OllamaClient(
            model=llm_config.get('model', 'granite4:tiny-h'),
            base_url=llm_config.get('base_url', 'http://localhost:11434')
        )
        self.logger.info(f"LLM istemcisi başlatıldı: {llm_config.get('model')}")
        
        # Bilgi bankası yükleyici
        self.kb_loader = KnowledgeLoader(self.memory)
        
        # Bilgi bankasını otomatik yükle
        if self.config.is_kb_enabled() and self.config.get("knowledge_base.auto_load"):
            self._load_knowledge_base()
        
        # Prompt şablonu
        self._load_prompt_template()
        
        # Aktif kullanıcı
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # Araç sistemi
        self.tool_executor = ToolExecutor(self.memory, self.current_user)

        self.logger.info("MemAgentPro başarıyla başlatıldı")
    
    def _setup_logging(self) -> None:
        """Loglama yapılandırması"""
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
        
        self.logger = logging.getLogger("MemAgentPro")
    
    def _load_knowledge_base(self) -> None:
        """Bilgi bankasını yükler"""
        kb_config = self.config.get_kb_config()
        default_kb = kb_config.get("default_kb", "ecommerce")
        
        try:
            if default_kb == "ecommerce":
                count = self.kb_loader.load_default_ecommerce_kb()
                self.logger.info(f"E-ticaret bilgi bankası yüklendi: {count} kayıt")
            elif default_kb == "tech_support":
                count = self.kb_loader.load_default_tech_support_kb()
                self.logger.info(f"Teknik destek bilgi bankası yüklendi: {count} kayıt")
            
            # Özel dosyadan yükle
            custom_file = kb_config.get("custom_kb_file")
            if custom_file:
                if custom_file.endswith('.json'):
                    count = self.kb_loader.load_from_json(custom_file)
                    self.logger.info(f"Özel bilgi bankası yüklendi: {count} kayıt")
                elif custom_file.endswith('.yaml'):
                    count = self.kb_loader.load_from_yaml(custom_file)
                    self.logger.info(f"Özel bilgi bankası yüklendi: {count} kayıt")
        except Exception as e:
            self.logger.error(f"Bilgi bankası yüklenirken hata: {e}")
    
    def _load_prompt_template(self) -> None:
        """Prompt şablonunu yükler"""
        prompt_config = self.config.get_prompt_config()
        
        # Özel prompt varsa kullan
        if prompt_config.get("custom_prompt"):
            self.system_prompt = prompt_config["custom_prompt"]
            self.logger.info("Özel sistem promptu yüklendi")
            return
        
        # Şablon kullan
        template_name = prompt_config.get("template", "customer_service")
        variables = prompt_config.get("variables", {})
        
        try:
            # Güncel tarihi ekle
            variables['current_date'] = datetime.now().strftime("%Y-%m-%d")
            
            self.system_prompt = prompt_manager.render_prompt(
                template_name, 
                **variables
            )
            self.logger.info(f"Prompt şablonu yüklendi: {template_name}")
        except Exception as e:
            self.logger.error(f"Prompt şablonu yüklenirken hata: {e}")
            self.system_prompt = "Sen yardımsever bir asistansın."
    
    def check_setup(self) -> Dict[str, any]:
        """Sistem kurulumunu kontrol eder"""
        ollama_running = self.llm.check_connection()
        models = self.llm.list_models()
        model_exists = self.llm.model in models
        
        stats = self.memory.get_statistics()
        
        return {
            "ollama_running": ollama_running,
            "available_models": models,
            "target_model": self.llm.model,
            "model_ready": model_exists,
            "database_ready": True,
            "total_users": stats['total_users'],
            "total_interactions": stats['total_interactions'],
            "kb_entries": stats['knowledge_base_entries'],
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
        
        # Kullanıcı yoksa ekle
        profile = self.memory.get_user_profile(user_id)
        if not profile:
            self.memory.add_user(user_id, name)
            self.logger.info(f"Yeni kullanıcı oluşturuldu: {user_id}")
        
        self.logger.debug(f"Aktif kullanıcı ayarlandı: {user_id}")
    
    def chat(self, message: str, user_id: Optional[str] = None,
             metadata: Optional[Dict] = None) -> str:
        """
        Kullanıcı ile sohbet eder (gelişmiş özelliklerle)
        
        Args:
            message: Kullanıcının mesajı
            user_id: Kullanıcı kimliği (opsiyonel)
            metadata: Ek bilgiler
            
        Returns:
            Botun cevabı
        """
        start_time = datetime.now()
        
        # Kullanıcı ayarla
        if user_id:
            self.set_user(user_id)
        elif not self.current_user:
            return "Hata: Kullanıcı kimliği belirtilmedi."
        
        user_id = self.current_user

        # Önce araç komutlarını kontrol et
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            return tool_result

        # Bilgi bankasında ara (eğer etkinse)
        kb_context = ""
        if self.config.get("response.use_knowledge_base", True):
            kb_results = self.memory.search_knowledge(
                query=message,
                limit=self.config.get("knowledge_base.search_limit", 5)
            )
            
            if kb_results:
                kb_context = "\n\nİlgili Bilgiler:\n"
                for i, result in enumerate(kb_results, 1):
                    kb_context += f"{i}. S: {result['question']}\n   C: {result['answer']}\n"
                
                self.logger.debug(f"Bilgi bankasında {len(kb_results)} sonuç bulundu")
        
        # Geçmiş konuşmaları al
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if self.config.is_memory_enabled():
            recent_limit = self.config.get("response.recent_conversations_limit", 5)
            recent_convs = self.memory.get_recent_conversations(user_id, recent_limit)
            
            # Ters çevir (eski → yeni)
            for conv in reversed(recent_convs):
                messages.append({"role": "user", "content": conv['user_message']})
                messages.append({"role": "assistant", "content": conv['bot_response']})
        
        # Bilgi bankası bağlamını ekle
        if kb_context:
            messages.append({
                "role": "system", 
                "content": f"Kullanıcının sorusuna cevap verirken bu bilgileri kullanabilirsin:{kb_context}"
            })
        
        # Şimdiki mesaj
        messages.append({"role": "user", "content": message})
        
        # LLM'den cevap al
        llm_config = self.config.get_llm_config()
        response = self.llm.chat(
            messages=messages,
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 500)
        )
        
        # Etkileşimi kaydet
        self.memory.add_interaction(
            user_id=user_id,
            user_message=message,
            bot_response=response,
            metadata=metadata
        )
        
        # Performans logu
        elapsed = (datetime.now() - start_time).total_seconds()
        self.logger.info(f"Cevap üretildi: {elapsed:.2f}s - User: {user_id}")
        
        return response
    
    def update_profile(self, info: Dict, user_id: Optional[str] = None) -> None:
        """Kullanıcı profilini günceller"""
        uid = user_id or self.current_user
        if uid:
            self.memory.update_user_profile(uid, info)
            self.logger.debug(f"Profil güncellendi: {uid}")
    
    def search_history(self, keyword: str, user_id: Optional[str] = None) -> List[Dict]:
        """Kullanıcı geçmişinde arama yapar"""
        uid = user_id or self.current_user
        if uid:
            return self.memory.search_conversations(uid, keyword)
        return []
    
    def add_knowledge(self, category: str, question: str, answer: str,
                     keywords: Optional[List[str]] = None, priority: int = 0) -> int:
        """
        Bilgi bankasına yeni kayıt ekler
        
        Args:
            category: Kategori
            question: Soru
            answer: Cevap
            keywords: Anahtar kelimeler
            priority: Öncelik
            
        Returns:
            Kayıt ID'si
        """
        kb_id = self.memory.add_knowledge(category, question, answer, keywords, priority)
        self.logger.info(f"Yeni bilgi eklendi: {category} - {kb_id}")
        return kb_id
    
    def get_statistics(self) -> Dict:
        """Genel istatistikleri döndürür"""
        return self.memory.get_statistics()
    
    def change_prompt_template(self, template_name: str, **variables) -> None:
        """
        Prompt şablonunu değiştirir
        
        Args:
            template_name: Şablon adı
            **variables: Şablon değişkenleri
        """
        try:
            variables['current_date'] = datetime.now().strftime("%Y-%m-%d")
            self.system_prompt = prompt_manager.render_prompt(template_name, **variables)
            self.logger.info(f"Prompt şablonu değiştirildi: {template_name}")
        except Exception as e:
            self.logger.error(f"Prompt şablonu değiştirilemedi: {e}")
    
    def list_prompt_templates(self) -> List[str]:
        """Mevcut prompt şablonlarını listeler"""
        return prompt_manager.list_templates()
    
    def close(self) -> None:
        """Kaynakları temizler"""
        self.memory.close()
        self.logger.info("MemAgentPro kapatıldı")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

