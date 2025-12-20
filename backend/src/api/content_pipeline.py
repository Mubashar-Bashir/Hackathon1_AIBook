"""
Content Pipeline API Endpoints

This module provides API endpoints for triggering and managing the content pipeline.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Optional
from pydantic import BaseModel
import asyncio
import logging

from src.services.content_service import ContentService, ContentProcessingResult
from src.services.embedding_service import EmbeddingService
from src.utils.vector_store import vector_store
from src.models.content import BookContent
from src.utils.logging import log_content_pipeline_event, log_error, log_performance


class ContentPipelineRequest(BaseModel):
    """Request model for content pipeline"""
    base_url: str
    sitemap_url: Optional[str] = None
    urls: Optional[List[str]] = None


class ContentPipelineResponse(BaseModel):
    """Response model for content pipeline"""
    status: str
    message: str
    results: List[ContentProcessingResult]
    total_processed: int
    total_errors: int


class PipelineStatusResponse(BaseModel):
    """Response model for pipeline status"""
    status: str
    active_jobs: int
    last_run: Optional[str] = None
    next_scheduled: Optional[str] = None


router = APIRouter(prefix="/api/content", tags=["content-pipeline"])


# In-memory storage for pipeline jobs (in production, use a proper job queue)
pipeline_jobs = {}
active_jobs = set()


@router.post("/fetch", response_model=ContentPipelineResponse)
async def trigger_content_pipeline(request: ContentPipelineRequest):
    """Trigger the content fetching and processing pipeline"""
    start_time = asyncio.get_event_loop().time()

    try:
        log_content_pipeline_event(
            event_type="pipeline_start",
            url=request.base_url,
            **{
                "urls_count": len(request.urls) if request.urls else 0,
                "has_sitemap": request.sitemap_url is not None
            }
        )

        # Initialize services
        embedding_service = EmbeddingService()
        content_service = ContentService(embedding_service, vector_store)

        # Determine which URLs to process
        if request.urls and len(request.urls) > 0:
            # Process specific URLs - this will use the monitored version
            log_content_pipeline_event(
                event_type="processing_specific_urls",
                url=request.base_url,
                **{"urls_count": len(request.urls)}
            )
            results = await content_service.process_content_from_urls(
                request.base_url,
                request.urls
            )
        else:
            # Process content from sitemap - this will use the monitored version
            log_content_pipeline_event(
                event_type="processing_sitemap",
                url=request.base_url,
                **{"sitemap_url": request.sitemap_url}
            )
            # Use the update_content_pipeline method which has monitoring integration
            results = await content_service.update_content_pipeline(
                request.base_url,
                request.sitemap_url
            )

        # Count successful and failed results
        total_processed = sum(1 for r in results if r.status == 'success')
        total_errors = len(results) - total_processed

        execution_time = asyncio.get_event_loop().time() - start_time

        log_content_pipeline_event(
            event_type="pipeline_complete",
            url=request.base_url,
            status="completed",
            **{
                "total_processed": total_processed,
                "total_errors": total_errors,
                "execution_time": execution_time
            }
        )

        log_performance(
            metric="content_pipeline_execution_time",
            value=execution_time,
            unit="seconds",
            threshold=30.0  # Log warning if pipeline takes more than 30 seconds
        )

        return ContentPipelineResponse(
            status="completed",
            message=f"Content pipeline completed: {total_processed} processed, {total_errors} errors",
            results=results,
            total_processed=total_processed,
            total_errors=total_errors
        )
    except Exception as e:
        execution_time = asyncio.get_event_loop().time() - start_time
        log_error(e, "content_pipeline_api", request.base_url)
        log_content_pipeline_event(
            event_type="pipeline_error",
            url=request.base_url,
            status="error",
            error=str(e),
            **{"execution_time": execution_time}
        )
        raise HTTPException(status_code=500, detail=f"Error running content pipeline: {str(e)}")


@router.post("/fetch-async")
async def trigger_content_pipeline_async(background_tasks: BackgroundTasks, request: ContentPipelineRequest):
    """Trigger the content pipeline asynchronously"""
    try:
        # Generate a job ID
        import uuid
        job_id = str(uuid.uuid4())

        # Add to active jobs
        active_jobs.add(job_id)

        # Run the pipeline in the background
        background_tasks.add_task(
            _run_pipeline_background,
            job_id,
            request
        )

        return {
            "status": "started",
            "job_id": job_id,
            "message": "Content pipeline started in background"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting content pipeline: {str(e)}")


async def _run_pipeline_background(job_id: str, request: ContentPipelineRequest):
    """Background task to run the content pipeline"""
    try:
        # Initialize services
        embedding_service = EmbeddingService()
        content_service = ContentService(embedding_service, vector_store)

        # Determine which URLs to process
        if request.urls and len(request.urls) > 0:
            # Process specific URLs
            results = await content_service.process_content_from_urls(
                request.base_url,
                request.urls
            )
        else:
            # Process content from sitemap
            results = await content_service.process_content_from_sitemap(
                request.base_url,
                request.sitemap_url
            )

        # Store results
        pipeline_jobs[job_id] = {
            "results": results,
            "completed_at": asyncio.get_event_loop().time()
        }
    except Exception as e:
        pipeline_jobs[job_id] = {
            "error": str(e),
            "completed_at": asyncio.get_event_loop().time()
        }
    finally:
        # Remove from active jobs
        active_jobs.discard(job_id)


@router.get("/status/{job_id}")
async def get_pipeline_status(job_id: str):
    """Get the status of a content pipeline job"""
    if job_id in active_jobs:
        return {
            "status": "running",
            "job_id": job_id,
            "message": "Pipeline is currently running"
        }
    elif job_id in pipeline_jobs:
        job_result = pipeline_jobs[job_id]
        if "error" in job_result:
            return {
                "status": "failed",
                "job_id": job_id,
                "error": job_result["error"],
                "completed_at": job_result["completed_at"]
            }
        else:
            results = job_result["results"]
            total_processed = sum(1 for r in results if r.status == 'success')
            total_errors = len(results) - total_processed
            return {
                "status": "completed",
                "job_id": job_id,
                "results": results,
                "total_processed": total_processed,
                "total_errors": total_errors,
                "completed_at": job_result["completed_at"]
            }
    else:
        raise HTTPException(status_code=404, detail="Job ID not found")


@router.get("/status", response_model=PipelineStatusResponse)
async def get_pipeline_overview():
    """Get an overview of pipeline status"""
    return PipelineStatusResponse(
        status="active",
        active_jobs=len(active_jobs),
        last_run=None,  # Would need to track this in a real implementation
        next_scheduled=None  # Would need scheduling system for this
    )


@router.get("/fetch/health")
async def content_pipeline_health():
    """Health check for the content pipeline service"""
    return {
        "status": "healthy",
        "active_jobs": len(active_jobs),
        "pipeline_jobs_stored": len(pipeline_jobs)
    }


# Add a scheduled pipeline runner
class PipelineScheduler:
    """Simple scheduler for running pipeline on schedule"""

    def __init__(self, content_service: ContentService):
        self.content_service = content_service
        self.is_running = False

    async def start_scheduled_pipeline(self, base_url: str, interval_hours: int = 24):
        """Start a scheduled pipeline that runs at regular intervals"""
        if self.is_running:
            return

        self.is_running = True
        while self.is_running:
            try:
                await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds
                await self.content_service.update_content_pipeline(base_url)
            except Exception as e:
                print(f"Error in scheduled pipeline: {e}")

    def stop_scheduled_pipeline(self):
        """Stop the scheduled pipeline"""
        self.is_running = False


# Global scheduler instance (in production, use proper job scheduling like Celery)
scheduler = None


@router.post("/schedule")
async def schedule_pipeline(request: ContentPipelineRequest, interval_hours: int = 24):
    """Schedule the content pipeline to run at regular intervals"""
    global scheduler

    try:
        # Initialize services
        embedding_service = EmbeddingService()
        content_service = ContentService(embedding_service, vector_store)

        # Create and start scheduler
        scheduler = PipelineScheduler(content_service)

        # Run in background
        asyncio.create_task(
            scheduler.start_scheduled_pipeline(request.base_url, interval_hours)
        )

        return {
            "status": "scheduled",
            "message": f"Content pipeline scheduled to run every {interval_hours} hours",
            "base_url": request.base_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling content pipeline: {str(e)}")


@router.post("/unschedule")
async def unschedule_pipeline():
    """Stop the scheduled content pipeline"""
    global scheduler

    if scheduler:
        scheduler.stop_scheduled_pipeline()
        scheduler = None
        return {"status": "stopped", "message": "Scheduled content pipeline stopped"}
    else:
        raise HTTPException(status_code=404, detail="No scheduled pipeline found")