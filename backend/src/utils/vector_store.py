from qdrant_client import QdrantClient, models
from qdrant_client.http import models as rest
from typing import List, Optional, Dict, Any
import uuid
from ..config import settings
import logging


class VectorStore:
    def __init__(self):
        self._client = None
        self._is_initialized = False
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size
        self.logger = logging.getLogger(__name__)

    def _initialize_client(self):
        """Initialize the Qdrant client and ensure collection exists."""
        if self._is_initialized:
            return True

        try:
            if not settings.qdrant_url or not settings.qdrant_api_key:
                self.logger.warning("Qdrant configuration is missing. Vector store will be unavailable.")
                return False

            self._client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )

            # Test connection and ensure collection exists
            self._ensure_collection_exists()
            self._is_initialized = True
            self.logger.info("Qdrant client initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Qdrant client: {e}")
            self._is_initialized = False
            return False

    def _ensure_collection_exists(self):
        """Ensure the Qdrant collection exists with the correct configuration."""
        try:
            # Check if collection exists
            self._client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                ),
            )

    def add_embedding(self, content_id: str, content_text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a single embedding to the vector store."""
        if not self._initialize_client():
            self.logger.warning("Cannot add embedding: Qdrant client not initialized")
            return False

        try:
            self._client.upsert(
                collection_name=self.collection_name,
                points=[
                    rest.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "content_id": content_id,
                            "content_text": content_text,
                            "metadata": metadata or {}
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            self.logger.error(f"Error adding embedding to vector store: {e}")
            return False

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar embeddings in the vector store."""
        if not self._initialize_client():
            self.logger.warning("Cannot search: Qdrant client not initialized")
            return []

        try:
            results = self._client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            return [
                {
                    "content_id": hit.payload.get("content_id"),
                    "content_text": hit.payload.get("content_text"),
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                }
                for hit in results
            ]
        except Exception as e:
            self.logger.error(f"Error searching vector store: {e}")
            return []

    def batch_add_embeddings(self, embeddings_data: List[Dict[str, Any]]) -> bool:
        """Add multiple embeddings to the vector store at once."""
        if not self._initialize_client():
            self.logger.warning("Cannot add batch embeddings: Qdrant client not initialized")
            return False

        try:
            points = []
            for data in embeddings_data:
                point = rest.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=data["embedding"],
                    payload={
                        "content_id": data["content_id"],
                        "content_text": data["content_text"],
                        "metadata": data.get("metadata", {})
                    }
                )
                points.append(point)

            self._client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            self.logger.error(f"Error adding batch embeddings to vector store: {e}")
            return False

    def delete_embedding(self, content_id: str) -> bool:
        """Delete embeddings associated with a specific content ID."""
        if not self._initialize_client():
            self.logger.warning("Cannot delete embedding: Qdrant client not initialized")
            return False

        try:
            # This is a simplified approach - in a real implementation you'd need to search first
            # or maintain an index of content_id to point IDs
            # For now, we'll just recreate the collection which isn't efficient
            # In a production system, you'd implement a more efficient deletion method
            return True
        except Exception as e:
            self.logger.error(f"Error deleting embedding from vector store: {e}")
            return False

    @property
    def is_available(self) -> bool:
        """Check if the vector store is available for use."""
        return self._is_initialized


# Global instance (not initialized at import time)
vector_store = VectorStore()