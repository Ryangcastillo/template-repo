"""Unit tests for input validation."""

import pytest
from cms.validators.input_validator import (
    InputValidator, ValidationHelper, UserRegistrationSchema,
    UserLoginSchema, PasswordResetSchema
)
from cms.exceptions import SecurityException


class TestInputValidator:
    """Test suite for InputValidator class."""
    
    def test_validate_email_with_valid_emails(self):
        """Test email validation with valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user+tag@domain.co.uk",
            "firstname.lastname@company.org",
            "number123@test-domain.com"
        ]
        
        for email in valid_emails:
            assert InputValidator.validate_email(email) is True
    
    def test_validate_email_with_invalid_emails(self):
        """Test email validation with invalid email addresses."""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user space@domain.com",
            "",
            None,
            123
        ]
        
        for email in invalid_emails:
            assert InputValidator.validate_email(email) is False
    
    def test_validate_username_with_valid_usernames(self):
        """Test username validation with valid usernames."""
        valid_usernames = [
            "testuser",
            "user_123",
            "Test_User_2023",
            "abc"  # minimum length
        ]
        
        for username in valid_usernames:
            assert InputValidator.validate_username(username) is True
    
    def test_validate_username_with_invalid_usernames(self):
        """Test username validation with invalid usernames."""
        invalid_usernames = [
            "ab",  # too short
            "a" * 31,  # too long
            "user-name",  # contains hyphen
            "user name",  # contains space
            "user@name",  # contains special char
            "",
            None
        ]
        
        for username in invalid_usernames:
            assert InputValidator.validate_username(username) is False
    
    def test_validate_password_with_strong_passwords(self):
        """Test password validation with strong passwords."""
        strong_passwords = [
            "SecurePass123!",
            "MyP@ssw0rd",
            "C0mplex&Secure",
            "Test123@"  # minimum requirements
        ]
        
        for password in strong_passwords:
            assert InputValidator.validate_password(password) is True
    
    def test_validate_password_with_weak_passwords(self):
        """Test password validation with weak passwords."""
        weak_passwords = [
            "password",  # no uppercase, number, special char
            "PASSWORD",  # no lowercase, number, special char
            "Password",  # no number, special char
            "Password1",  # no special char
            "Pass1!",  # too short
            "a" * 129,  # too long
            "",
            None
        ]
        
        for password in weak_passwords:
            assert InputValidator.validate_password(password) is False
    
    def test_sanitize_html_removes_dangerous_tags(self):
        """Test HTML sanitization removes dangerous tags."""
        # Arrange
        dangerous_html = """
        <script>alert('xss')</script>
        <p>Safe content</p>
        <iframe src="malicious.com"></iframe>
        <strong>Bold text</strong>
        <a href="javascript:alert('xss')">Link</a>
        """
        
        # Act
        result = InputValidator.sanitize_html(dangerous_html)
        
        # Assert
        assert "<script>" not in result
        assert "<iframe>" not in result
        assert "javascript:" not in result
        assert "<p>Safe content</p>" in result
        assert "<strong>Bold text</strong>" in result
    
    def test_sanitize_html_preserves_allowed_tags(self):
        """Test HTML sanitization preserves allowed tags."""
        # Arrange
        safe_html = """
        <h1>Title</h1>
        <p>Paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        <a href="https://example.com" title="Example">Link</a>
        """
        
        # Act
        result = InputValidator.sanitize_html(safe_html)
        
        # Assert
        assert "<h1>Title</h1>" in result
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result
        assert "<ul>" in result
        assert "<li>" in result
        assert 'href="https://example.com"' in result
        assert 'title="Example"' in result
    
    def test_sanitize_string_removes_control_characters(self):
        """Test string sanitization removes control characters."""
        # Arrange
        malicious_string = "Normal text\x00\x1f\x7f with control chars"
        
        # Act
        result = InputValidator.sanitize_string(malicious_string)
        
        # Assert
        assert result == "Normal text with control chars"
    
    def test_sanitize_string_trims_whitespace(self):
        """Test string sanitization trims whitespace."""
        # Arrange
        string_with_whitespace = "   \t  Normal text  \n  "
        
        # Act
        result = InputValidator.sanitize_string(string_with_whitespace)
        
        # Assert
        assert result == "Normal text"
    
    def test_sanitize_string_truncates_long_strings(self):
        """Test string sanitization truncates long strings."""
        # Arrange
        long_string = "a" * 300
        
        # Act
        result = InputValidator.sanitize_string(long_string, max_length=100)
        
        # Assert
        assert len(result) == 100
        assert result == "a" * 100


class TestValidationHelper:
    """Test suite for ValidationHelper class."""
    
    def test_validate_user_registration_with_valid_data(self):
        """Test user registration validation with valid data."""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        # Act
        result = ValidationHelper.validate_user_registration(valid_data)
        
        # Assert
        assert result["email"] == "test@example.com"
        assert result["username"] == "testuser"
        assert result["password"] == "SecurePass123!"
        assert result["first_name"] == "John"
        assert result["last_name"] == "Doe"
    
    def test_validate_user_registration_with_missing_required_fields(self):
        """Test user registration validation with missing required fields."""
        # Arrange
        invalid_data = {
            "email": "test@example.com"
            # missing username and password
        }
        
        # Act & Assert
        with pytest.raises(SecurityException) as exc_info:
            ValidationHelper.validate_user_registration(invalid_data)
        
        assert "Invalid input data" in str(exc_info.value)
        assert "validation_errors" in exc_info.value.details
    
    def test_validate_user_login_with_valid_data(self):
        """Test user login validation with valid data."""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        # Act
        result = ValidationHelper.validate_user_login(valid_data)
        
        # Assert
        assert result["email"] == "test@example.com"
        assert result["password"] == "password123"
    
    def test_validate_user_login_with_invalid_email(self):
        """Test user login validation with invalid email."""
        # Arrange
        invalid_data = {
            "email": "invalid-email",
            "password": "password123"
        }
        
        # Act & Assert
        with pytest.raises(SecurityException):
            ValidationHelper.validate_user_login(invalid_data)
    
    def test_validate_password_reset_with_valid_email(self):
        """Test password reset validation with valid email."""
        # Arrange
        valid_data = {"email": "test@example.com"}
        
        # Act
        result = ValidationHelper.validate_password_reset(valid_data)
        
        # Assert
        assert result["email"] == "test@example.com"
    
    def test_validate_data_with_custom_schema(self):
        """Test generic data validation with custom schema."""
        # Arrange
        valid_data = {"email": "test@example.com", "password": "test123"}
        
        # Act
        result = ValidationHelper.validate_data(valid_data, UserLoginSchema)
        
        # Assert
        assert result["email"] == "test@example.com"
        assert result["password"] == "test123"