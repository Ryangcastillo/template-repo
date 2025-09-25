# Error Handling & Security

## Centralized Error Management

### Error Handler Architecture

```python
# src/utils/error_handler.py
from typing import Dict, Any, Optional
from enum import Enum
import logging
import traceback

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BaseError(Exception):
    """Base exception class for all application errors"""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM, 
                 details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.details = details or {}
        super().__init__(message)

class ValidationError(BaseError):
    """Raised when input validation fails"""
    pass

class BusinessLogicError(BaseError):
    """Raised when business rules are violated"""
    pass

class ExternalServiceError(BaseError):
    """Raised when external service calls fail"""
    pass

class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle and log errors consistently"""
        error_context = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        if isinstance(error, BaseError):
            error_context["severity"] = error.severity.value
            error_context["details"] = error.details
            
            if error.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
                self.logger.error(f"High severity error: {error.message}", extra=error_context)
            else:
                self.logger.warning(f"Application error: {error.message}", extra=error_context)
        else:
            self.logger.error(f"Unexpected error: {str(error)}", extra=error_context)
        
        return self._format_error_response(error, error_context)
    
    def _format_error_response(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format error for API responses"""
        if isinstance(error, BaseError):
            return {
                "error": True,
                "message": error.message,
                "type": type(error).__name__,
                "severity": error.severity.value
            }
        
        return {
            "error": True,
            "message": "An unexpected error occurred",
            "type": "InternalError"
        }
```

### Retry Logic with Exponential Backoff

```python
# src/utils/retry.py
import asyncio
import random
from typing import Callable, Any, TypeVar, Type
from functools import wraps

T = TypeVar('T')

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2,
    jitter: bool = True,
    exceptions: tuple = (Exception,)
):
    """Decorator for retrying functions with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        raise ExternalServiceError(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}",
                            ErrorSeverity.HIGH,
                            {"last_error": str(e), "attempts": attempt + 1}
                        )
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    if jitter:
                        delay *= (0.5 + random.random() * 0.5)
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            return asyncio.run(async_wrapper(*args, **kwargs))
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator
```

## Security Hardening

### Input Validation

```python
# src/utils/validators.py
from pydantic import BaseModel, validator
import re
from typing import Any, Optional

class SecureInput(BaseModel):
    """Base class for secure input validation"""
    
    @validator('*', pre=True)
    def sanitize_strings(cls, value: Any) -> Any:
        """Remove potential XSS and injection attacks"""
        if isinstance(value, str):
            # Remove potential script tags
            value = re.sub(r'<script.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
            # Remove SQL injection patterns
            value = re.sub(r'(\b(union|select|insert|delete|update|drop|create|alter)\b)', '', value, flags=re.IGNORECASE)
        return value
    
    @validator('*')
    def check_length(cls, value: Any) -> Any:
        """Prevent buffer overflow attacks"""
        if isinstance(value, str) and len(value) > 10000:
            raise ValidationError("Input too long", ErrorSeverity.MEDIUM)
        return value
```

### Rate Limiting

```python
# src/middleware/rate_limiter.py
import time
from collections import defaultdict, deque
from typing import Dict, DefaultDict

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: DefaultDict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limits"""
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests outside the window
        while client_requests and client_requests[0] < now - self.window_seconds:
            client_requests.popleft()
        
        # Check if under limit
        if len(client_requests) >= self.max_requests:
            return False
        
        # Add current request
        client_requests.append(now)
        return True
```

### Secure Configuration

```python
# src/config/security.py
from typing import List
import os

class SecurityConfig:
    """Security configuration settings"""
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # API Security
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "development-key-change-in-production")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    # Input validation
    MAX_INPUT_SIZE: int = int(os.getenv("MAX_INPUT_SIZE", "1048576"))  # 1MB
    ALLOWED_FILE_TYPES: List[str] = os.getenv("ALLOWED_FILE_TYPES", "txt,json,csv").split(",")
```

## Logging and Monitoring

```python
# src/utils/logging_config.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)
        
        return json.dumps(log_entry)

def setup_logging(level: str = "INFO") -> None:
    """Setup structured logging configuration"""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)
```

## Best Practices

1. **Never log sensitive data** (passwords, API keys, personal information)
2. **Use structured logging** for better observability
3. **Implement proper authentication** for all endpoints
4. **Validate all inputs** at the API boundary
5. **Use HTTPS in production** with proper TLS configuration
6. **Implement proper session management** with secure cookies
7. **Regular security audits** of dependencies and code
8. **Monitor for suspicious patterns** in logs and metrics