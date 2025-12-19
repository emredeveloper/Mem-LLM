"""
Data Export/Import System
Supports multiple formats and databases: JSON, CSV, SQLite, PostgreSQL, MongoDB
"""

import csv
import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DataExporter:
    """Export memory data to various formats and databases"""

    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: MemoryManager or SQLMemoryManager instance
        """
        self.memory = memory_manager

    def export_to_json(self, user_id: str, output_file: str) -> Dict[str, Any]:
        """
        Export user data to JSON file

        Args:
            user_id: User ID to export
            output_file: Output JSON file path

        Returns:
            Export statistics
        """
        try:
            # Get all user data
            conversations = self.memory.get_recent_conversations(user_id, limit=1000)
            profile = getattr(self.memory, "user_profiles", {}).get(user_id, {})

            data = {
                "user_id": user_id,
                "export_date": datetime.now().isoformat(),
                "conversations": conversations,
                "profile": profile,
                "metadata": {
                    "total_conversations": len(conversations),
                    "format": "json",
                    "version": "1.0",
                },
            }

            # Write to file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"Exported {len(conversations)} conversations to {output_file}")

            return {
                "success": True,
                "file": str(output_path),
                "conversations": len(conversations),
                "size_bytes": output_path.stat().st_size,
            }

        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return {"success": False, "error": str(e)}

    def export_to_csv(self, user_id: str, output_file: str) -> Dict[str, Any]:
        """
        Export conversations to CSV file

        Args:
            user_id: User ID to export
            output_file: Output CSV file path

        Returns:
            Export statistics
        """
        try:
            conversations = self.memory.get_recent_conversations(user_id, limit=1000)

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["timestamp", "user_message", "bot_response", "metadata"]
                )
                writer.writeheader()

                for conv in conversations:
                    writer.writerow(
                        {
                            "timestamp": conv.get("timestamp", ""),
                            "user_message": conv.get("user_message", ""),
                            "bot_response": conv.get("bot_response", ""),
                            "metadata": json.dumps(conv.get("metadata", {})),
                        }
                    )

            logger.info(f"Exported {len(conversations)} conversations to CSV: {output_file}")

            return {
                "success": True,
                "file": str(output_path),
                "conversations": len(conversations),
                "size_bytes": output_path.stat().st_size,
            }

        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return {"success": False, "error": str(e)}

    def export_to_sqlite(self, user_id: str, db_file: str) -> Dict[str, Any]:
        """
        Export to SQLite database

        Args:
            user_id: User ID to export
            db_file: SQLite database file path

        Returns:
            Export statistics
        """
        try:
            conversations = self.memory.get_recent_conversations(user_id, limit=1000)

            db_path = Path(db_file)
            db_path.parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Create table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    metadata TEXT
                )
            """
            )

            # Insert conversations
            for conv in conversations:
                cursor.execute(
                    """
                    INSERT INTO conversations
                    (user_id, timestamp, user_message, bot_response, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        conv.get("timestamp", datetime.now().isoformat()),
                        conv.get("user_message", ""),
                        conv.get("bot_response", ""),
                        json.dumps(conv.get("metadata", {})),
                    ),
                )

            conn.commit()
            conn.close()

            logger.info(f"Exported {len(conversations)} conversations to SQLite: {db_file}")

            return {
                "success": True,
                "file": str(db_path),
                "conversations": len(conversations),
                "size_bytes": db_path.stat().st_size,
            }

        except Exception as e:
            logger.error(f"SQLite export failed: {e}")
            return {"success": False, "error": str(e)}

    def export_to_postgresql(self, user_id: str, connection_string: str) -> Dict[str, Any]:
        """
        Export to PostgreSQL database

        Args:
            user_id: User ID to export
            connection_string: PostgreSQL connection string
                             (e.g., "postgresql://user:pass@localhost/dbname")

        Returns:
            Export statistics
        """
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        except ImportError:
            return {
                "success": False,
                "error": "psycopg2 not installed. Install: pip install psycopg2-binary",
            }

        try:
            conversations = self.memory.get_recent_conversations(user_id, limit=1000)

            # Parse connection string to get database name
            import re

            match = re.search(r"/([^/]+)(?:\?|$)", connection_string)
            db_name = match.group(1) if match else None

            # Try to connect, if database doesn't exist, create it
            try:
                conn = psycopg2.connect(connection_string)
            except psycopg2.OperationalError as e:
                if "does not exist" in str(e) and db_name:
                    # Connect to default 'postgres' database to create new one
                    base_conn_string = connection_string.rsplit("/", 1)[0] + "/postgres"
                    temp_conn = psycopg2.connect(base_conn_string)
                    temp_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    temp_cursor = temp_conn.cursor()
                    temp_cursor.execute(f"CREATE DATABASE {db_name}")
                    temp_cursor.close()
                    temp_conn.close()
                    logger.info(f"Created PostgreSQL database: {db_name}")

                    # Now connect to the new database
                    conn = psycopg2.connect(connection_string)
                else:
                    raise

            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    metadata JSONB
                )
            """
            )

            # Insert conversations
            for conv in conversations:
                cursor.execute(
                    """
                    INSERT INTO conversations
                    (user_id, timestamp, user_message, bot_response, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        user_id,
                        conv.get("timestamp", datetime.now().isoformat()),
                        conv.get("user_message", ""),
                        conv.get("bot_response", ""),
                        json.dumps(conv.get("metadata", {})),
                    ),
                )

            conn.commit()
            cursor.close()
            conn.close()

            logger.info(f"Exported {len(conversations)} conversations to PostgreSQL")

            return {
                "success": True,
                "database": "postgresql",
                "conversations": len(conversations),
                "database_created": db_name is not None,
            }

        except Exception as e:
            logger.error(f"PostgreSQL export failed: {e}")
            return {"success": False, "error": str(e)}

    def export_to_mongodb(
        self,
        user_id: str,
        connection_string: str,
        database: str = "mem_llm",
        collection: str = "conversations",
    ) -> Dict[str, Any]:
        """
        Export to MongoDB database

        Args:
            user_id: User ID to export
            connection_string: MongoDB connection string
                             (e.g., "mongodb://localhost:27017/")
            database: Database name
            collection: Collection name

        Returns:
            Export statistics
        """
        try:
            from pymongo import MongoClient
        except ImportError:
            return {
                "success": False,
                "error": "pymongo not installed. Install: pip install pymongo",
            }

        try:
            conversations = self.memory.get_recent_conversations(user_id, limit=1000)

            client = MongoClient(connection_string)

            # MongoDB automatically creates database and collection if they don't exist
            db = client[database]
            coll = db[collection]

            # Check if this is a new database/collection
            is_new_db = database not in client.list_database_names()
            is_new_collection = collection not in db.list_collection_names()

            if is_new_db:
                logger.info(f"Creating MongoDB database: {database}")
            if is_new_collection:
                logger.info(f"Creating MongoDB collection: {collection}")

            # Prepare documents
            documents = []
            for conv in conversations:
                doc = {
                    "user_id": user_id,
                    "timestamp": conv.get("timestamp", datetime.now().isoformat()),
                    "user_message": conv.get("user_message", ""),
                    "bot_response": conv.get("bot_response", ""),
                    "metadata": conv.get("metadata", {}),
                    "export_date": datetime.now(),
                }
                documents.append(doc)

            # Insert documents
            result = coll.insert_many(documents)

            client.close()

            logger.info(f"Exported {len(conversations)} conversations to MongoDB")

            return {
                "success": True,
                "database": "mongodb",
                "conversations": len(conversations),
                "inserted_ids": len(result.inserted_ids),
                "database_created": is_new_db,
                "collection_created": is_new_collection,
            }

        except Exception as e:
            logger.error(f"MongoDB export failed: {e}")
            return {"success": False, "error": str(e)}


class DataImporter:
    """Import memory data from various formats and databases"""

    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: MemoryManager or SQLMemoryManager instance
        """
        self.memory = memory_manager

    def import_from_json(self, input_file: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Import user data from JSON file

        Args:
            input_file: Input JSON file path
            user_id: Override user ID (use file's user_id if None)

        Returns:
            Import statistics
        """
        try:
            input_path = Path(input_file)

            if not input_path.exists():
                return {"success": False, "error": f"File not found: {input_file}"}

            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Get user ID
            target_user_id = user_id or data.get("user_id")
            if not target_user_id:
                return {"success": False, "error": "No user_id specified"}

            # Import conversations
            conversations = data.get("conversations", [])
            imported = 0

            for conv in conversations:
                self.memory.add_conversation(
                    target_user_id,
                    conv.get("user_message", ""),
                    conv.get("bot_response", ""),
                    conv.get("metadata", {}),
                )
                imported += 1

            # Import profile if available
            if "profile" in data and hasattr(self.memory, "update_profile"):
                self.memory.update_profile(target_user_id, data["profile"])

            logger.info(f"Imported {imported} conversations from {input_file}")

            return {
                "success": True,
                "file": str(input_path),
                "user_id": target_user_id,
                "conversations": imported,
            }

        except Exception as e:
            logger.error(f"JSON import failed: {e}")
            return {"success": False, "error": str(e)}

    def import_from_csv(self, input_file: str, user_id: str) -> Dict[str, Any]:
        """
        Import conversations from CSV file

        Args:
            input_file: Input CSV file path
            user_id: User ID for imported conversations

        Returns:
            Import statistics
        """
        try:
            input_path = Path(input_file)

            if not input_path.exists():
                return {"success": False, "error": f"File not found: {input_file}"}

            imported = 0

            with open(input_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    metadata = {}
                    if row.get("metadata"):
                        try:
                            metadata = json.loads(row["metadata"])
                        except (ValueError, json.JSONDecodeError):
                            pass

                    self.memory.add_conversation(
                        user_id, row.get("user_message", ""), row.get("bot_response", ""), metadata
                    )
                    imported += 1

            logger.info(f"Imported {imported} conversations from CSV: {input_file}")

            return {
                "success": True,
                "file": str(input_path),
                "user_id": user_id,
                "conversations": imported,
            }

        except Exception as e:
            logger.error(f"CSV import failed: {e}")
            return {"success": False, "error": str(e)}

    def import_from_sqlite(self, db_file: str, user_id: str) -> Dict[str, Any]:
        """
        Import from SQLite database

        Args:
            db_file: SQLite database file path
            user_id: User ID to import data for

        Returns:
            Import statistics
        """
        try:
            db_path = Path(db_file)

            if not db_path.exists():
                return {"success": False, "error": f"Database not found: {db_file}"}

            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Query conversations
            cursor.execute(
                """
                SELECT timestamp, user_message, bot_response, metadata
                FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp
            """,
                (user_id,),
            )

            imported = 0
            for row in cursor.fetchall():
                metadata = {}
                if row["metadata"]:
                    try:
                        metadata = json.loads(row["metadata"])
                    except (ValueError, json.JSONDecodeError):
                        pass

                self.memory.add_conversation(
                    user_id, row["user_message"], row["bot_response"], metadata
                )
                imported += 1

            conn.close()

            logger.info(f"Imported {imported} conversations from SQLite: {db_file}")

            return {
                "success": True,
                "file": str(db_path),
                "user_id": user_id,
                "conversations": imported,
            }

        except Exception as e:
            logger.error(f"SQLite import failed: {e}")
            return {"success": False, "error": str(e)}

    def import_from_postgresql(self, connection_string: str, user_id: str) -> Dict[str, Any]:
        """
        Import from PostgreSQL database

        Args:
            connection_string: PostgreSQL connection string
            user_id: User ID to import data for

        Returns:
            Import statistics
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError:
            return {
                "success": False,
                "error": "psycopg2 not installed. Install: pip install psycopg2-binary",
            }

        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Query conversations
            cursor.execute(
                """
                SELECT timestamp, user_message, bot_response, metadata
                FROM conversations
                WHERE user_id = %s
                ORDER BY timestamp
            """,
                (user_id,),
            )

            imported = 0
            for row in cursor.fetchall():
                metadata = row["metadata"] if isinstance(row["metadata"], dict) else {}

                self.memory.add_conversation(
                    user_id, row["user_message"], row["bot_response"], metadata
                )
                imported += 1

            cursor.close()
            conn.close()

            logger.info(f"Imported {imported} conversations from PostgreSQL")

            return {
                "success": True,
                "database": "postgresql",
                "user_id": user_id,
                "conversations": imported,
            }

        except Exception as e:
            logger.error(f"PostgreSQL import failed: {e}")
            return {"success": False, "error": str(e)}

    def import_from_mongodb(
        self,
        connection_string: str,
        user_id: str,
        database: str = "mem_llm",
        collection: str = "conversations",
    ) -> Dict[str, Any]:
        """
        Import from MongoDB database

        Args:
            connection_string: MongoDB connection string
            user_id: User ID to import data for
            database: Database name
            collection: Collection name

        Returns:
            Import statistics
        """
        try:
            from pymongo import MongoClient
        except ImportError:
            return {
                "success": False,
                "error": "pymongo not installed. Install: pip install pymongo",
            }

        try:
            client = MongoClient(connection_string)
            db = client[database]
            coll = db[collection]

            # Query conversations
            documents = coll.find({"user_id": user_id}).sort("timestamp", 1)

            imported = 0
            for doc in documents:
                self.memory.add_conversation(
                    user_id,
                    doc.get("user_message", ""),
                    doc.get("bot_response", ""),
                    doc.get("metadata", {}),
                )
                imported += 1

            client.close()

            logger.info(f"Imported {imported} conversations from MongoDB")

            return {
                "success": True,
                "database": "mongodb",
                "user_id": user_id,
                "conversations": imported,
            }

        except Exception as e:
            logger.error(f"MongoDB import failed: {e}")
            return {"success": False, "error": str(e)}
