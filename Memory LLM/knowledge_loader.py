"""
Knowledge Base Loader
Loads pre-prepared problem/solution database into the system
"""

import json
try:
    import yaml
except ImportError:
    import pyyaml as yaml
from pathlib import Path
from typing import List, Dict, Optional
from memory_db import SQLMemoryManager


class KnowledgeLoader:
    """Knowledge base management and loading"""
    
    def __init__(self, db_manager: SQLMemoryManager):
        """
        Args:
            db_manager: SQL memory manager
        """
        self.db = db_manager
    
    def load_from_json(self, file_path: str) -> int:
        """
        Load knowledge base from JSON file
        
        JSON Format:
        {
            "knowledge_base": [
                {
                    "category": "shipping",
                    "question": "Kargo ne zaman gelir?",
                    "answer": "Kargo 3-5 iş günü içinde teslim edilir.",
                    "keywords": ["kargo", "teslimat", "süre"],
                    "priority": 10
                }
            ]
        }
        
        Args:
            file_path: JSON file path
            
        Returns:
            Number of loaded records
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for entry in data.get('knowledge_base', []):
            self.db.add_knowledge(
                category=entry['category'],
                question=entry['question'],
                answer=entry['answer'],
                keywords=entry.get('keywords', []),
                priority=entry.get('priority', 0)
            )
            count += 1
        
        return count
    
    def load_from_yaml(self, file_path: str) -> int:
        """
        Load knowledge base from YAML file
        
        Args:
            file_path: YAML file path
            
        Returns:
            Number of loaded records
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        count = 0
        for entry in data.get('knowledge_base', []):
            self.db.add_knowledge(
                category=entry['category'],
                question=entry['question'],
                answer=entry['answer'],
                keywords=entry.get('keywords', []),
                priority=entry.get('priority', 0)
            )
            count += 1
        
        return count
    
    def load_default_ecommerce_kb(self) -> int:
        """
        Load default knowledge base for e-commerce
        
        Returns:
            Number of loaded records
        """
        knowledge = [
            # Kargo
            {
                "category": "shipping",
                "question": "Kargom ne zaman gelir?",
                "answer": "After your order is confirmed, it will be shipped within 2-3 business days and delivered to your address within 3-5 business days.",
                "keywords": ["shipping", "delivery", "time", "when"],
                "priority": 10
            },
            {
                "category": "shipping",
                "question": "How to track shipping?",
                "answer": "You can see the shipping tracking number by clicking on your order number from the My Orders page. You can track it from the shipping company's website with this number.",
                "keywords": ["kargo", "takip", "sorgulama"],
                "priority": 9
            },
            {
                "category": "shipping",
                "question": "How much is the shipping fee?",
                "answer": "Shipping is free for purchases of 150 TL and above. For orders below that, the shipping fee is 29.90 TL.",
                "keywords": ["shipping", "fee", "free", "cost"],
                "priority": 8
            },
            # İade
            {
                "category": "iade",
                "question": "Ürün iadesi nasıl yapılır?",
                "answer": "Ürün teslim tarihinden itibaren 14 gün içinde iade edebilirsiniz. Siparişlerim sayfasından iade talebi oluşturun, ürünü kargo ile gönderin. İade onaylandıktan sonra ödemeniz 5-7 iş günü içinde hesabınıza iade edilir.",
                "keywords": ["iade", "geri gönderme", "iptal"],
                "priority": 10
            },
            {
                "category": "iade",
                "question": "İade ücreti kim öder?",
                "answer": "Ürün kusurlu veya hatalı gönderilmişse iade kargo ücreti tarafımızca karşılanır. Cayma hakkı kullanımında kargo ücreti müşteriye aittir.",
                "keywords": ["iade", "kargo", "ücret"],
                "priority": 7
            },
            # Ödeme
            {
                "category": "ödeme",
                "question": "Hangi ödeme yöntemleri kabul edilir?",
                "answer": "Kredi kartı, banka kartı, havale/EFT ve kapıda ödeme seçenekleri mevcuttur. Taksit seçenekleri için banka ve kart türünüze göre değişiklik gösterebilir.",
                "keywords": ["ödeme", "kredi kartı", "taksit", "havale"],
                "priority": 8
            },
            {
                "category": "ödeme",
                "question": "İade ne zaman hesabıma geçer?",
                "answer": "İade onaylandıktan sonra kredi kartına yapılan ödemeler 5-7 iş günü içinde hesabınıza yansır. Havale/EFT ile yapılan ödemeler 2-3 iş günü içinde iade edilir.",
                "keywords": ["iade", "ödeme", "geri ödeme", "para iadesi"],
                "priority": 9
            },
            # Sipariş
            {
                "category": "sipariş",
                "question": "Siparişimi nasıl iptal edebilirim?",
                "answer": "Sipariş kargoya verilmeden önce Siparişlerim sayfasından iptal edebilirsiniz. Kargoya verildikten sonra iptal için iade işlemi başlatmanız gerekir.",
                "keywords": ["sipariş", "iptal", "vazgeçme"],
                "priority": 9
            },
            {
                "category": "sipariş",
                "question": "Sipariş durumu nasıl öğrenilir?",
                "answer": "Hesabınıza giriş yaparak 'Siparişlerim' sayfasından sipariş durumunuzu anlık olarak takip edebilirsiniz. Ayrıca her aşamada e-posta ve SMS ile bilgilendirme yapılır.",
                "keywords": ["sipariş", "durum", "takip", "sorgulama"],
                "priority": 8
            },
            # Hesap
            {
                "category": "hesap",
                "question": "Şifremi unuttum ne yapmalıyım?",
                "answer": "Giriş sayfasındaki 'Şifremi Unuttum' linkine tıklayın. E-posta adresinizi girin, size gönderilen link ile şifrenizi yenileyebilirsiniz.",
                "keywords": ["şifre", "parola", "unuttum", "giriş"],
                "priority": 7
            },
            {
                "category": "hesap",
                "question": "Hesabımı nasıl silerim?",
                "answer": "Hesap silme işlemi için müşteri hizmetleri ile iletişime geçmeniz gerekmektedir. KVKK kapsamında verileriniz silinecektir.",
                "keywords": ["hesap", "silme", "kapatma", "KVKK"],
                "priority": 5
            },
            # Ürün
            {
                "category": "ürün",
                "question": "Ürün stokta yok ne zaman gelir?",
                "answer": "Stokta olmayan ürünler için 'Gelince Haber Ver' butonunu kullanabilirsiniz. Ürün stoğa girdiğinde e-posta ile bilgilendirilirsiniz.",
                "keywords": ["stok", "tükendi", "yok", "bekleme"],
                "priority": 6
            },
            {
                "category": "ürün",
                "question": "Ürün garantisi var mı?",
                "answer": "Tüm ürünlerimiz 2 yıl resmi distribütör garantisi ile satılmaktadır. Garanti belgesi ürünle birlikte gönderilir.",
                "keywords": ["garanti", "servis", "onarım"],
                "priority": 7
            },
        ]
        
        count = 0
        for entry in knowledge:
            self.db.add_knowledge(**entry)
            count += 1
        
        return count
    
    def load_default_tech_support_kb(self) -> int:
        """
        Default knowledge base for technical support
        
        Returns:
            Number of loaded records
        """
        knowledge = [
            {
                "category": "bağlantı",
                "question": "İnternete bağlanamıyorum",
                "answer": "1) Modem/router'ı kapatıp 30 saniye bekleyin ve tekrar açın. 2) Wi-Fi şifrenizi kontrol edin. 3) Cihazınızın uçak modunda olmadığından emin olun. 4) Başka cihazlarla da bağlantı deneyin.",
                "keywords": ["internet", "bağlantı", "wifi", "ağ"],
                "priority": 10
            },
            {
                "category": "şifre",
                "question": "Şifremi nasıl sıfırlarım?",
                "answer": "Giriş ekranında 'Şifremi Unuttum' seçeneğine tıklayın. Kayıtlı e-posta adresinize şifre sıfırlama linki gelecektir. Link 24 saat geçerlidir.",
                "keywords": ["şifre", "parola", "sıfırlama", "unutma"],
                "priority": 9
            },
            {
                "category": "yavaşlık",
                "question": "Program çok yavaş çalışıyor",
                "answer": "1) Gereksiz arka plan uygulamalarını kapatın. 2) Bilgisayarınızı yeniden başlatın. 3) Disk temizliği yapın. 4) RAM kullanımını kontrol edin. 5) Antivirüs taraması yapın.",
                "keywords": ["yavaş", "donma", "performans", "hız"],
                "priority": 8
            },
            {
                "category": "kurulum",
                "question": "Programı nasıl kurarım?",
                "answer": "1) İndirdiğiniz setup dosyasına çift tıklayın. 2) Kurulum sihirbazını takip edin. 3) Lisans anlaşmasını kabul edin. 4) Kurulum dizinini seçin. 5) 'Kur' butonuna tıklayın.",
                "keywords": ["kurulum", "yükleme", "install", "setup"],
                "priority": 7
            },
        ]
        
        count = 0
        for entry in knowledge:
            self.db.add_knowledge(**entry)
            count += 1
        
        return count
    
    def export_to_json(self, output_file: str, 
                       category: Optional[str] = None) -> None:
        """
        Export knowledge base to JSON file
        
        Args:
            output_file: Output file
            category: Category filter (optional)
        """
        cursor = self.db.conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT category, question, answer, keywords, priority
                FROM knowledge_base
                WHERE active = 1 AND category = ?
                ORDER BY category, priority DESC
            """, (category,))
        else:
            cursor.execute("""
                SELECT category, question, answer, keywords, priority
                FROM knowledge_base
                WHERE active = 1
                ORDER BY category, priority DESC
            """)
        
        rows = cursor.fetchall()
        
        knowledge_list = []
        for row in rows:
            entry = dict(row)
            if entry.get('keywords'):
                entry['keywords'] = json.loads(entry['keywords'])
            knowledge_list.append(entry)
        
        output = {"knowledge_base": knowledge_list}
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)


def create_sample_kb_files():
    """Create sample knowledge base files"""
    
    # E-ticaret JSON
    ecommerce_kb = {
        "knowledge_base": [
            {
                "category": "shipping",
                "question": "Kargom ne zaman gelir?",
                "answer": "2-3 iş günü içinde kargoya verilir, 3-5 iş günü içinde teslim edilir.",
                "keywords": ["kargo", "teslimat", "süre"],
                "priority": 10
            },
            {
                "category": "iade",
                "question": "Ürün iadesi nasıl yapılır?",
                "answer": "14 gün içinde iade edebilirsiniz. Siparişlerim sayfasından iade talebi oluşturun.",
                "keywords": ["iade", "geri gönderme"],
                "priority": 10
            }
        ]
    }
    
    Path("knowledge_samples").mkdir(exist_ok=True)
    
    with open("knowledge_samples/ecommerce_kb.json", 'w', encoding='utf-8') as f:
        json.dump(ecommerce_kb, f, ensure_ascii=False, indent=2)
    
    # YAML versiyonu
    yaml_content = """knowledge_base:
  - category: kargo
    question: Kargom ne zaman gelir?
    answer: 2-3 iş günü içinde kargoya verilir, 3-5 iş günü içinde teslim edilir.
    keywords:
      - kargo
      - teslimat
      - süre
    priority: 10
    
  - category: iade
    question: Ürün iadesi nasıl yapılır?
    answer: 14 gün içinde iade edebilirsiniz. Siparişlerim sayfasından iade talebi oluşturun.
    keywords:
      - iade
      - geri gönderme
    priority: 10
"""
    
    with open("knowledge_samples/ecommerce_kb.yaml", 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print("✅ Sample knowledge base files created:")
    print("   - knowledge_samples/ecommerce_kb.json")
    print("   - knowledge_samples/ecommerce_kb.yaml")


if __name__ == "__main__":
    create_sample_kb_files()

