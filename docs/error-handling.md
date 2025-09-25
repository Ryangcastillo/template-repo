# Error Handling Strategy

## Centralized Error Management

### Error Manager Class

```python
from enum import Enum
from typing import Dict, Any, Optional
import logging

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorManager:
    """Centralized error handling and logging system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def handle_error(
        self, 
        error: Exception, 
        severity: ErrorSeverity,
        context: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle errors with consistent logging and response."""
        
        error_id = self._generate_error_id()
        
        # Log error
        self._log_error(error, severity, error_id, context)
        
        # Return standardized response
        return {
            "error_id": error_id,
            "message": user_message or self._get_default_message(severity),
            "severity": severity.value,
            "timestamp": self._get_timestamp()
        }
```

## Error Categories

### 1. Validation Errors
- **Type**: User input validation failures
- **Response**: 400 Bad Request
- **Action**: Return detailed validation messages

### 2. Authentication Errors
- **Type**: Login, token, permission failures
- **Response**: 401 Unauthorized / 403 Forbidden
- **Action**: Log attempt, return generic message

### 3. Business Logic Errors
- **Type**: Domain rule violations
- **Response**: 422 Unprocessable Entity
- **Action**: Return business rule explanation

### 4. External Service Errors
- **Type**: API calls, database connections
- **Response**: 503 Service Unavailable
- **Action**: Implement retry logic

### 5. System Errors
- **Type**: Unexpected exceptions
- **Response**: 500 Internal Server Error
- **Action**: Log full trace, return generic message

## Error Response Format

```json
{
  "error": {
    "id": "error_20231225_abc123",
    "message": "The requested resource was not found",
    "code": "RESOURCE_NOT_FOUND",
    "severity": "medium",
    "timestamp": "2023-12-25T10:30:00Z",
    "details": {
      "field": "user_id",
      "value": "12345"
    }
  }
}
```

## Retry Mechanisms

### Database Operations

```python
import time
from functools import wraps

def retry_db_operation(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except DatabaseConnectionError as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator
```

### External API Calls

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_robust_session():
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session
```

## Logging Configuration

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'ERROR'
        }
    },
    'loggers': {
        'cms': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## Monitoring and Alerting

### Error Thresholds
- **Critical errors**: Immediate alert
- **High errors**: Alert within 5 minutes
- **Medium errors**: Daily summary
- **Low errors**: Weekly summary

### Health Checks

```python
from typing import Dict, List

class HealthChecker:
    def __init__(self):
        self.checks = []
    
    def add_check(self, name: str, check_func):
        self.checks.append((name, check_func))
    
    def run_checks(self) -> Dict[str, Any]:
        results = {"status": "healthy", "checks": []}
        
        for name, check_func in self.checks:
            try:
                result = check_func()
                results["checks"].append({
                    "name": name,
                    "status": "pass",
                    "response_time": result.get("response_time", 0)
                })
            except Exception as e:
                results["status"] = "unhealthy"
                results["checks"].append({
                    "name": name,
                    "status": "fail",
                    "error": str(e)
                })
        
        return results
```