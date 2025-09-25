"""
Security utilities for input validation and sanitization.
"""

import re
import bleach
from typing import Any, Dict
from marshmallow import Schema, fields, validate, ValidationError

from cms.exceptions import SecurityException


class InputValidator:
    """Centralized input validation and sanitization."""
    
    # Email regex pattern (RFC 5322 compliant)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )
    
    # Username pattern: alphanumeric and underscores only
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')
    
    # Strong password pattern
    PASSWORD_PATTERN = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]'
    )
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format."""
        if not email or not isinstance(email, str):
            return False
        return bool(cls.EMAIL_PATTERN.match(email.strip().lower()))
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """Validate username format."""
        if not username or not isinstance(username, str):
            return False
        return (
            3 <= len(username) <= 30 and
            bool(cls.USERNAME_PATTERN.match(username))
        )
    
    @classmethod
    def validate_password(cls, password: str) -> bool:
        """Validate password strength."""
        if not password or not isinstance(password, str):
            return False
        return (
            8 <= len(password) <= 128 and
            bool(cls.PASSWORD_PATTERN.match(password))
        )
    
    @classmethod
    def sanitize_html(cls, content: str) -> str:
        """Remove dangerous HTML tags and attributes."""
        if not content:
            return ""
        
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3',
            'h4', 'h5', 'h6', 'blockquote', 'a', 'img'
        ]
        
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
        }
        
        return bleach.clean(
            content, 
            tags=allowed_tags, 
            attributes=allowed_attributes,
            strip=True
        )
    
    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 255) -> str:
        """Sanitize general string input."""
        if not value:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f]', '', str(value))
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Truncate to max length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized


class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    
    email = fields.Email(required=True)
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=30),
            validate.Regexp(
                InputValidator.USERNAME_PATTERN,
                error="Username can only contain letters, numbers, and underscores"
            )
        ]
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                InputValidator.PASSWORD_PATTERN,
                error="Password must contain uppercase, lowercase, number, and special character"
            )
        ]
    )
    first_name = fields.Str(
        required=False,
        validate=validate.Length(max=50),
        load_default=""
    )
    last_name = fields.Str(
        required=False,
        validate=validate.Length(max=50),
        load_default=""
    )


class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


class PasswordResetSchema(Schema):
    """Schema for password reset validation."""
    
    email = fields.Email(required=True)


class ValidationHelper:
    """Helper methods for validation operations."""
    
    @staticmethod
    def validate_data(data: Dict[str, Any], schema_class: Schema) -> Dict[str, Any]:
        """Validate data using marshmallow schema.
        
        Args:
            data: Data to validate
            schema_class: Marshmallow schema class
            
        Returns:
            Validated and deserialized data
            
        Raises:
            SecurityException: When validation fails
        """
        schema = schema_class()
        try:
            return schema.load(data)
        except ValidationError as e:
            raise SecurityException(
                "Invalid input data",
                details={"validation_errors": e.messages}
            )
    
    @staticmethod
    def validate_user_registration(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user registration data."""
        return ValidationHelper.validate_data(data, UserRegistrationSchema)
    
    @staticmethod
    def validate_user_login(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user login data."""
        return ValidationHelper.validate_data(data, UserLoginSchema)
    
    @staticmethod
    def validate_password_reset(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate password reset data."""
        return ValidationHelper.validate_data(data, PasswordResetSchema)