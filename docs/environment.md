# Development Environment

## Python Virtual Environment

### Using Poetry (Recommended)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Initialize project
poetry init

# Install dependencies
poetry install

# Activate environment
poetry shell

# Add dependencies
poetry add django fastapi sqlalchemy
poetry add pytest black flake8 --group dev
```

### Using pip-tools (Alternative)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install pip-tools
pip install pip-tools

# Create requirements files
echo "django>=4.0" > requirements.in
echo "pytest>=7.0" > requirements-dev.in

# Generate lock files
pip-compile requirements.in
pip-compile requirements-dev.in

# Install dependencies
pip-sync requirements.txt requirements-dev.txt
```

## Context7 MCP Integration

### Installation

Context7 MCP provides up-to-date documentation for all packages and libraries.

#### GitHub Copilot Coding Agent
1. Navigate to Repository Settings > Copilot > Coding agent > MCP configuration
2. Add `context7` entry with:
   - Type: `http`
   - URL: `https://mcp.context7.com/mcp`
   - Headers: `CONTEXT7_API_KEY: your_api_key`

#### Local Development (Cursor/VS Code/Claude)
Create `.cursor/mcp.json`:

```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

### Usage

Include **`use context7`** in prompts when:
- Installing new packages
- Using library APIs
- Configuring dependencies
- Checking for updates

## Development Tools

### Code Quality

```bash
# Formatting
black .
isort .

# Linting
flake8 .
pylint cms/

# Type checking
mypy cms/

# Security scanning
bandit -r cms/
safety check
```

### Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Coverage
pytest --cov=cms tests/

# Watch mode
ptw tests/
```

### Database

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Seeds
python manage.py seed_data

# Shell
python manage.py shell
```

## Environment Variables

Create `.env` file:

```env
# Application
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cms_db

# Context7
CONTEXT7_API_KEY=your-context7-key

# External Services
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

## Dependencies Management

Always maintain lockfiles:
- `poetry.lock` (Poetry)
- `requirements.lock` (pip-tools)

Update regularly:

```bash
# Poetry
poetry update

# pip-tools
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in
```