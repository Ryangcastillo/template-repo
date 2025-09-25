"""
Error Manager for centralized error handling.

This module implements the centralized error management system
as specified in the architectural requirements.
"""

import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

from cms.exceptions import CMSException


class ErrorSeverity(Enum):
    """Error severity levels."""
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
        """Handle errors with consistent logging and response.
        
        Args:
            error: The exception that occurred
            severity: Severity level of the error
            context: Additional context information
            user_message: User-friendly error message
            
        Returns:
            Standardized error response dictionary
        """
        error_id = self._generate_error_id()
        
        # Log error with appropriate level
        self._log_error(error, severity, error_id, context)
        
        # Return standardized response
        return {
            "error_id": error_id,
            "message": user_message or self._get_default_message(severity),
            "severity": severity.value,
            "timestamp": self._get_timestamp(),
            "type": error.__class__.__name__
        }
    
    def _generate_error_id(self) -> str:
        """Generate unique error ID for tracking."""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8]
        return f"error_{timestamp}_{unique_id}"
    
    def _log_error(
        self, 
        error: Exception, 
        severity: ErrorSeverity,
        error_id: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log error with appropriate level and details."""
        log_data = {
            "error_id": error_id,
            "error_type": error.__class__.__name__,
            "error_message": str(error),
            "severity": severity.value,
            "context": context or {}
        }
        
        if severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            self.logger.error(
                f"Error {error_id}: {error}",
                extra=log_data,
                exc_info=True
            )
        elif severity == ErrorSeverity.MEDIUM:
            self.logger.warning(
                f"Error {error_id}: {error}",
                extra=log_data
            )
        else:
            self.logger.info(
                f"Error {error_id}: {error}",
                extra=log_data
            )
    
    def _get_default_message(self, severity: ErrorSeverity) -> str:
        """Get default user message based on severity."""
        messages = {
            ErrorSeverity.LOW: "A minor issue occurred. Please try again.",
            ErrorSeverity.MEDIUM: "An error occurred while processing your request.",
            ErrorSeverity.HIGH: "A serious error occurred. Please contact support.",
            ErrorSeverity.CRITICAL: "A critical system error occurred. Please contact support immediately."
        }
        return messages.get(severity, "An unexpected error occurred.")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat() + "Z"


# Global error manager instance
error_manager = ErrorManager()