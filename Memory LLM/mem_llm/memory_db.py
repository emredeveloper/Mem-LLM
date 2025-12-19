"""
SQL Database Memory Management
Stores memory data using SQLite - Production-ready
"""

import json
import logging
import sqlite3
import threading
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Optional vector store support
try:
    from .vector_store import VectorStore, create_vector_store

    VECTOR_STORE_AVAILABLE = True
except ImportError:
    VECTOR_STORE_AVAILABLE = False
    VectorStore = None


class SQLMemoryManager:
    """SQLite-based memory management system with thread-safety"""

    def __init__(
        self,
        db_path: str = "memories/memories.db",
        enable_vector_search: bool = False,
        vector_store_type: str = "chroma",
        embedding_model: str = "nomic-embed-text-v2-moe:latest",
    ):
        """
        Args:
            db_path: SQLite database file path
            enable_vector_search: Enable vector/semantic search (optional)
            vector_store_type: Type of vector store ('chroma', etc.)
            embedding_model: Embedding model name (sentence-transformers)
        """
        self.db_path = Path(db_path)

        # Ensure directory exists
        db_dir = self.db_path.parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)

        self.conn = None
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._init_database()

        # Vector store (optional)
        self.enable_vector_search = enable_vector_search
        self.vector_store: Optional[VectorStore] = None

        if enable_vector_search:
            if not VECTOR_STORE_AVAILABLE:
                logger.warning(
                    "Vector search requested but dependencies not available. "
                    "Install with: pip install chromadb sentence-transformers"
                )
                self.enable_vector_search = False
            else:
                try:
                    persist_dir = str(db_dir / "vector_store")
                    self.vector_store = create_vector_store(
                        store_type=vector_store_type,
                        collection_name="knowledge_base",
                        persist_directory=persist_dir,
                        embedding_model=embedding_model,
                    )
                    if self.vector_store:
                        logger.info(f"Vector search enabled: {vector_store_type}")
                    else:
                        logger.warning(
                            "Failed to initialize vector store, falling back to keyword search"
                        )
                        self.enable_vector_search = False
                except (ValueError, json.JSONDecodeError) as e:
                    logger.error(f"Error initializing vector store due to data format: {e}")
                    self.enable_vector_search = False
                except Exception as e:
                    logger.error(f"An unexpected error occurred initializing vector store: {e}")
                    self.enable_vector_search = False

    def _init_database(self) -> None:
        """Create database and tables"""
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0,  # 30 second timeout for busy database
            isolation_level=None,  # Autocommit mode
        )
        self.conn.row_factory = sqlite3.Row

        # Enable WAL mode for better concurrency
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
        self.conn.execute("PRAGMA busy_timeout=30000")  # 30 second busy timeout

        cursor = self.conn.cursor()

        # User profiles table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP,
                preferences TEXT,
                summary TEXT,
                metadata TEXT
            )
        """
        )

        # Conversations table
        cursor.execute(
            """
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
        """
        )

        # İndeksler - Performans için
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_timestamp
            ON conversations(user_id, timestamp DESC)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_resolved
            ON conversations(user_id, resolved)
        """
        )

        # Senaryo şablonları tablosu
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scenario_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                system_prompt TEXT NOT NULL,
                example_interactions TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Problem/FAQ veritabanı
        cursor.execute(
            """
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
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_category
            ON knowledge_base(category, active)
        """
        )

        self.conn.commit()

    def add_user(
        self, user_id: str, name: Optional[str] = None, metadata: Optional[Dict] = None
    ) -> None:
        """
        Add new user or update existing (thread-safe)

        Args:
            user_id: User ID
            name: User name
            metadata: Additional information
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (user_id, name, metadata)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    name = COALESCE(excluded.name, users.name),
                    metadata = COALESCE(excluded.metadata, users.metadata)
            """,
                (user_id, name, json.dumps(metadata or {})),
            )

    def add_interaction(
        self,
        user_id: str,
        user_message: str,
        bot_response: str,
        metadata: Optional[Dict] = None,
        resolved: bool = False,
    ) -> int:
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
            cursor.execute(
                """
                INSERT INTO conversations
                (user_id, user_message, bot_response, metadata, resolved)
                VALUES (?, ?, ?, ?, ?)
            """,
                (user_id, user_message, bot_response, json.dumps(metadata or {}), resolved),
            )

            interaction_id = cursor.lastrowid

            # Update user's last interaction time
            cursor.execute(
                """
                UPDATE users
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """,
                (user_id,),
            )

            return interaction_id

    # Alias for compatibility
    def add_conversation(
        self, user_id: str, user_message: str, bot_response: str, metadata: Optional[Dict] = None
    ) -> int:
        """Alias for add_interaction"""
        return self.add_interaction(user_id, user_message, bot_response, metadata)

    def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get user's recent conversations (thread-safe)

        Args:
            user_id: User identifier
            limit: Number of conversations to retrieve

        Returns:
            List of conversations
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT timestamp, user_message, bot_response, metadata, resolved
                FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (user_id, limit),
            )

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def search_conversations(self, user_id: str, keyword: str) -> List[Dict]:
        """
        Search for keywords in conversations (thread-safe)

        Args:
            user_id: User identifier
            keyword: Keyword to search for

        Returns:
            Matching conversations
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT timestamp, user_message, bot_response, metadata, resolved
            FROM conversations
            WHERE user_id = ?
            AND (user_message LIKE ? OR bot_response LIKE ? OR metadata LIKE ?)
            ORDER BY timestamp DESC
        """,
            (user_id, f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile

        Args:
            user_id: User identifier

        Returns:
            User profile or None
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE user_id = ?
        """,
            (user_id,),
        )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def update_user_profile(self, user_id: str, updates: Dict) -> None:
        """
        Update user profile

        Args:
            user_id: User identifier
            updates: Fields to update
        """
        allowed_fields = ["name", "preferences", "summary", "metadata"]
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
            cursor.execute(
                f"""
                UPDATE users
                SET {', '.join(set_clause)}
                WHERE user_id = ?
            """,
                values,
            )
            self.conn.commit()

    def add_knowledge(
        self,
        category: str,
        question: str,
        answer: str,
        keywords: Optional[List[str]] = None,
        priority: int = 0,
    ) -> int:
        """
        Add new entry to knowledge base

        Args:
            category: Category (e.g., "shipping", "returns", "payment")
            question: Question
            answer: Answer
            keywords: Keywords
            priority: Priority (higher = shown first)

        Returns:
            Entry ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO knowledge_base
            (category, question, answer, keywords, priority)
            VALUES (?, ?, ?, ?, ?)
        """,
            (category, question, answer, json.dumps(keywords or []), priority),
        )

        kb_id = cursor.lastrowid
        self.conn.commit()

        # Sync to vector store if enabled
        if self.enable_vector_search and self.vector_store:
            try:
                self._sync_to_vector_store(kb_id)
            except Exception as e:
                logger.warning(f"Failed to sync KB entry to vector store: {e}")

        return kb_id

    def search_knowledge(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5,
        use_vector_search: Optional[bool] = None,
    ) -> List[Dict]:
        """
        Search in knowledge base (keyword matching or semantic search)

        Args:
            query: Search query
            category: Category filter (optional)
            limit: Maximum number of results
            use_vector_search: Force vector search (None = auto-detect)

        Returns:
            Found entries
        """
        # Use vector search if enabled and available
        if use_vector_search is None:
            use_vector_search = self.enable_vector_search

        if use_vector_search and self.vector_store:
            return self._vector_search(query, category, limit)
        else:
            return self._keyword_search(query, category, limit)

    def _keyword_search(
        self, query: str, category: Optional[str] = None, limit: int = 5
    ) -> List[Dict]:
        """Traditional keyword-based search"""
        cursor = self.conn.cursor()

        # Extract important keywords from query (remove question words)
        import re

        stopwords = [
            "ne",
            "kadar",
            "nedir",
            "nasıl",
            "için",
            "mı",
            "mi",
            "mu",
            "mü",
            "what",
            "how",
            "when",
            "where",
            "is",
            "are",
            "the",
            "a",
            "an",
        ]

        # Clean query and extract keywords
        query_lower = query.lower()
        words = re.findall(r"\w+", query_lower)
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

    def _vector_search(
        self, query: str, category: Optional[str] = None, limit: int = 5
    ) -> List[Dict]:
        """Vector-based semantic search"""
        if not self.vector_store:
            return []

        # Prepare metadata filter
        filter_metadata = None
        if category:
            filter_metadata = {"category": category}

        # Search in vector store
        vector_results = self.vector_store.search(
            query=query,
            limit=limit * 2,  # Get more results to filter by category if needed
            filter_metadata=filter_metadata,
        )

        # Map vector results back to KB format
        results = []
        for result in vector_results[:limit]:
            # Extract metadata
            metadata = result.get("metadata", {})

            results.append(
                {
                    "category": metadata.get("category", ""),
                    "question": metadata.get("question", ""),
                    "answer": result.get("text", ""),
                    "priority": metadata.get("priority", 0),
                    "score": result.get("score", 0.0),  # Similarity score
                    "vector_search": True,
                }
            )

        return results

    def _sync_to_vector_store(self, kb_id: int) -> None:
        """Sync a single KB entry to vector store"""
        if not self.vector_store:
            return

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, category, question, answer, keywords, priority
            FROM knowledge_base
            WHERE id = ?
        """,
            (kb_id,),
        )

        row = cursor.fetchone()
        if row:
            doc = {
                "id": str(row["id"]),
                "text": f"{row['question']}\n{row['answer']}",  # Combine for better search
                "metadata": {
                    "category": row["category"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "keywords": row["keywords"],
                    "priority": row["priority"],
                    "kb_id": row["id"],
                },
            }
            self.vector_store.add_documents([doc])

    def sync_all_kb_to_vector_store(self) -> int:
        """
        Sync all existing KB entries to vector store

        Returns:
            Number of entries synced
        """
        if not self.vector_store:
            return 0

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, category, question, answer, keywords, priority
            FROM knowledge_base
            WHERE active = 1
        """
        )

        rows = cursor.fetchall()
        documents = []

        for row in rows:
            doc = {
                "id": str(row["id"]),
                "text": f"{row['question']}\n{row['answer']}",
                "metadata": {
                    "category": row["category"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "keywords": row["keywords"],
                    "priority": row["priority"],
                    "kb_id": row["id"],
                },
            }
            documents.append(doc)

        if documents:
            try:
                # Add in batches for better performance
                batch_size = 100
                for i in range(0, len(documents), batch_size):
                    batch = documents[i : i + batch_size]
                    self.vector_store.add_documents(batch)
                    logger.debug(f"Synced {len(batch)} KB entries to vector store")

                logger.info(f"Synced {len(documents)} KB entries to vector store")
            except Exception as e:
                logger.error(f"Error syncing KB to vector store: {e}")
                return 0

        return len(documents)

    def get_statistics(self) -> Dict:
        """
        Return general statistics

        Returns:
            Statistics information
        """
        cursor = self.conn.cursor()

        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()["count"]

        # Total interactions
        cursor.execute("SELECT COUNT(*) as count FROM conversations")
        total_interactions = cursor.fetchone()["count"]

        # Unresolved issues
        cursor.execute("SELECT COUNT(*) as count FROM conversations WHERE resolved = 0")
        unresolved = cursor.fetchone()["count"]

        # Knowledge base entry count
        cursor.execute("SELECT COUNT(*) as count FROM knowledge_base WHERE active = 1")
        kb_count = cursor.fetchone()["count"]

        return {
            "total_users": total_users,
            "total_interactions": total_interactions,
            "unresolved_issues": unresolved,
            "knowledge_base_entries": kb_count,
            "avg_interactions_per_user": total_interactions / total_users if total_users > 0 else 0,
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
