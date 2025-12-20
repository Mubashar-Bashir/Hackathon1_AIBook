"""
Content Service for RAG Pipeline

This module provides functionality to process fetched content, chunk it,
generate embeddings, and store in the vector database.
"""

import asyncio
import logging
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from src.models.content import BookContent, TextChunk
from src.models.rag_pipeline import ContentProcessingResult
from src.services.embedding_service import EmbeddingService
from src.utils.vector_store import vector_store
from src.utils.document_fetcher import DocumentFetcher, ContentFetchResult
from src.utils.logging import log_content_pipeline_event, log_error

import uuid


class ContentService:
    """Service to handle content processing pipeline"""

    def __init__(self, embedding_service: EmbeddingService, vector_store_service=None):
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service
        self.logger = logging.getLogger(__name__)

    async def process_content_from_sitemap(self, base_url: str, sitemap_url: Optional[str] = None) -> List[ContentProcessingResult]:
        """
        Process all content from sitemap: fetch, chunk, embed, and store
        """
        # Import rag_monitor locally to avoid circular import
        from src.api.rag_monitor import rag_monitor

        fetcher = DocumentFetcher(base_url)

        # Fetch content from sitemap
        content_results = fetcher.fetch_content_from_sitemap(sitemap_url)
        total_docs = len(content_results)

        # Generate a job ID for this pipeline run
        job_id = str(uuid.uuid4())

        # Start monitoring
        await rag_monitor.start_pipeline_monitoring(job_id, total_docs)

        results = []
        fetch_errors = 0
        for i, content_result in enumerate(content_results):
            if content_result.status == 'success':
                result = await self.process_single_content(content_result)
                results.append(result)
            else:
                fetch_errors += 1
                results.append(ContentProcessingResult(
                    content_id='',
                    url=content_result.url,
                    title=content_result.title,
                    chunks_processed=0,
                    status='error',
                    error=content_result.error
                ))

            # Update fetch progress
            await rag_monitor.update_fetch_progress(job_id, i + 1, fetch_errors, total_docs)

        return results

    async def process_content_from_urls(self, base_url: str, urls: List[str]) -> List[ContentProcessingResult]:
        """
        Process content from specific URLs: fetch, chunk, embed, and store
        """
        # Import rag_monitor locally to avoid circular import
        from src.api.rag_monitor import rag_monitor

        fetcher = DocumentFetcher(base_url)

        # Fetch content from URLs
        content_results = fetcher.fetch_content_from_urls(urls)
        total_docs = len(content_results)

        # Generate a job ID for this pipeline run
        job_id = str(uuid.uuid4())

        # Start monitoring
        await rag_monitor.start_pipeline_monitoring(job_id, total_docs)

        results = []
        fetch_errors = 0
        for i, content_result in enumerate(content_results):
            if content_result.status == 'success':
                result = await self.process_single_content(content_result)
                results.append(result)
            else:
                fetch_errors += 1
                results.append(ContentProcessingResult(
                    content_id='',
                    url=content_result.url,
                    title=content_result.title,
                    chunks_processed=0,
                    status='error',
                    error=content_result.error
                ))

            # Update fetch progress
            await rag_monitor.update_fetch_progress(job_id, i + 1, fetch_errors, total_docs)

        return results

    async def process_single_content(self, content_result: ContentFetchResult) -> ContentProcessingResult:
        """
        Process a single piece of content: chunk, embed, and store
        """
        # Import rag_monitor locally to avoid circular import
        from src.api.rag_monitor import rag_monitor

        try:
            # Log the start of content processing
            log_content_pipeline_event(
                event_type="content_processing_start",
                url=content_result.url,
                status="processing"
            )

            # Create BookContent entity
            book_content = BookContent(
                url=content_result.url,
                title=content_result.title,
                content=content_result.content,
                source_type='web_page',
                created_at=datetime.utcnow()
            )

            # Chunk the content
            chunks = self.chunk_content(book_content.content, book_content.id)

            # Generate embeddings and store
            stored_chunk_ids = []
            embedding_errors = 0

            # Update embedding progress
            await rag_monitor.update_embedding_progress(rag_monitor.pipeline_status["current_job_id"], 0, 0, len(chunks))

            for i, chunk in enumerate(chunks):
                try:
                    # Generate embedding
                    embedding = await self.embedding_service.generate_embedding(chunk.content)

                    # Store in vector database
                    success = vector_store.add_embedding(
                        content_id=book_content.id,
                        content_text=chunk.content,
                        embedding=embedding,
                        metadata={
                            'url': book_content.url,
                            'title': book_content.title,
                            'chunk_index': chunk.chunk_index
                        }
                    )
                    if success:
                        stored_chunk_ids.append(chunk.id)  # Using chunk.id instead of a separate chunk_id
                    else:
                        embedding_errors += 1
                except Exception as chunk_error:
                    self.logger.error(f"Error processing chunk {chunk.chunk_index} for {content_result.url}: {chunk_error}")
                    log_error(chunk_error, f"content_chunk_processing_{chunk.chunk_index}", content_result.url)
                    embedding_errors += 1

                # Update embedding progress
                await rag_monitor.update_embedding_progress(rag_monitor.pipeline_status["current_job_id"], i + 1, embedding_errors, len(chunks))

            # Update storing progress
            await rag_monitor.update_storing_progress(rag_monitor.pipeline_status["current_job_id"], len(stored_chunk_ids), embedding_errors, len(chunks))

            # Log successful completion
            log_content_pipeline_event(
                event_type="content_processing_complete",
                url=content_result.url,
                status="success",
                **{
                    "chunks_processed": len(chunks),
                    "stored_chunks": len(stored_chunk_ids)
                }
            )

            self.logger.info(f"Successfully processed content from {content_result.url} into {len(chunks)} chunks")

            return ContentProcessingResult(
                content_id=book_content.id,
                url=content_result.url,
                title=content_result.title,
                chunks_processed=len(chunks),
                status='success'
            )
        except Exception as e:
            self.logger.error(f"Error processing content from {content_result.url}: {e}")
            log_error(e, "content_processing", content_result.url)
            log_content_pipeline_event(
                event_type="content_processing_error",
                url=content_result.url,
                status="error",
                error=str(e)
            )
            return ContentProcessingResult(
                content_id='',
                url=content_result.url,
                title=content_result.title,
                chunks_processed=0,
                status='error',
                error=str(e)
            )

    def chunk_content(self, content: str, content_id: str, chunk_size: int = 512, overlap: float = 0.2) -> List[TextChunk]:
        """
        Chunk content into smaller pieces for RAG processing
        """
        if not content:
            return []

        # Calculate overlap size
        overlap_size = int(chunk_size * overlap)

        # Split content into tokens (simplified - in practice, use proper tokenization)
        sentences = self._split_into_sentences(content)

        chunks = []
        current_chunk = ""
        chunk_index = 0

        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                # Save current chunk
                chunk = TextChunk(
                    content_id=content_id,
                    chunk_index=chunk_index,
                    content=current_chunk.strip(),
                    token_count=len(current_chunk.split())
                )
                chunks.append(chunk)

                # Start new chunk with overlap
                if overlap_size > 0:
                    # Add overlapping content from the end of the previous chunk
                    overlap_start = max(0, len(current_chunk) - overlap_size)
                    current_chunk = current_chunk[overlap_start:] + " " + sentence
                else:
                    current_chunk = sentence
                chunk_index += 1
            else:
                current_chunk += " " + sentence

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk = TextChunk(
                content_id=content_id,
                chunk_index=chunk_index,
                content=current_chunk.strip(),
                token_count=len(current_chunk.split())
            )
            chunks.append(chunk)

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences (simplified approach)
        """
        import re

        # Split on sentence endings, preserving the punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Clean up the sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    async def update_content_pipeline(self, base_url: str, sitemap_url: Optional[str] = None) -> List[ContentProcessingResult]:
        """
        Run the complete content pipeline: fetch from sitemap, process, and store
        """
        # Import rag_monitor locally to avoid circular import
        from src.api.rag_monitor import rag_monitor

        self.logger.info(f"Starting content pipeline for {base_url}")

        results = await self.process_content_from_sitemap(base_url, sitemap_url)

        success_count = sum(1 for r in results if r.status == 'success')
        error_count = len(results) - success_count

        # Calculate total chunks and embeddings processed
        total_chunks = sum(r.chunks_processed for r in results)

        # Mark pipeline as complete in the monitor
        if rag_monitor.pipeline_status["current_job_id"]:
            await rag_monitor.mark_pipeline_complete(
                rag_monitor.pipeline_status["current_job_id"],
                len(results),  # total docs
                total_chunks,  # total chunks
                total_chunks   # total embeddings (assuming 1 embedding per chunk)
            )

        self.logger.info(f"Content pipeline completed: {success_count} successful, {error_count} errors")

        return results


# Example usage
async def run_content_pipeline():
    """
    Example function to run the content pipeline
    """
    from src.services.embedding_service import EmbeddingService

    # Initialize services
    embedding_service = EmbeddingService()
    content_service = ContentService(embedding_service, vector_store)  # Use global vector_store instance

    # Run pipeline
    results = await content_service.update_content_pipeline(
        "https://book-20sb9ub9v-mubashar-bashirs-projects.vercel.app"
    )

    for result in results:
        print(f"URL: {result.url}, Status: {result.status}, Chunks: {result.chunks_processed}")


if __name__ == "__main__":
    # Run the content pipeline
    asyncio.run(run_content_pipeline())