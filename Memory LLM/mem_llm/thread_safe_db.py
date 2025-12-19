"""
Thread-Safe Database Connection Pool
=====================================
Provides thread-safe SQLite connections with proper transaction management
"""

import logging
import queue
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Optional


class ConnectionPool:
    """Thread-safe SQLite connection pool"""

    def __init__(self, db_path: str, pool_size: int = 5):
        """
        Initialize connection pool

        Args:
            db_path: Path to SQLite database
            pool_size: Maximum number of connections
        """
        self.db_path = Path(db_path)
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size)
        self.local = threading.local()
        self._lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

        # Pre-create connections
        for _ in range(pool_size):
            conn = self._create_connection()
            self.pool.put(conn)

    def _create_connection(self) -> sqlite3.Connection:
        """Create a new connection with proper settings"""
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0,  # 30 second timeout
            isolation_level=None,  # Autocommit mode for better concurrency
        )
        conn.row_factory = sqlite3.Row

        # Enable WAL mode and optimizations
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-64000")
        conn.execute("PRAGMA busy_timeout=30000")  # 30 second busy timeout

        return conn

    @contextmanager
    def get_connection(self):
        """
        Get a connection from pool (context manager)

        Usage:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ...")
        """
        # Check if thread already has a connection
        if hasattr(self.local, "conn") and self.local.conn:
            yield self.local.conn
            return

        # Get connection from pool
        conn = None
        try:
            conn = self.pool.get(timeout=10.0)
            self.local.conn = conn
            yield conn
        except queue.Empty:
            self.logger.error("Connection pool exhausted")
            # Create temporary connection
            conn = self._create_connection()
            yield conn
        finally:
            # Return to pool
            if conn and hasattr(self.local, "conn"):
                self.local.conn = None
                try:
                    self.pool.put_nowait(conn)
                except queue.Full:
                    conn.close()

    @contextmanager
    def transaction(self):
        """
        Execute operations in a transaction

        Usage:
            with pool.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT ...")
                cursor.execute("UPDATE ...")
            # Automatically committed
        """
        with self.get_connection() as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                yield conn
                conn.execute("COMMIT")
            except Exception as e:
                conn.execute("ROLLBACK")
                self.logger.error(f"Transaction rolled back: {e}")
                raise

    def close_all(self):
        """Close all connections in pool"""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                conn.close()
            except queue.Empty:
                break


class ThreadSafeSQLMemory:
    """Thread-safe wrapper for SQL memory operations"""

    def __init__(self, db_path: str = "memories/memories.db", pool_size: int = 5):
        """
        Initialize thread-safe SQL memory

        Args:
            db_path: Database file path
            pool_size: Connection pool size
        """
        self.db_path = Path(db_path)

        # Ensure directory exists
        db_dir = self.db_path.parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)

        self.pool = ConnectionPool(str(db_path), pool_size)
        self.logger = logging.getLogger(__name__)
        self._init_database()

    def _init_database(self):
        """Initialize database schema"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()

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

            # Indexes for performance
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

            # Knowledge base table
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

            conn.commit()

    def add_user(self, user_id: str, name: Optional[str] = None, metadata: Optional[dict] = None):
        """Thread-safe user addition"""
        import json

        with self.pool.transaction() as conn:
            cursor = conn.cursor()
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
        metadata: Optional[dict] = None,
        resolved: bool = False,
    ) -> int:
        """Thread-safe interaction addition"""
        import json

        if not user_message or not bot_response:
            raise ValueError("Messages cannot be None or empty")

        with self.pool.transaction() as conn:
            cursor = conn.cursor()

            # Ensure user exists
            self.add_user(user_id)

            # Add interaction
            cursor.execute(
                """
                INSERT INTO conversations
                (user_id, user_message, bot_response, metadata, resolved)
                VALUES (?, ?, ?, ?, ?)
            """,
                (user_id, user_message, bot_response, json.dumps(metadata or {}), resolved),
            )

            interaction_id = cursor.lastrowid

            # Update last interaction time
            cursor.execute(
                """
                UPDATE users
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """,
                (user_id,),
            )

            return interaction_id

    def get_recent_conversations(self, user_id: str, limit: int = 10) -> list:
        """Thread-safe conversation retrieval"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
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

    def search_conversations(self, user_id: str, keyword: str) -> list:
        """Thread-safe conversation search"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT timestamp, user_message, bot_response, metadata
                FROM conversations
                WHERE user_id = ?
                AND (user_message LIKE ? OR bot_response LIKE ?)
                ORDER BY timestamp DESC
                LIMIT 100
            """,
                (user_id, f"%{keyword}%", f"%{keyword}%"),
            )

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def close(self):
        """Close connection pool"""
        self.pool.close_all()

    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.close()
        except Exception:
            pass
