# Development Tasks & Workflows

## Standard Development Tasks

### Task 1: Setting Up a New Feature

**Objective**: Create a new feature following Spec-Driven Development

**Steps**:
1. Create feature specification in `/specs/`
2. Set up feature branch: `git checkout -b feature/feature-name`
3. Write failing tests (Red phase)
4. Implement minimal code to pass tests (Green phase)
5. Refactor code for quality (Refactor phase)
6. Update documentation
7. Submit pull request

**Example Workflow**:
```bash
# 1. Create specification
echo "# Feature: User Profile Management" > specs/user-profile.md

# 2. Create branch
git checkout -b feature/user-profile

# 3. Write tests first
# Create test file in tests/unit/test_user_profile.py

# 4. Implement feature
# Create implementation in src/services/user_profile.py

# 5. Verify all tests pass
pytest tests/unit/test_user_profile.py

# 6. Update docs
# Update relevant files in /docs/

# 7. Commit and push
git add .
git commit -m "Add: User profile management feature with CRUD operations"
git push origin feature/user-profile
```

### Task 2: Refactoring Existing Code

**Objective**: Improve code quality without changing external behavior

**Steps**:
1. Ensure comprehensive test coverage exists
2. Create refactor branch: `git checkout -b refactor/component-name`
3. Run tests to establish baseline
4. Make incremental changes
5. Run tests after each change
6. Document architectural decisions
7. Submit pull request

**Refactoring Checklist**:
- [ ] Extract long methods into smaller functions
- [ ] Remove code duplication
- [ ] Improve variable and function names
- [ ] Add type hints where missing
- [ ] Optimize database queries
- [ ] Update documentation

### Task 3: Bug Fixing

**Objective**: Fix reported issues systematically

**Steps**:
1. Reproduce the bug with a failing test
2. Create fix branch: `git checkout -b fix/bug-description`
3. Implement minimal fix
4. Ensure fix doesn't break existing functionality
5. Update documentation if needed
6. Submit pull request with bug details

**Bug Fix Template**:
```python
def test_bug_reproduction():
    """Test that reproduces the reported bug."""
    # Arrange: Set up the conditions that cause the bug
    user = create_test_user()
    invalid_data = {"email": "not-an-email"}
    
    # Act & Assert: Verify the bug exists
    with pytest.raises(ValidationError):
        user.update_email(invalid_data["email"])

def test_bug_fix():
    """Test that verifies the bug is fixed."""
    # Arrange: Set up the same conditions
    user = create_test_user()
    valid_data = {"email": "test@example.com"}
    
    # Act: Apply the fix
    result = user.update_email(valid_data["email"])
    
    # Assert: Verify the fix works
    assert result == True
    assert user.email == valid_data["email"]
```

## Automated Development Tasks

### Task 4: Dependency Management

**Scripts for automation**:

```bash
#!/bin/bash
# scripts/update_dependencies.sh

echo "🔍 Checking for outdated packages..."
pip list --outdated

echo "🔒 Updating lockfile..."
if [ -f "poetry.lock" ]; then
    poetry update
elif [ -f "requirements.txt" ]; then
    pip-compile --upgrade requirements.in
fi

echo "🛡️ Running security audit..."
pip-audit

echo "🧪 Running tests with updated dependencies..."
pytest

echo "✅ Dependencies updated successfully!"
```

### Task 5: Code Quality Checks

```bash
#!/bin/bash
# scripts/quality_check.sh

echo "🎨 Formatting code..."
black src/ tests/
isort src/ tests/

echo "🔍 Linting code..."
flake8 src/ tests/
mypy src/

echo "🧪 Running tests..."
pytest --cov=src --cov-report=term-missing

echo "📊 Generating coverage report..."
coverage html

echo "✅ Quality checks completed!"
```

### Task 6: Security Audit

```bash
#!/bin/bash
# scripts/security_audit.sh

echo "🔒 Checking for known vulnerabilities..."
safety check

echo "🛡️ Scanning for secrets..."
truffleHog --regex --entropy=False .

echo "🔍 Analyzing dependencies..."
pip-audit

echo "📋 Generating security report..."
bandit -r src/ -f json -o security_report.json

echo "✅ Security audit completed!"
```

## AI-Assisted Development Tasks

### Task 7: Code Review Preparation

**Using Context7 MCP for comprehensive analysis**:

```bash
# Prepare comprehensive context for AI review
echo "📝 Generating code review context..."

# Get current changes
git --no-pager diff > changes.diff

# Get project structure
tree src/ > project_structure.txt

# Get test coverage
pytest --cov=src --cov-report=term > coverage.txt

# Use Context7 MCP to analyze
echo "🤖 Running AI-assisted code review..."
# This would integrate with Context7 MCP to provide intelligent feedback
```

### Task 8: Documentation Generation

**Automated documentation updates**:

```python
#!/usr/bin/env python3
# scripts/generate_docs.py

import ast
import os
from typing import List, Dict

def extract_functions(file_path: str) -> List[Dict]:
    """Extract function information from Python file."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                'name': node.name,
                'line': node.lineno,
                'docstring': ast.get_docstring(node)
            })
    
    return functions

def generate_api_docs():
    """Generate API documentation from source code."""
    api_functions = []
    
    for root, dirs, files in os.walk('src/'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions = extract_functions(file_path)
                api_functions.extend(functions)
    
    # Generate markdown documentation
    with open('docs/api_reference.md', 'w') as doc_file:
        doc_file.write("# API Reference\n\n")
        for func in api_functions:
            if func['docstring']:
                doc_file.write(f"## {func['name']}\n\n")
                doc_file.write(f"{func['docstring']}\n\n")

if __name__ == "__main__":
    generate_api_docs()
    print("📚 API documentation generated!")
```

