"""
Vector Store Abstraction Layer
Supports multiple vector databases (Chroma, FAISS, etc.)
"""

import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class VectorStore(ABC):
    """Abstract interface for vector stores"""

    @abstractmethod
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to vector store

        Args:
            documents: List of dicts with 'id', 'text', 'metadata'
        """
        pass

    @abstractmethod
    def search(
        self, query: str, limit: int = 5, filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Search similar documents

        Args:
            query: Search query text
            limit: Maximum number of results
            filter_metadata: Optional metadata filters

        Returns:
            List of similar documents with scores
        """
        pass

    @abstractmethod
    def delete_collection(self) -> None:
        """Delete all vectors in collection"""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        pass


try:
    import chromadb

    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    # Don't warn on import, only when actually trying to use it


class ChromaVectorStore(VectorStore):
    """ChromaDB implementation of VectorStore"""

    def __init__(
        self,
        collection_name: str = "knowledge_base",
        persist_directory: Optional[str] = None,
        embedding_model: str = "nomic-embed-text-v2-moe:latest",
    ):
        """
        Initialize ChromaDB vector store

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist data (None = in-memory)
            embedding_model: Embedding model name (sentence-transformers compatible)
        """
        if not CHROMA_AVAILABLE:
            raise ImportError("ChromaDB is not installed. Install with: pip install chromadb")

        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model

        # Initialize Chroma client
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        # Lazy load embedding model
        self._embedding_fn = None

        # Get or create collection with embedding function
        try:
            # Create embedding function
            embedding_fn = self._get_embedding_function()

            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=embedding_fn,
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as e:
            logger.error(f"Failed to create Chroma collection: {e}")
            raise

    def _get_embedding_function(self):
        """Lazy load embedding function"""
        if self._embedding_fn is None:
            try:
                # Try to use ChromaDB's native SentenceTransformerEmbeddingFunction
                try:
                    # Try different import paths for ChromaDB embedding functions
                    try:
                        from chromadb.utils import embedding_functions

                        embedding_fn_class = (
                            embedding_functions.SentenceTransformerEmbeddingFunction
                        )
                    except (ImportError, AttributeError):
                        try:
                            from chromadb.utils.embedding_functions import (
                                SentenceTransformerEmbeddingFunction as embedding_fn_class,
                            )
                        except ImportError:
                            embedding_fn_class = None

                    if embedding_fn_class:
                        self._embedding_fn = embedding_fn_class(model_name=self.embedding_model)
                        self.logger.info(
                            "Loaded embedding model using ChromaDB native function: "
                            f"{self.embedding_model}"
                        )
                    else:
                        raise AttributeError("SentenceTransformerEmbeddingFunction not found")

                except Exception:
                    # Fallback: Custom embedding function wrapper compatible with ChromaDB
                    from sentence_transformers import SentenceTransformer

                    model = SentenceTransformer(self.embedding_model)

                    class CustomEmbeddingFunction:
                        def __init__(self, model, model_name):
                            self.model = model
                            self.model_name = model_name
                            self.name = model_name  # ChromaDB may check for 'name' attribute

                        def __call__(self, texts: List[str]) -> List[List[float]]:
                            embeddings = self.model.encode(texts, show_progress_bar=False)
                            return embeddings.tolist()

                        def encode_queries(self, queries: List[str]) -> List[List[float]]:
                            return self.__call__(queries)

                    self._embedding_fn = CustomEmbeddingFunction(model, self.embedding_model)
                    logger.info(
                        f"Loaded embedding model using custom wrapper: {self.embedding_model}"
                    )
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )

        return self._embedding_fn

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to ChromaDB"""
        if not documents:
            return

        # Prepare data
        ids = []
        texts = []
        metadatas = []

        for doc in documents:
            # Use UUID for unique document IDs, fallback to provided id or generate new
            doc_id = str(doc.get("id", str(uuid.uuid4())))
            # Ensure unique IDs
            if doc_id in ids:
                doc_id = f"{doc_id}_{len(ids)}"
            ids.append(doc_id)
            texts.append(doc["text"])
            # Ensure metadata values are JSON-serializable
            metadata = doc.get("metadata", {})
            clean_metadata = {}
            for k, v in metadata.items():
                if isinstance(v, (str, int, float, bool)) or v is None:
                    clean_metadata[k] = v
                else:
                    clean_metadata[k] = str(v)
            metadatas.append(clean_metadata)

        # Add to collection (Chroma will use embedding function automatically)
        try:
            self.collection.add(ids=ids, documents=texts, metadatas=metadatas)

            logger.debug(f"Added {len(documents)} documents to Chroma")
        except Exception as e:
            logger.error(f"Error adding documents to Chroma: {e}")
            raise

    def search(
        self, query: str, limit: int = 5, filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search in ChromaDB"""
        try:
            # Build where clause for metadata filtering
            where = None
            if filter_metadata:
                where = filter_metadata

            # Search (Chroma will use embedding function automatically)
            results = self.collection.query(query_texts=[query], n_results=limit, where=where)

            # Format results
            formatted_results = []
            if (
                results.get("documents")
                and len(results["documents"]) > 0
                and len(results["documents"][0]) > 0
            ):
                num_results = len(results["documents"][0])
                distances = results.get("distances", [[0.0] * num_results])

                for i in range(num_results):
                    # ChromaDB uses cosine distance (0 = identical, 1 = opposite)
                    # Convert to similarity score (1 = identical, 0 = opposite)
                    distance = distances[0][i] if distances and len(distances[0]) > i else 0.0
                    similarity = (
                        1.0 - distance if distance <= 1.0 else max(0.0, 1.0 / (1.0 + distance))
                    )

                    formatted_results.append(
                        {
                            "id": (
                                results["ids"][0][i]
                                if results.get("ids") and len(results["ids"][0]) > i
                                else f"doc_{i}"
                            ),
                            "text": results["documents"][0][i],
                            "metadata": (
                                results["metadatas"][0][i]
                                if results.get("metadatas") and len(results["metadatas"][0]) > i
                                else {}
                            ),
                            "score": similarity,
                        }
                    )

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching Chroma: {e}")
            return []

    def delete_collection(self) -> None:
        """Delete collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted Chroma collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model,
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_documents": 0}


def create_vector_store(store_type: str = "chroma", **kwargs) -> Optional[VectorStore]:
    """
    Factory function to create vector store

    Args:
        store_type: Type of vector store ('chroma', 'faiss', etc.)
        **kwargs: Store-specific parameters

    Returns:
        VectorStore instance or None if not available
    """
    if store_type == "chroma":
        if not CHROMA_AVAILABLE:
            logger.info(
                "ℹ️  Vector search disabled (ChromaDB not installed). "
                "For semantic search, run: pip install chromadb sentence-transformers"
            )
            return None
        return ChromaVectorStore(**kwargs)
    else:
        logger.warning(f"Unknown vector store type: {store_type}")
        return None
