from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorDetails:
    def __init__(self, error: str, code: str, status_code: int, details: str = None):
        self.error = error
        self.code = code
        self.status_code = status_code
        self.details = details

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions globally."""
    error_details = ErrorDetails(
        error="HTTP Exception",
        code=f"HTTP_{exc.status_code}",
        status_code=exc.status_code,
        details=str(exc.detail) if hasattr(exc, 'detail') else "HTTP exception occurred"
    )

    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail if hasattr(exc, 'detail') else 'Unknown error'}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_details.error,
            "code": error_details.code,
            "message": error_details.details,
            "path": str(request.url),
            "timestamp": _get_current_timestamp()
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors globally."""
    error_details = ErrorDetails(
        error="Validation Error",
        code="VALIDATION_ERROR",
        status_code=422,
        details="Request validation failed"
    )

    logger.error(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": error_details.error,
            "code": error_details.code,
            "message": error_details.details,
            "validation_errors": exc.errors(),
            "path": str(request.url),
            "timestamp": _get_current_timestamp()
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions globally."""
    error_details = ErrorDetails(
        error="Internal Server Error",
        code="INTERNAL_ERROR",
        status_code=500,
        details="An unexpected error occurred"
    )

    # Log the full traceback for debugging
    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=500,
        content={
            "error": error_details.error,
            "code": error_details.code,
            "message": error_details.details,
            "path": str(request.url),
            "timestamp": _get_current_timestamp()
        }
    )

def _get_current_timestamp():
    """Get current timestamp in ISO format."""
    from datetime import datetime
    return datetime.utcnow().isoformat()

def add_exception_handlers(app):
    """Add exception handlers to the FastAPI application."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)