## Testing Tasks

### Task 9: Test Coverage Analysis

```bash
#!/bin/bash
# scripts/coverage_analysis.sh

echo "📊 Running comprehensive test coverage analysis..."

# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=80

# Generate coverage badge
coverage-badge -f -o coverage.svg

echo "📈 Coverage report generated in htmlcov/index.html"
echo "🎯 Coverage badge updated: coverage.svg"

# Find uncovered lines
echo "❌ Uncovered lines:"
coverage report --show-missing | grep -E "^src/"
```

### Task 10: Performance Testing

```python
#!/usr/bin/env python3
# scripts/performance_test.py

import time
import statistics
from typing import List, Callable

def measure_performance(func: Callable, iterations: int = 100) -> Dict:
    """Measure function performance over multiple iterations."""
    times = []
    
    for _ in range(iterations):
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times)
    }

def benchmark_critical_functions():
    """Benchmark critical application functions."""
    # Import your critical functions here
    from src.services.user_service import authenticate_user
    from src.services.data_service import process_large_dataset
    
    # Benchmark authentication
    auth_stats = measure_performance(
        lambda: authenticate_user("test_user", "test_password"),
        iterations=1000
    )
    
    print(f"Authentication Performance:")
    print(f"  Mean: {auth_stats['mean']:.4f}s")
    print(f"  Median: {auth_stats['median']:.4f}s")
    print(f"  Std Dev: {auth_stats['stdev']:.4f}s")

if __name__ == "__main__":
    benchmark_critical_functions()
```

## Deployment Tasks

### Task 11: Pre-deployment Checklist

```bash
#!/bin/bash
# scripts/pre_deployment.sh

echo "🚀 Running pre-deployment checks..."

# Security checks
echo "🔒 Security audit..."
safety check
bandit -r src/

# Code quality
echo "🎨 Code quality checks..."
flake8 src/
mypy src/

# Tests
echo "🧪 Running full test suite..."
pytest --cov=src --cov-fail-under=80

# Dependencies
echo "📦 Checking dependencies..."
pip check

# Environment validation
echo "🌍 Validating environment..."
python -c "import src.config; print('✅ Config validated')"

# Database migrations (if applicable)
echo "🗄️ Checking database migrations..."
# Add your migration check command here

echo "✅ Pre-deployment checks completed!"
```

### Task 12: Environment Setup

```bash
#!/bin/bash
# scripts/setup_environment.sh

echo "🔧 Setting up development environment..."

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
if [ -f "poetry.lock" ]; then
    pip install poetry
    poetry install
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install development tools
pip install pre-commit black flake8 mypy pytest coverage

# Setup pre-commit hooks
pre-commit install

# Create local configuration
cp .env.example .env
echo "📝 Please update .env with your local settings"

echo "✅ Development environment setup completed!"
```

## Maintenance Tasks

### Task 13: Weekly Maintenance

```bash
#!/bin/bash
# scripts/weekly_maintenance.sh

echo "🔄 Running weekly maintenance tasks..."

# Update dependencies
echo "📦 Updating dependencies..."
if [ -f "poetry.lock" ]; then
    poetry update
fi

# Security audit
echo "🔒 Security audit..."
safety check
pip-audit

# Clean up temporary files
echo "🧹 Cleaning up..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Update documentation
echo "📚 Updating documentation..."
python scripts/generate_docs.py

# Run full test suite
echo "🧪 Running tests..."
pytest

echo "✅ Weekly maintenance completed!"
```

## Integration with AI Tools

### Task 14: Spec-Kit Integration

```bash
#!/bin/bash
# scripts/spec_kit_workflow.sh

echo "📋 Starting Spec-Kit workflow..."

# Constitution check
if [ ! -f "specs/constitution.md" ]; then
    echo "📜 Creating project constitution..."
    # Template for constitution
    cat > specs/constitution.md << EOF
# Project Constitution

## Core Principles
1. Code quality over speed
2. Security by design
3. Test-driven development
4. Clear documentation

## Technical Standards
- Python 3.9+
- Type hints required
- 80%+ test coverage
- No security vulnerabilities

## Decision Making
- All major changes require specs
- Code reviews mandatory
- Automated testing required
EOF
fi

echo "✅ Spec-Kit workflow initialized!"
```

## Task Templates

### New Feature Template

```markdown
# Feature: [Feature Name]

## Specification
- **What**: Brief description of the feature
- **Why**: Business justification
- **Who**: Target users

## Technical Plan
- **Architecture**: How it fits into existing system
- **Dependencies**: Required libraries or services
- **Database Changes**: Schema modifications needed

## Implementation Tasks
- [ ] Write tests
- [ ] Implement core logic
- [ ] Add API endpoints
- [ ] Update documentation
- [ ] Security review
- [ ] Performance testing

## Acceptance Criteria
- [ ] All tests pass
- [ ] Code coverage maintained
- [ ] Security review completed
- [ ] Documentation updated
```

### Bug Fix Template

```markdown
# Bug Fix: [Bug Description]

## Problem
- **Symptom**: What users experience
- **Root Cause**: Technical cause of the issue
- **Impact**: Who is affected and how

## Solution
- **Approach**: High-level solution strategy
- **Changes**: Specific code changes needed
- **Testing**: How to verify the fix

## Implementation
- [ ] Reproduce bug with test
- [ ] Implement fix
- [ ] Verify fix works
- [ ] Ensure no regressions
- [ ] Update documentation if needed
```

These tasks and templates provide a comprehensive framework for AI-assisted development while maintaining code quality, security, and documentation standards.