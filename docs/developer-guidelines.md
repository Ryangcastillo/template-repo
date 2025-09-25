# Developer Guidelines

## Test-Driven Development (TDD)

### TDD Cycle

1. **Red**: Write a failing test
2. **Green**: Write minimum code to pass
3. **Refactor**: Improve code while keeping tests green

### Test Structure

```python
# tests/test_user_service.py
import pytest
from cms.services.user_service import UserService
from cms.models.user import User

class TestUserService:
    def setup_method(self):
        """Setup for each test method."""
        self.user_service = UserService()
    
    def test_create_user_with_valid_data(self):
        """Test creating user with valid data."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "SecurePass123"
        }
        
        # Act
        result = self.user_service.create_user(user_data)
        
        # Assert
        assert result.success is True
        assert result.user.email == "test@example.com"
    
    def test_create_user_with_invalid_email(self):
        """Test creating user with invalid email."""
        # Arrange
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "SecurePass123"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.user_service.create_user(user_data)
        
        assert "Invalid email format" in str(exc_info.value)
```

### Test Categories

1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete user workflows
4. **Contract Tests**: Test API contracts

## Commit Guidelines

### Commit Message Format

```
Type: Brief description

Longer description if needed.

- Bullet points for details
- Reference issues: Closes #123
```

### Commit Types

- `Refactor`: Code restructuring without functionality changes
- `Fix`: Bug fixes
- `Add`: New features or files
- `Update`: Modifications to existing features
- `Remove`: Deletion of code or files
- `Docs`: Documentation changes
- `Spec`: Specification or requirement changes

### Examples

```
Refactor: Extract user validation logic into service

- Move validation from controller to UserValidationService
- Add comprehensive unit tests for validation rules
- Improve error messages for better UX

Closes #45
```

## Pull Request Guidelines

### Small, Stackable PRs

Break large changes into small, logical units:

1. **PR 1**: Extract utility functions
2. **PR 2**: Create service layer (depends on PR 1)
3. **PR 3**: Update controllers to use services (depends on PR 2)

### PR Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring
- [ ] Documentation
- [ ] Breaking change

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Screenshots
(If applicable)
```

## Code Style Guidelines

### Python Formatting

```python
# Use Black for formatting
black .

# Sort imports with isort
isort .

# Line length: 88 characters (Black default)
# Use double quotes for strings
# Type hints for all function parameters and return values
```

### Naming Conventions

```python
# Classes: PascalCase
class UserService:
    pass

# Functions/Variables: snake_case
def create_user(user_data: dict) -> User:
    is_valid = True
    return user

# Constants: UPPER_SNAKE_CASE
MAX_LOGIN_ATTEMPTS = 3

# Private methods: leading underscore
def _validate_password(self, password: str) -> bool:
    pass
```

### Documentation

```python
class UserService:
    """Service for managing user operations.
    
    This service handles user creation, validation, and management
    following the business rules defined in the user domain.
    """
    
    def create_user(self, user_data: dict) -> UserResult:
        """Create a new user with validation.
        
        Args:
            user_data: Dictionary containing user information
                - email: User's email address
                - username: Unique username
                - password: Plain text password (will be hashed)
        
        Returns:
            UserResult: Result object with success status and user data
        
        Raises:
            ValidationError: When user data is invalid
            DuplicateEmailError: When email already exists
        """
        pass
```

## Code Review Process

### Before Requesting Review

1. **Self-review**: Review your own code first
2. **Tests**: Ensure all tests pass
3. **Documentation**: Update relevant documentation
4. **Linting**: Fix all linting issues

### Review Checklist

- [ ] Code follows established patterns
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling implemented
- [ ] Documentation updated

### Review Response

```markdown
Thanks for the review! I've addressed your comments:

- ✅ Fixed the validation logic in user_service.py
- ✅ Added missing test cases for edge cases
- ❓ Question about the caching strategy - should we cache at service or repository level?
- 🚧 Working on the performance optimization, will update shortly
```

## Refactoring Guidelines

### When to Refactor

1. **Code smells detected**:
   - Long functions (>20 lines)
   - Duplicated code
   - Complex conditionals
   - Large classes

2. **Before adding new features**:
   - Clean up related code first
   - Ensure good test coverage

3. **Regular maintenance**:
   - Weekly code review
   - Monthly architecture review

### Refactoring Steps

1. **Ensure tests exist** for the code being refactored
2. **Run tests** to establish baseline
3. **Make small changes** incrementally
4. **Run tests** after each change
5. **Commit frequently** with descriptive messages

### Safe Refactoring Techniques

```python
# Extract Method
def process_user_data(self, data):
    # Before: Long method with multiple responsibilities
    if not data.get('email'):
        raise ValidationError("Email required")
    
    if not self._is_valid_email(data['email']):
        raise ValidationError("Invalid email")
    
    if User.objects.filter(email=data['email']).exists():
        raise DuplicateEmailError("Email exists")
    
    hashed_password = self._hash_password(data['password'])
    user = User.objects.create(
        email=data['email'],
        password=hashed_password
    )
    return user

# After: Extracted methods
def process_user_data(self, data):
    self._validate_user_data(data)
    return self._create_user(data)

def _validate_user_data(self, data):
    self._validate_email(data.get('email'))
    self._check_email_uniqueness(data['email'])

def _create_user(self, data):
    hashed_password = self._hash_password(data['password'])
    return User.objects.create(
        email=data['email'],
        password=hashed_password
    )
```