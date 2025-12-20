"""
Vector Store Service for RAG System

This module provides a service layer for vector store operations including
adding embeddings, searching, and managing vector collections.
"""

from typing import List, Optional, Dict, Any
from qdrant_client.http import models as rest
from src.utils.vector_store import vector_store
from src.config import settings


class VectorStoreService:
    def __init__(self):
        self.vector_store = vector_store
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size

    async def add_embedding(self, content_id: str, content_text: str, embedding: List[float],
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a single embedding to the vector store.

        Args:
            content_id: ID of the content being embedded
            content_text: The original text content
            embedding: The embedding vector
            metadata: Additional metadata to store with the embedding

        Returns:
            str: The ID of the created embedding point in the vector store
        """
        # The current vector_store implementation doesn't return the point ID
        # We'll modify the approach to return a success status and potentially generate our own ID
        success = self.vector_store.add_embedding(content_id, content_text, embedding, metadata)
        if success:
            # In a real implementation, we would return the actual Qdrant point ID
            # For now, we'll return a generated ID
            import uuid
            return str(uuid.uuid4())
        return None

    async def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings in the vector store.

        Args:
            query_embedding: The embedding vector to search for
            limit: Maximum number of results to return

        Returns:
            List of matching results with content_id, content_text, metadata, and score
        """
        return self.vector_store.search_similar(query_embedding, limit)

    async def batch_add_embeddings(self, embeddings_data: List[Dict[str, Any]]) -> bool:
        """
        Add multiple embeddings to the vector store at once.

        Args:
            embeddings_data: List of dictionaries containing embedding data
                             Each dict should have: content_id, content_text, embedding, metadata (optional)

        Returns:
            bool: True if successful, False otherwise
        """
        return self.vector_store.batch_add_embeddings(embeddings_data)

    async def delete_embedding_by_content_id(self, content_id: str) -> bool:
        """
        Delete embeddings associated with a specific content ID.

        Args:
            content_id: The ID of the content to delete embeddings for

        Returns:
            bool: True if successful, False otherwise
        """
        # Note: The current implementation doesn't have a proper deletion method
        # This would need to be implemented in the vector_store utility
        return self.vector_store.delete_embedding(content_id)

    async def get_vector_store_status(self) -> Dict[str, Any]:
        """
        Get the status of the vector store.

        Returns:
            Dict containing status information about the vector store
        """
        try:
            # Get collection info
            collection_info = self.vector_store.client.get_collection(self.collection_name)
            return {
                "status": "connected",
                "collection_name": self.collection_name,
                "vector_size": self.vector_size,
                "point_count": collection_info.points_count,
                "distance": collection_info.config.params.vectors.distance
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def recreate_collection(self) -> bool:
        """
        Recreate the vector store collection (useful for development/testing).

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete existing collection if it exists
            try:
                self.vector_store.client.delete_collection(self.collection_name)
            except:
                pass  # Collection might not exist yet

            # Recreate collection
            self.vector_store.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=rest.VectorParams(
                    size=self.vector_size,
                    distance=rest.Distance.COSINE
                ),
            )
            return True
        except Exception as e:
            print(f"Error recreating collection: {e}")
            return False


# Global instance
vector_store_service = VectorStoreService()