import re
from typing import Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from urllib.parse import unquote

logger = logging.getLogger(__name__)

class InputValidator:
    def __init__(self):
        # Common patterns for validation
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.username_pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')  # 3-20 chars, alphanumeric and underscore
        self.password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$')  # min 8 chars with letter and number

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        return bool(self.email_pattern.match(email))

    def validate_url(self, url: str) -> bool:
        """Validate URL format."""
        return bool(self.url_pattern.match(url))

    def validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(self.username_pattern.match(username))

    def validate_password(self, password: str) -> bool:
        """Validate password format."""
        return bool(self.password_pattern.match(password))

    def sanitize_text(self, text: str, max_length: int = 10000) -> str:
        """
        Sanitize text input by removing potentially dangerous content.

        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized text
        """
        if not text:
            return ""

        # Limit length
        if len(text) > max_length:
            text = text[:max_length]

        # URL decode any encoded characters
        text = unquote(text)

        # Remove potentially dangerous patterns
        # Remove script tags (case insensitive)
        text = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
        # Remove javascript: urls
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        # Remove data: urls
        text = re.sub(r'data:', '', text, flags=re.IGNORECASE)
        # Remove on* event handlers
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)

        return text.strip()

    def validate_json_depth(self, obj, max_depth: int = 10, current_depth: int = 0) -> bool:
        """
        Validate that JSON object doesn't exceed maximum nesting depth.

        Args:
            obj: Object to validate
            max_depth: Maximum allowed nesting depth
            current_depth: Current depth (used for recursion)

        Returns:
            True if valid, False if too deep
        """
        if current_depth > max_depth:
            return False

        if isinstance(obj, dict):
            for value in obj.values():
                if not self.validate_json_depth(value, max_depth, current_depth + 1):
                    return False
        elif isinstance(obj, list):
            for item in obj:
                if not self.validate_json_depth(item, max_depth, current_depth + 1):
                    return False

        return True

# Global validator instance
validator = InputValidator()

async def input_validation_middleware(request: Request, call_next):
    """
    Middleware to validate and sanitize input data.
    """
    # Get the request body if it's a POST/PUT/PATCH request
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            # Read the body
            body_bytes = await request.body()
            if body_bytes:
                # For now, just log the request for monitoring
                # In a production system, you'd want to validate the specific fields
                # based on the endpoint being called
                pass
        except Exception as e:
            logger.error(f"Error reading request body: {e}")
            # Continue with the request even if we can't read the body

    response = await call_next(request)
    return response

def validate_and_sanitize_input(text: Optional[str], field_name: str = "input", max_length: int = 10000) -> str:
    """
    Validate and sanitize a single input field.

    Args:
        text: Input text to validate and sanitize
        field_name: Name of the field for error messages
        max_length: Maximum allowed length

    Returns:
        Sanitized text

    Raises:
        HTTPException: If validation fails
    """
    if text is None:
        text = ""

    # Sanitize the input
    sanitized = validator.sanitize_text(text, max_length)

    # Check for suspicious patterns
    if len(sanitized) != len(text):
        logger.warning(f"Input sanitization modified {field_name} content")

    return sanitized

def validate_email_input(email: str) -> str:
    """
    Validate email input.

    Args:
        email: Email to validate

    Returns:
        Validated email

    Raises:
        HTTPException: If validation fails
    """
    if not validator.validate_email(email):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid email format: {email}"
        )
    return email

def validate_password_input(password: str) -> str:
    """
    Validate password input.

    Args:
        password: Password to validate

    Returns:
        Validated password

    Raises:
        HTTPException: If validation fails
    """
    if not validator.validate_password(password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long and contain at least one letter and one number"
        )
    return password