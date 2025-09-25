# Environment Setup

## Prerequisites

- Python 3.9+
- Git
- Poetry (recommended) or pip-tools

## Development Environment Setup

### Option 1: Using Poetry (Recommended)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Clone and setup
git clone <repository-url>
cd <repository-name>

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Option 2: Using pip-tools

```bash
# Install pip-tools
pip install pip-tools

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip-sync requirements.txt
```

### Option 3: Traditional pip

```bash
# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Development settings
DEBUG=True
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=sqlite:///./dev.db

# API Keys (use secure values in production)
API_SECRET_KEY=your-development-secret-key

# External Services
EXTERNAL_API_URL=https://api.example.com
EXTERNAL_API_KEY=your-api-key
```

## Development Tools

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### Linting and Formatting

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/
```

### Development Server

```bash
# Start development server
python -m uvicorn src.main:app --reload --port 8000
```

## IDE Configuration

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true
}
```

## Troubleshooting

### Common Issues

1. **Poetry installation fails**: Use `pip install poetry` as fallback
2. **Virtual environment not activated**: Always activate before running commands
3. **Import errors**: Ensure `PYTHONPATH` includes the `src/` directory
4. **Port conflicts**: Change the port in development server command

### Environment Validation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify environment
python -c "import sys; print(sys.executable)"
```