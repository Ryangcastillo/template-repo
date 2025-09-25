# Developer Guidelines

## Code Style and Standards

### Python Code Style

We follow **PEP 8** with the following specific guidelines:

```python
# Good: Clear, descriptive names
def calculate_user_subscription_cost(user_id: str, plan_type: str) -> float:
    """Calculate the cost of a user's subscription plan."""
    pass

# Bad: Unclear abbreviations
def calc_usr_sub_cost(uid: str, pt: str) -> float:
    pass
```

### Type Hints

- **Always use type hints** for function parameters and return values
- Use `typing` module for complex types
- Use `Optional` for nullable values

```python
from typing import Dict, List, Optional, Union

def process_data(
    data: List[Dict[str, Any]], 
    filters: Optional[Dict[str, str]] = None
) -> Union[List[Dict], None]:
    pass
```

### Docstrings

Use **Google-style docstrings**:

```python
def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user with username and password.
    
    Args:
        username: The user's username
        password: The user's password (will be hashed)
    
    Returns:
        True if authentication successful, False otherwise
        
    Raises:
        ValidationError: If username or password format is invalid
        AuthenticationError: If credentials are incorrect
    """
    pass
```

## Git Workflow

### Commit Message Format

All commit messages must follow this pattern:

```
<type>: <description>

[optional body]

[optional footer]
```

**Valid types:**
- `Refactor`: Code refactoring without changing functionality  
- `Fix`: Bug fixes
- `Add`: New features or functionality
- `Update`: Changes to existing features
- `Remove`: Removing code or features
- `Docs`: Documentation changes
- `Spec`: Specification updates

**Examples:**
```
Add: User authentication endpoint with JWT tokens

- Implement login/logout functionality
- Add JWT token generation and validation
- Include rate limiting for auth endpoints

Refactor: Extract database connection logic into separate module

- Move database connection code to utils/database.py
- Add connection pooling and retry logic
- Update all services to use new connection module
```

### Branch Naming

- `feature/feature-name` - New features
- `refactor/component-name` - Refactoring work  
- `fix/bug-description` - Bug fixes
- `docs/topic` - Documentation updates

### Pull Request Guidelines

1. **Keep PRs small** - Max 400 lines changed
2. **Reference specs** - Link to relevant `/specs/` files
3. **Include tests** - All code changes must have tests
4. **Update docs** - Update relevant `/docs/` files
5. **Atomic changes** - One logical change per PR

## Testing Standards

### Test Organization

```
tests/
├── unit/          # Unit tests for individual functions
├── integration/   # Integration tests for modules
├── e2e/          # End-to-end tests
└── fixtures/     # Test data and fixtures
```

### Test Naming Convention

```python
def test_should_return_valid_jwt_token_when_credentials_are_correct():
    """Test that valid credentials generate a proper JWT token."""
    pass

def test_should_raise_validation_error_when_username_is_empty():
    """Test that empty username raises ValidationError."""
    pass
```

### Test Structure (Arrange-Act-Assert)

```python
def test_calculate_subscription_cost():
    # Arrange
    user_id = "user123"
    plan_type = "premium"
    expected_cost = 29.99
    
    # Act
    result = calculate_user_subscription_cost(user_id, plan_type)
    
    # Assert
    assert result == expected_cost
    assert isinstance(result, float)
```

## Code Review Checklist

### For Authors

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has appropriate test coverage
- [ ] Documentation updated if needed
- [ ] No debug code or console.logs left
- [ ] Error handling implemented
- [ ] Performance considerations addressed

### For Reviewers

- [ ] Code is readable and maintainable
- [ ] Business logic is correct
- [ ] Edge cases are handled
- [ ] Security considerations addressed
- [ ] No code duplication
- [ ] Appropriate design patterns used
- [ ] Database queries optimized

## Development Workflow

### 1. Before Starting Work

```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Verify tests pass
pytest

# Check code quality
black --check src/
flake8 src/
```

### 2. During Development

- Write tests first (TDD approach)
- Commit frequently with descriptive messages
- Run tests after each change
- Update documentation as you go

### 3. Before Submitting PR

```bash
# Run full test suite
pytest --cov=src

# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/

# Update documentation
# Update CHANGELOG.md if significant changes
```

## Performance Guidelines

### Database Queries

```python
# Good: Use specific fields
users = session.query(User.id, User.name).filter(User.active == True).all()

# Bad: Select all fields
users = session.query(User).filter(User.active == True).all()
```

### Async Operations

```python
# Good: Use async for I/O operations
async def fetch_user_data(user_id: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return response.json()

# Bad: Blocking I/O in async context
def fetch_user_data_sync(user_id: str) -> Dict:
    response = requests.get(f"/users/{user_id}")  # Blocks event loop
    return response.json()
```

## Security Guidelines

1. **Input Validation**: Validate all inputs at API boundaries
2. **SQL Injection**: Use parameterized queries or ORM
3. **XSS Prevention**: Sanitize all user inputs
4. **Authentication**: Implement proper JWT token handling
5. **Authorization**: Check permissions for all operations
6. **Logging**: Never log sensitive information
7. **Dependencies**: Regularly update and audit dependencies

## IDE Configuration

### VS Code Extensions

Required extensions:
- Python
- Pylint
- Black Formatter
- isort
- GitLens

### Settings

```json
{
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Troubleshooting Common Issues

### Import Errors

```python
# Add to PYTHONPATH or use relative imports
export PYTHONPATH="${PYTHONPATH}:/path/to/project/src"
```

### Test Discovery Issues

```python
# Ensure __init__.py files exist in test directories
# Use proper test naming conventions (test_*.py or *_test.py)
```

### Type Checking Errors

```python
# Use type: ignore comments sparingly and with explanation
result = some_complex_function()  # type: ignore # Complex return type from third-party
```

## Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)