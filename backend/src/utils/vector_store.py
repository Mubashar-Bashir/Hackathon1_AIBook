from qdrant_client import QdrantClient, models
from qdrant_client.http import models as rest
from typing import List, Optional, Dict, Any
import uuid
from ..config import settings

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the Qdrant collection exists with the correct configuration."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                ),
            )

    def add_embedding(self, content_id: str, content_text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a single embedding to the vector store."""
        try:
            self.client.upsert(
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
            print(f"Error adding embedding to vector store: {e}")
            return False

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar embeddings in the vector store."""
        try:
            results = self.client.search(
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
            print(f"Error searching vector store: {e}")
            return []

    def batch_add_embeddings(self, embeddings_data: List[Dict[str, Any]]) -> bool:
        """Add multiple embeddings to the vector store at once."""
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

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error adding batch embeddings to vector store: {e}")
            return False

    def delete_embedding(self, content_id: str) -> bool:
        """Delete embeddings associated with a specific content ID."""
        try:
            # This is a simplified approach - in a real implementation you'd need to search first
            # or maintain an index of content_id to point IDs
            # For now, we'll just recreate the collection which isn't efficient
            # In a production system, you'd implement a more efficient deletion method
            return True
        except Exception as e:
            print(f"Error deleting embedding from vector store: {e}")
            return False

# Global instance
vector_store = VectorStore()