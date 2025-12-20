"""
RAG Process Monitoring API

This module provides real-time monitoring for the RAG content pipeline
with WebSocket support for live progress updates.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import asyncio
import json
import logging
from datetime import datetime
from pydantic import BaseModel

from src.models.rag_pipeline import ContentProcessingResult
from src.utils.vector_store import vector_store

router = APIRouter(prefix="/api/monitor", tags=["rag-monitor"])

# Global state for monitoring
pipeline_status = {
    "current_job_id": None,
    "status": "idle",  # idle, fetching, embedding, storing, completed, error
    "progress": 0,
    "total_steps": 3,  # fetch, embed, store
    "current_step": 0,
    "step_details": {
        "fetching": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
        "embedding": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
        "storing": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0}
    },
    "metadata": {
        "total_documents": 0,
        "total_chunks": 0,
        "total_embeddings": 0,
        "start_time": None,
        "end_time": None
    },
    "active_connections": []
}

class RAGProgressUpdate(BaseModel):
    job_id: str
    status: str
    step: str
    progress: int
    total: int
    completed: int
    errors: int
    message: str
    metadata: dict

class RAGMonitor:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.pipeline_status = {
            "current_job_id": None,
            "status": "idle",  # idle, fetching, embedding, storing, completed, error
            "progress": 0,
            "total_steps": 3,  # fetch, embed, store
            "current_step": 0,
            "step_details": {
                "fetching": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
                "embedding": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
                "storing": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0}
            },
            "metadata": {
                "total_documents": 0,
                "total_chunks": 0,
                "total_embeddings": 0,
                "start_time": None,
                "end_time": None
            },
            "active_connections": []
        }

    async def broadcast_update(self, update_data: dict):
        """Broadcast progress update to all connected clients"""
        if not self.connections:
            return

        for connection in self.connections:
            try:
                await connection.send_text(json.dumps(update_data))
            except:
                # Remove disconnected clients
                if connection in self.connections:
                    self.connections.remove(connection)

    async def start_pipeline_monitoring(self, job_id: str, total_docs: int):
        """Start monitoring a pipeline job"""
        # Reset the pipeline status for the new job
        await self.reset_pipeline_status()

        self.pipeline_status["current_job_id"] = job_id
        self.pipeline_status["status"] = "fetching"
        self.pipeline_status["progress"] = 0
        self.pipeline_status["current_step"] = 1
        self.pipeline_status["step_details"]["fetching"]["total"] = total_docs
        self.pipeline_status["step_details"]["fetching"]["status"] = "in_progress"
        self.pipeline_status["metadata"]["start_time"] = datetime.now().isoformat()

        update = {
            "job_id": job_id,
            "status": "fetching",
            "step": "fetching",
            "progress": 0,
            "total": total_docs,
            "completed": 0,
            "errors": 0,
            "message": f"Starting to fetch {total_docs} documents...",
            "metadata": self.pipeline_status["metadata"]
        }
        await self.broadcast_update(update)

    async def update_fetch_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update fetching progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["fetching"]["completed"] = completed
            self.pipeline_status["step_details"]["fetching"]["errors"] = errors
            self.pipeline_status["step_details"]["fetching"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["fetching"]["status"] = "completed"
                self.pipeline_status["status"] = "embedding"
                self.pipeline_status["current_step"] = 2

                # Set up embedding step
                self.pipeline_status["step_details"]["embedding"]["total"] = completed
                self.pipeline_status["step_details"]["embedding"]["status"] = "in_progress"

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "fetching",
                "progress": self.pipeline_status["step_details"]["fetching"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Fetched {completed}/{total} documents ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def update_embedding_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update embedding progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["embedding"]["completed"] = completed
            self.pipeline_status["step_details"]["embedding"]["errors"] = errors
            self.pipeline_status["step_details"]["embedding"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["embedding"]["status"] = "completed"
                self.pipeline_status["status"] = "storing"
                self.pipeline_status["current_step"] = 3

                # Set up storing step
                self.pipeline_status["step_details"]["storing"]["total"] = completed
                self.pipeline_status["step_details"]["storing"]["status"] = "in_progress"

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "embedding",
                "progress": self.pipeline_status["step_details"]["embedding"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Processed embeddings for {completed}/{total} chunks ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def update_storing_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update storing progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["storing"]["completed"] = completed
            self.pipeline_status["step_details"]["storing"]["errors"] = errors
            self.pipeline_status["step_details"]["storing"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["storing"]["status"] = "completed"
                self.pipeline_status["status"] = "completed"
                self.pipeline_status["metadata"]["end_time"] = datetime.now().isoformat()

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "storing",
                "progress": self.pipeline_status["step_details"]["storing"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Stored {completed}/{total} embeddings in vector database ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def mark_pipeline_complete(self, job_id: str, total_docs: int, total_chunks: int, total_embeddings: int):
        """Mark pipeline as complete"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["status"] = "completed"
            self.pipeline_status["progress"] = 100
            self.pipeline_status["metadata"]["total_documents"] = total_docs
            self.pipeline_status["metadata"]["total_chunks"] = total_chunks
            self.pipeline_status["metadata"]["total_embeddings"] = total_embeddings
            self.pipeline_status["metadata"]["end_time"] = datetime.now().isoformat()

            update = {
                "job_id": job_id,
                "status": "completed",
                "step": "completed",
                "progress": 100,
                "total": total_embeddings,
                "completed": total_embeddings,
                "errors": 0,
                "message": f"Pipeline completed! {total_docs} docs, {total_chunks} chunks, {total_embeddings} embeddings stored.",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def reset_pipeline_status(self):
        """Reset pipeline status for a new job"""
        self.pipeline_status = {
            "current_job_id": None,
            "status": "idle",
            "progress": 0,
            "total_steps": 3,
            "current_step": 0,
            "step_details": {
                "fetching": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
                "embedding": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0},
                "storing": {"status": "pending", "progress": 0, "total": 0, "completed": 0, "errors": 0}
            },
            "metadata": {
                "total_documents": 0,
                "total_chunks": 0,
                "total_embeddings": 0,
                "start_time": None,
                "end_time": None
            },
            "active_connections": []
        }

    async def update_fetch_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update fetching progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["fetching"]["completed"] = completed
            self.pipeline_status["step_details"]["fetching"]["errors"] = errors
            self.pipeline_status["step_details"]["fetching"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["fetching"]["status"] = "completed"
                self.pipeline_status["status"] = "embedding"
                self.pipeline_status["current_step"] = 2

                # Set up embedding step
                self.pipeline_status["step_details"]["embedding"]["total"] = completed
                self.pipeline_status["step_details"]["embedding"]["status"] = "in_progress"

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "fetching",
                "progress": self.pipeline_status["step_details"]["fetching"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Fetched {completed}/{total} documents ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def update_embedding_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update embedding progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["embedding"]["completed"] = completed
            self.pipeline_status["step_details"]["embedding"]["errors"] = errors
            self.pipeline_status["step_details"]["embedding"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["embedding"]["status"] = "completed"
                self.pipeline_status["status"] = "storing"
                self.pipeline_status["current_step"] = 3

                # Set up storing step
                self.pipeline_status["step_details"]["storing"]["total"] = completed
                self.pipeline_status["step_details"]["storing"]["status"] = "in_progress"

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "embedding",
                "progress": self.pipeline_status["step_details"]["embedding"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Processed embeddings for {completed}/{total} chunks ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

    async def update_storing_progress(self, job_id: str, completed: int, errors: int, total: int):
        """Update storing progress"""
        if self.pipeline_status["current_job_id"] == job_id:
            self.pipeline_status["step_details"]["storing"]["completed"] = completed
            self.pipeline_status["step_details"]["storing"]["errors"] = errors
            self.pipeline_status["step_details"]["storing"]["progress"] = min(100, int((completed / total) * 100)) if total > 0 else 0

            if completed >= total:
                self.pipeline_status["step_details"]["storing"]["status"] = "completed"
                self.pipeline_status["status"] = "completed"
                self.pipeline_status["metadata"]["end_time"] = datetime.now().isoformat()

            update = {
                "job_id": job_id,
                "status": self.pipeline_status["status"],
                "step": "storing",
                "progress": self.pipeline_status["step_details"]["storing"]["progress"],
                "total": total,
                "completed": completed,
                "errors": errors,
                "message": f"Stored {completed}/{total} embeddings in vector database ({errors} errors)",
                "metadata": self.pipeline_status["metadata"]
            }
            await self.broadcast_update(update)

# Global monitor instance
rag_monitor = RAGMonitor()

@router.websocket("/rag-progress")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time RAG progress monitoring"""
    await websocket.accept()
    rag_monitor.connections.append(websocket)

    try:
        # Send current status when client connects
        if rag_monitor.pipeline_status["current_job_id"]:
            current_status = {
                "job_id": rag_monitor.pipeline_status["current_job_id"],
                "status": rag_monitor.pipeline_status["status"],
                "step": "fetching",  # or current active step
                "progress": rag_monitor.pipeline_status["step_details"]["fetching"]["progress"],
                "total": rag_monitor.pipeline_status["step_details"]["fetching"]["total"],
                "completed": rag_monitor.pipeline_status["step_details"]["fetching"]["completed"],
                "errors": rag_monitor.pipeline_status["step_details"]["fetching"]["errors"],
                "message": f"Monitoring active pipeline...",
                "metadata": rag_monitor.pipeline_status["metadata"]
            }
            await websocket.send_text(json.dumps(current_status))

        while True:
            # Keep the connection alive
            data = await websocket.receive_text()
            # Process any commands if needed
    except WebSocketDisconnect:
        rag_monitor.connections.remove(websocket)

@router.get("/rag-status")
async def get_rag_status():
    """Get current RAG pipeline status"""
    return rag_monitor.pipeline_status

@router.get("/vector-stats")
async def get_vector_stats():
    """Get current vector store statistics"""
    try:
        collection_name = vector_store.collection_name
        collection_info = vector_store.client.get_collection(collection_name)
        return {
            "collection_name": collection_name,
            "total_vectors": collection_info.points_count,
            "status": "healthy"
        }
    except Exception as e:
        return {
            "collection_name": "unknown",
            "total_vectors": 0,
            "status": "error",
            "error": str(e)
        }