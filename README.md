# Python AI Refactor Template 🚀

This is a **GitHub template repository** designed for projects maintained and refactored using **AI coding agents** with **spec-driven development**.

## Features
- ✅ One-shot **Copilot Super Prompt** (in `.aiconfig.md`)
- ✅ **Step-by-step Playbook** for guided refactoring
- ✅ Organized `/docs/` folder (architecture, environment, security, error handling, tasks)
- ✅ **spec-kit integration** (`/specs/` folder)
- ✅ **GitHub Actions** enforcement (commit messages, changelog, lockfiles, TDD)

## Quick Start

### 1. Use This Template
1. Click **"Use this template"** when creating a new repository
2. Clone your new repository
3. Follow the setup instructions below

### 2. Environment Setup

#### Using Poetry (Recommended)
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Initialize project
poetry init

# Install dependencies
poetry install

# Activate environment
poetry shell
```

#### Using pip-tools (Alternative)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install pip-tools
pip install pip-tools

# Install dependencies
pip-sync requirements.txt requirements-dev.txt
```

### 3. Context7 MCP Configuration

For up-to-date library documentation, configure Context7 MCP:

**GitHub Copilot Coding Agent:**
1. Go to Repository Settings > Copilot > Coding agent > MCP configuration
2. Add `context7` entry with type `http`, URL `https://mcp.context7.com/mcp`

**Local Development (Cursor/VS Code):**
```json
// .cursor/mcp.json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

## Repository Structure

```
python-ai-refactor-template/
├── .aiconfig.md                 # AI Agent binding contract
├── .github/
│   └── workflows/
│       └── refactor-checks.yml  # Contract enforcement
├── docs/                        # Comprehensive documentation
│   ├── architecture.md          # System architecture & design
│   ├── environment.md           # Development environment
│   ├── error-handling.md        # Error management strategy
│   ├── developer-guidelines.md  # TDD & coding practices
│   ├── security.md             # Security guidelines
│   ├── tasks.md                # Project management
│   └── changelog.md            # Version history
├── specs/                      # Spec-kit specifications
│   └── README.md               # Spec-kit usage guide
├── cms/                        # Python CMS application
│   ├── controllers/            # HTTP request handlers
│   ├── services/               # Business logic
│   ├── models/                 # Data models
│   ├── repositories/           # Data access layer
│   ├── validators/             # Input validation
│   ├── middleware/             # Request/response processing
│   ├── utils/                  # Shared utilities
│   ├── exceptions/             # Custom exceptions
│   └── tests/                  # Test suites
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Core Principles

### 1. AI Agent Compatibility
- **Binding Contract**: `.aiconfig.md` enforces development rules
- **Automated Checks**: GitHub Actions validate compliance
- **Context7 Integration**: Up-to-date library documentation

### 2. Test-Driven Development
- **Red → Green → Refactor** cycle mandatory
- Comprehensive test coverage (unit, integration, e2e)
- Tests written before code changes

### 3. Security by Design
- Input validation at all entry points
- Output encoding for XSS prevention
- Centralized authentication & authorization
- Regular security audits and dependency scanning

### 4. Modular Architecture
- **Layered Design**: Clear separation of concerns
- **Dependency Injection**: Loose coupling between components
- **Single Responsibility**: Each component has one purpose
- **Open/Closed Principle**: Extensible without modification

## Development Workflow

### 1. Feature Development
```bash
# Start with spec-kit
specify init "Feature Name"
specify /plan
specify /tasks

# Create feature branch
git checkout -b feature/feature-name

# Follow TDD cycle
# 1. Write failing test (Red)
# 2. Write minimal code (Green)
# 3. Refactor while keeping tests green
```

### 2. Commit Guidelines
Commit messages must start with one of:
- `Refactor`: Code restructuring without functionality changes
- `Fix`: Bug fixes
- `Add`: New features or files
- `Update`: Modifications to existing features
- `Remove`: Deletion of code or files
- `Docs`: Documentation changes
- `Spec`: Specification or requirement changes

Example:
```bash
git commit -m "Refactor: Extract user validation logic into service

- Move validation from controller to UserValidationService
- Add comprehensive unit tests for validation rules
- Improve error messages for better UX

Closes #45"
```

### 3. Pull Request Process
- **Small PRs**: Break large changes into small, logical units
- **Stacked PRs**: Use dependencies for related changes
- **Review**: All code must be reviewed before merging
- **Tests**: All tests must pass before merging

## Usage Examples

### Starting a New CMS Project
```bash
# Use this template
git clone https://github.com/yourusername/your-cms-project
cd your-cms-project

# Set up environment
poetry install
poetry shell

# Initialize database
python manage.py migrate
python manage.py seed_data

# Start development server
python manage.py runserver
```

### AI Agent Integration
When working with AI coding agents, include **`use context7`** in prompts for:
- Package installation
- Library API usage
- Configuration examples
- Best practices

Example prompt:
```
"use context7 to help me implement JWT authentication with the latest version of PyJWT, including proper error handling and security best practices"
```

## Documentation

Comprehensive documentation is available in the `/docs/` folder:

- **[Architecture](docs/architecture.md)**: System design and component structure
- **[Environment](docs/environment.md)**: Development environment setup
- **[Security](docs/security.md)**: Security guidelines and best practices  
- **[Developer Guidelines](docs/developer-guidelines.md)**: TDD practices and coding standards
- **[Error Handling](docs/error-handling.md)**: Centralized error management
- **[Tasks](docs/tasks.md)**: Project management and workflow

## Contributing

1. **Follow the AI Agent Contract**: All changes must comply with `.aiconfig.md`
2. **Write Tests First**: Follow TDD practices
3. **Document Changes**: Update relevant documentation
4. **Small PRs**: Keep changes focused and reviewable
5. **Security First**: Consider security implications of all changes

## License

This template is available under the MIT License. See LICENSE file for details.

## Support

- **Documentation**: Check `/docs/` folder for comprehensive guides
- **Issues**: Use GitHub Issues with appropriate labels
- **Discussions**: Use GitHub Discussions for questions and ideas

---

⚠️ **AI Agent Contract Enforcement**: This repository enforces strict development practices through automated checks. All contributions must follow the guidelines in `.aiconfig.md` or they will be rejected.
