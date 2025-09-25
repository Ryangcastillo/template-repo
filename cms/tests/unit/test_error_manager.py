"""Unit tests for error manager."""

import pytest
from unittest.mock import Mock, patch
from cms.utils.error_manager import ErrorManager, ErrorSeverity
from cms.exceptions import ValidationError, CMSException


class TestErrorManager:
    """Test suite for ErrorManager class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.error_manager = ErrorManager()
    
    def test_handle_validation_error_with_medium_severity(self):
        """Test handling validation error with medium severity."""
        # Arrange
        error = ValidationError("Invalid email format")
        severity = ErrorSeverity.MEDIUM
        context = {"field": "email", "value": "invalid-email"}
        user_message = "Please enter a valid email address"
        
        # Act
        result = self.error_manager.handle_error(
            error, severity, context, user_message
        )
        
        # Assert
        assert result["message"] == user_message
        assert result["severity"] == "medium"
        assert result["type"] == "ValidationError"
        assert "error_id" in result
        assert "timestamp" in result
        assert result["error_id"].startswith("error_")
    
    def test_handle_critical_error_without_user_message(self):
        """Test handling critical error without user message."""
        # Arrange
        error = Exception("Database connection failed")
        severity = ErrorSeverity.CRITICAL
        
        # Act
        result = self.error_manager.handle_error(error, severity)
        
        # Assert
        assert result["severity"] == "critical"
        assert result["message"] == "A critical system error occurred. Please contact support immediately."
        assert result["type"] == "Exception"
    
    def test_generate_error_id_format(self):
        """Test error ID generation format."""
        # Act
        error_id = self.error_manager._generate_error_id()
        
        # Assert
        assert error_id.startswith("error_")
        assert len(error_id.split("_")) == 3  # error_YYYYMMDD_shortid
        assert len(error_id.split("_")[1]) == 8  # YYYYMMDD format
        assert len(error_id.split("_")[2]) == 8  # 8-character UUID
    
    @patch('cms.utils.error_manager.datetime')
    def test_get_timestamp_format(self, mock_datetime):
        """Test timestamp format generation."""
        # Arrange
        from datetime import datetime
        mock_datetime.utcnow.return_value = datetime(2023, 12, 25, 10, 30, 45)
        
        # Act
        timestamp = self.error_manager._get_timestamp()
        
        # Assert
        assert timestamp == "2023-12-25T10:30:45Z"
    
    def test_get_default_message_for_all_severities(self):
        """Test default messages for all severity levels."""
        # Test all severity levels
        test_cases = [
            (ErrorSeverity.LOW, "A minor issue occurred. Please try again."),
            (ErrorSeverity.MEDIUM, "An error occurred while processing your request."),
            (ErrorSeverity.HIGH, "A serious error occurred. Please contact support."),
            (ErrorSeverity.CRITICAL, "A critical system error occurred. Please contact support immediately.")
        ]
        
        for severity, expected_message in test_cases:
            # Act
            message = self.error_manager._get_default_message(severity)
            
            # Assert
            assert message == expected_message
    
    @patch('cms.utils.error_manager.ErrorManager._log_error')
    def test_log_error_called_with_correct_parameters(self, mock_log_error):
        """Test that _log_error is called with correct parameters."""
        # Arrange
        error = ValidationError("Test error")
        severity = ErrorSeverity.HIGH
        context = {"test": "context"}
        
        # Act
        self.error_manager.handle_error(error, severity, context)
        
        # Assert
        mock_log_error.assert_called_once()
        call_args = mock_log_error.call_args[0]
        assert call_args[0] == error
        assert call_args[1] == severity
        assert call_args[3] == context  # context is the 4th argument
    
    def test_handle_error_with_cms_exception(self):
        """Test handling CMS-specific exceptions."""
        # Arrange
        details = {"field": "username", "constraint": "unique"}
        error = CMSException("Username already exists", details=details)
        severity = ErrorSeverity.MEDIUM
        
        # Act
        result = self.error_manager.handle_error(error, severity)
        
        # Assert
        assert result["type"] == "CMSException"
        assert result["severity"] == "medium"
        assert "error_id" in result