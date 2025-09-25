"""
Custom exceptions for the CMS application.

This module provides a centralized exception hierarchy for consistent
error handling across the application.
"""

from typing import Dict, Any, Optional


class CMSException(Exception):
    """Base exception for all CMS-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(CMSException):
    """Raised when input validation fails."""
    pass


class AuthenticationError(CMSException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(CMSException):
    """Raised when authorization fails."""
    pass


class SecurityException(CMSException):
    """Raised when security violations are detected."""
    pass


class DatabaseError(CMSException):
    """Raised when database operations fail."""
    pass


class ExternalServiceError(CMSException):
    """Raised when external service calls fail."""
    pass


class BusinessLogicError(CMSException):
    """Raised when business rules are violated."""
    pass


class ConfigurationError(CMSException):
    """Raised when configuration is invalid or missing."""
    pass