import cohere
from typing import List, Optional
from ..config import settings
from ..utils.vector_store import vector_store

class EmbeddingService:
    def __init__(self):
        self.co = cohere.Client(settings.cohere_api_key)
        self.model = settings.cohere_embedding_model

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text using Cohere."""
        try:
            response = self.co.embed(
                texts=[text],
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error generating embedding with Cohere: {e}")
            return None

    def get_embeddings_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for multiple texts using Cohere."""
        try:
            response = self.co.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            print(f"Error generating batch embeddings with Cohere: {e}")
            return None

    def add_text_to_vector_store(self, content_id: str, text: str, metadata: Optional[dict] = None) -> bool:
        """Generate embedding for text and add it to the vector store."""
        embedding = self.get_embedding(text)
        if embedding is None:
            return False

        return vector_store.add_embedding(
            content_id=content_id,
            content_text=text,
            embedding=embedding,
            metadata=metadata
        )

    def search_similar_content(self, query: str, limit: int = 5) -> List[dict]:
        """Search for content similar to the query."""
        query_embedding = self.get_embedding(query)
        if query_embedding is None:
            return []

        return vector_store.search_similar(query_embedding, limit)

    def add_text_batch_to_vector_store(self, texts_data: List[dict]) -> bool:
        """Add multiple texts with their metadata to the vector store."""
        # Prepare embeddings
        texts = [data["text"] for data in texts_data]
        embeddings = self.get_embeddings_batch(texts)

        if embeddings is None:
            return False

        # Prepare data for vector store
        embeddings_data = []
        for i, data in enumerate(texts_data):
            embeddings_data.append({
                "content_id": data["content_id"],
                "content_text": data["text"],
                "embedding": embeddings[i],
                "metadata": data.get("metadata", {})
            })

        return vector_store.batch_add_embeddings(embeddings_data)

# Global instance
embedding_service = EmbeddingService()