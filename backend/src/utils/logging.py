import logging
import sys
from datetime import datetime
from typing import Optional
import os

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Set up logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers = []

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    # Suppress overly verbose logs from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("qdrant_client").setLevel(logging.WARNING)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance.

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def log_api_call(endpoint: str, method: str, user_id: Optional[str] = None,
                 status_code: int = 200, execution_time: float = 0.0):
    """
    Log API call information.

    Args:
        endpoint: API endpoint that was called
        method: HTTP method used
        user_id: ID of the user making the call (if authenticated)
        status_code: HTTP status code returned
        execution_time: Time taken to execute the call in seconds
    """
    logger = get_logger("api")
    user_info = f"User: {user_id}" if user_id else "User: anonymous"
    logger.info(f"API Call: {method} {endpoint} - {user_info} - Status: {status_code} - Time: {execution_time:.3f}s")

def log_error(error: Exception, context: str = "", user_id: Optional[str] = None):
    """
    Log error with context.

    Args:
        error: Exception that occurred
        context: Context where the error occurred
        user_id: ID of the user involved (if applicable)
    """
    logger = get_logger("error")
    user_info = f" User: {user_id}" if user_id else ""
    logger.error(f"Error in {context}{user_info}: {str(error)} - Type: {type(error).__name__}")

def log_performance(metric: str, value: float, unit: str = "",
                   threshold: Optional[float] = None):
    """
    Log performance metrics.

    Args:
        metric: Name of the metric being logged
        value: Value of the metric
        unit: Unit of measurement
        threshold: Optional threshold value for comparison
    """
    logger = get_logger("performance")
    unit_str = f" {unit}" if unit else ""
    message = f"Performance - {metric}: {value}{unit_str}"

    if threshold is not None and value > threshold:
        logger.warning(f"{message} (Above threshold: {threshold}{unit_str})")
    else:
        logger.info(message)


def log_content_pipeline_event(
    event_type: str,
    url: Optional[str] = None,
    status: Optional[str] = None,
    error: Optional[str] = None,
    user_id: Optional[str] = None,
    **kwargs
) -> None:
    """
    Log content pipeline events with structured format.

    Args:
        event_type: Type of event (fetch_start, fetch_complete, process_start, etc.)
        url: URL being processed (if applicable)
        status: Status of the operation (if applicable)
        error: Error message (if applicable)
        user_id: User ID (if applicable)
        **kwargs: Additional context fields
    """
    logger = get_logger("content_pipeline")
    extra = {
        "event_type": event_type,
        "component": "content_pipeline"
    }

    if url:
        extra["url"] = url
    if status:
        extra["status"] = status
    if error:
        extra["error"] = error
    if user_id:
        extra["user_id"] = user_id

    # Add any additional context
    extra.update(kwargs)

    # Create a structured log message
    message_parts = [f"Content pipeline event: {event_type}"]
    if url:
        message_parts.append(f"URL: {url}")
    if status:
        message_parts.append(f"Status: {status}")
    if error:
        message_parts.append(f"Error: {error}")

    message = " | ".join(message_parts)
    logger.info(message, extra=extra)


def log_rag_query_event(
    query: str,
    response: str,
    sources: list,
    confidence: float,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    **kwargs
) -> None:
    """
    Log RAG query events with structured format.

    Args:
        query: The original query
        response: The response generated
        sources: Sources used for the response
        confidence: Confidence score of the response
        user_id: User ID (if authenticated)
        session_id: Session ID
        **kwargs: Additional context fields
    """
    logger = get_logger("rag_service")
    extra = {
        "event_type": "rag_query",
        "component": "rag_service",
        "query_length": len(query),
        "response_length": len(response),
        "source_count": len(sources),
        "confidence_score": confidence
    }

    if user_id:
        extra["user_id"] = user_id
    if session_id:
        extra["session_id"] = session_id

    # Add any additional context
    extra.update(kwargs)

    # Create a structured log message
    message = f"RAG query processed | Query length: {len(query)} | Sources: {len(sources)} | Confidence: {confidence:.2f}"
    logger.info(message, extra=extra)


def log_function_calling_event(
    function_name: str,
    args: dict,
    result: Optional[dict] = None,
    error: Optional[str] = None,
    user_id: Optional[str] = None,
    **kwargs
) -> None:
    """
    Log OpenAI Function Calling events with structured format.

    Args:
        function_name: Name of the function being called
        args: Arguments passed to the function
        result: Result of the function call (if successful)
        error: Error message (if function failed)
        user_id: User ID (if applicable)
        **kwargs: Additional context fields
    """
    logger = get_logger("openai_function_calling")
    extra = {
        "event_type": "function_call",
        "component": "openai_function_calling",
        "function_name": function_name
    }

    if result:
        extra["result"] = result
    if error:
        extra["error"] = error
    if user_id:
        extra["user_id"] = user_id

    # Add any additional context
    extra.update(kwargs)

    # Create a structured log message
    message_parts = [f"Function calling event: {function_name}"]
    if result:
        message_parts.append(f"Result: {len(str(result))} chars")
    if error:
        message_parts.append(f"Error: {error}")

    message = " | ".join(message_parts)
    logger.info(message, extra=extra)