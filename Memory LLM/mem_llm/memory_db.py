"""
SQL Database Memory Management
Stores memory data using SQLite - Production-ready
"""

import sqlite3
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SQLMemoryManager:
    """SQLite-based memory management system with thread-safety"""
    
    def __init__(self, db_path: str = "memories/memories.db"):
        """
        Args:
            db_path: SQLite database file path
        """
        self.db_path = Path(db_path)
        
        # Ensure directory exists
        db_dir = self.db_path.parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._init_database()
    
    def _init_database(self) -> None:
        """Create database and tables"""
        self.conn = sqlite3.connect(
            str(self.db_path), 
            check_same_thread=False,
            timeout=30.0,  # 30 second timeout for busy database
            isolation_level=None  # Autocommit mode
        )
        self.conn.row_factory = sqlite3.Row
        
        # Enable WAL mode for better concurrency
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
        self.conn.execute("PRAGMA busy_timeout=30000")  # 30 second busy timeout
        
        cursor = self.conn.cursor()
        
        # User profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP,
                preferences TEXT,
                summary TEXT,
                metadata TEXT
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                metadata TEXT,
                sentiment TEXT,
                resolved BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # İndeksler - Performans için
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_timestamp 
            ON conversations(user_id, timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_resolved 
            ON conversations(user_id, resolved)
        """)
        
        # Senaryo şablonları tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenario_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                system_prompt TEXT NOT NULL,
                example_interactions TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Problem/FAQ veritabanı
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                keywords TEXT,
                priority INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category 
            ON knowledge_base(category, active)
        """)
        
        self.conn.commit()
    
    def add_user(self, user_id: str, name: Optional[str] = None, 
                 metadata: Optional[Dict] = None) -> None:
        """
        Add new user or update existing (thread-safe)
        
        Args:
            user_id: User ID
            name: User name
            metadata: Additional information
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, name, metadata)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    name = COALESCE(excluded.name, users.name),
                    metadata = COALESCE(excluded.metadata, users.metadata)
            """, (user_id, name, json.dumps(metadata or {})))
    
    def add_interaction(self, user_id: str, user_message: str, 
                       bot_response: str, metadata: Optional[Dict] = None,
                       resolved: bool = False) -> int:
        """
        Record new interaction (thread-safe)
        
        Args:
            user_id: User ID
            user_message: User's message
            bot_response: Bot's response
            metadata: Additional information
            resolved: Is issue resolved?
            
        Returns:
            Added record ID
        """
        if not user_message or not bot_response:
            raise ValueError("user_message and bot_response cannot be None or empty")
        
        with self._lock:
            cursor = self.conn.cursor()
            
            # Create user if not exists
            self.add_user(user_id)
            
            # Record interaction
            cursor.execute("""
                INSERT INTO conversations 
                (user_id, user_message, bot_response, metadata, resolved)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, user_message, bot_response, 
                  json.dumps(metadata or {}), resolved))
            
            interaction_id = cursor.lastrowid
            
            # Update user's last interaction time
            cursor.execute("""
                UPDATE users 
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (user_id,))
            
            return interaction_id
    
    # Alias for compatibility
    def add_conversation(self, user_id: str, user_message: str, bot_response: str, metadata: Optional[Dict] = None) -> int:
        """Alias for add_interaction"""
        return self.add_interaction(user_id, user_message, bot_response, metadata)
    
    def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Kullanıcının son konuşmalarını getirir (thread-safe)
        
        Args:
            user_id: Kullanıcı kimliği
            limit: Getirilecek konuşma sayısı
            
        Returns:
            Konuşmalar listesi
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT timestamp, user_message, bot_response, metadata, resolved
                FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def search_conversations(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Konuşmalarda anahtar kelime arar (thread-safe)
        
        Args:
            user_id: Kullanıcı kimliği
            keyword: Aranacak kelime
            
        Returns:
            Eşleşen konuşmalar
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, user_message, bot_response, metadata, resolved
            FROM conversations
            WHERE user_id = ?
            AND (user_message LIKE ? OR bot_response LIKE ? OR metadata LIKE ?)
            ORDER BY timestamp DESC
        """, (user_id, f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Kullanıcı profilini getirir
        
        Args:
            user_id: Kullanıcı kimliği
            
        Returns:
            Kullanıcı profili veya None
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def update_user_profile(self, user_id: str, updates: Dict) -> None:
        """
        Kullanıcı profilini günceller
        
        Args:
            user_id: Kullanıcı kimliği
            updates: Güncellenecek alanlar
        """
        allowed_fields = ['name', 'preferences', 'summary', 'metadata']
        set_clause = []
        values = []
        
        for field, value in updates.items():
            if field in allowed_fields:
                set_clause.append(f"{field} = ?")
                if isinstance(value, (dict, list)):
                    values.append(json.dumps(value))
                else:
                    values.append(value)
        
        if set_clause:
            values.append(user_id)
            cursor = self.conn.cursor()
            cursor.execute(f"""
                UPDATE users 
                SET {', '.join(set_clause)}
                WHERE user_id = ?
            """, values)
            self.conn.commit()
    
    def add_knowledge(self, category: str, question: str, answer: str,
                     keywords: Optional[List[str]] = None,
                     priority: int = 0) -> int:
        """
        Bilgi bankasına yeni kayıt ekler
        
        Args:
            category: Kategori (örn: "kargo", "iade", "ödeme")
            question: Soru
            answer: Cevap
            keywords: Anahtar kelimeler
            priority: Öncelik (yüksek = önce gösterilir)
            
        Returns:
            Kayıt ID'si
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge_base 
            (category, question, answer, keywords, priority)
            VALUES (?, ?, ?, ?, ?)
        """, (category, question, answer, 
              json.dumps(keywords or []), priority))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def search_knowledge(self, query: str, category: Optional[str] = None,
                        limit: int = 5) -> List[Dict]:
        """
        Bilgi bankasında arama yapar (gelişmiş keyword matching)
        
        Args:
            query: Arama sorgusu
            category: Kategori filtresi (opsiyonel)
            limit: Maksimum sonuç sayısı
            
        Returns:
            Bulunan kayıtlar
        """
        cursor = self.conn.cursor()
        
        # Extract important keywords from query (remove question words)
        import re
        stopwords = ['ne', 'kadar', 'nedir', 'nasıl', 'için', 'mı', 'mi', 'mu', 'mü', 
                     'what', 'how', 'when', 'where', 'is', 'are', 'the', 'a', 'an']
        
        # Clean query and extract keywords
        query_lower = query.lower()
        words = re.findall(r'\w+', query_lower)
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        # If no keywords, use original query
        if not keywords:
            keywords = [query_lower]
        
        # Build search conditions for each keyword
        conditions = []
        params = []
        
        for keyword in keywords[:5]:  # Max 5 keywords
            conditions.append("(question LIKE ? OR answer LIKE ? OR keywords LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        
        where_clause = " OR ".join(conditions) if conditions else "1=1"
        
        if category:
            sql = f"""
                SELECT category, question, answer, priority
                FROM knowledge_base
                WHERE active = 1 
                AND category = ?
                AND ({where_clause})
                ORDER BY priority DESC, id DESC
                LIMIT ?
            """
            cursor.execute(sql, [category] + params + [limit])
        else:
            sql = f"""
                SELECT category, question, answer, priority
                FROM knowledge_base
                WHERE active = 1 
                AND ({where_clause})
                ORDER BY priority DESC, id DESC
                LIMIT ?
            """
            cursor.execute(sql, params + [limit])
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """
        Genel istatistikleri döndürür
        
        Returns:
            İstatistik bilgileri
        """
        cursor = self.conn.cursor()
        
        # Toplam kullanıcı
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        # Toplam etkileşim
        cursor.execute("SELECT COUNT(*) as count FROM conversations")
        total_interactions = cursor.fetchone()['count']
        
        # Çözülmemiş sorunlar
        cursor.execute("SELECT COUNT(*) as count FROM conversations WHERE resolved = 0")
        unresolved = cursor.fetchone()['count']
        
        # Bilgi bankası kayıt sayısı
        cursor.execute("SELECT COUNT(*) as count FROM knowledge_base WHERE active = 1")
        kb_count = cursor.fetchone()['count']
        
        return {
            "total_users": total_users,
            "total_interactions": total_interactions,
            "unresolved_issues": unresolved,
            "knowledge_base_entries": kb_count,
            "avg_interactions_per_user": total_interactions / total_users if total_users > 0 else 0
        }
    
    def clear_memory(self, user_id: str) -> None:
        """Delete all user conversations"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        self.conn.commit()
    
    def close(self) -> None:
        """Veritabanı bağlantısını kapatır"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

