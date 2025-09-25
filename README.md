# Python AI Refactor Template 🚀

This is a **GitHub template repository** designed for projects maintained and refactored using **AI coding agents** with **Spec-Driven Development (SDD)**.

---

## 🔥 Condensed Copilot Super Prompt (One-Shot)

You are an **expert System Coder/Developer** specializing in **modular architecture, testing, and security**.  
Your task is to refactor this entire codebase into a **modern, secure, API-first architecture** while keeping external behavior unchanged.

### Follow these rules:
- **TDD First** → Red → Green → Refactor. Add missing tests before refactoring.  
- **GitHub Best Practices** → atomic commits, stacked PRs, spec kit conventions.  
- **Context7 MCP + GitHub MCP** → always reference for docs, APIs, dependencies.  
- **Architecture & Modularity** → clear layers (DAL, Services, API), DRY, small reusable modules, `/docs` folder.  
- **Dependencies** → remove unused, upgrade outdated, maintain lockfiles.  
- **Error Handling & Security** → centralized error handling, retries, harden input/output.  
- **Docs** → update `/docs/`, auto-generate `README.md`, changelog.  
- **AI Helpers** → create scripts for dependency audits, schema checks, linting.  

---

## 🧩 Step-by-Step Playbook

### Phase 1: Setup & Safety
- Create branch: `refactor/core-architecture`
- Run all tests, add missing coverage
- Enable GitHub Actions for CI (this template already has it)

### Phase 2: Dependencies & Environment
- Audit dependencies, remove unused
- Set up `.venv` or Poetry
- Document in `/docs/environment.md`

### Phase 3: Architecture & Modularity
- Restructure into layers (DAL, Services, API)
- Modularize long functions
- Keep docs in `/docs/`
- Commit atomically

### Phase 4: Error Management & Security
- Centralize error handling
- Add structured logging
- Harden API endpoints
- Document in `/docs/error-handling.md`

### Phase 5: Documentation & Guidelines
- Generate repo structure diagrams
- Update `README.md` + `/docs/developer-guidelines.md`
- Include GitHub workflow practices

### Phase 6: Finalization
- Review commits for atomicity
- Stack PRs logically
- Run regression tests
- Merge only if CI passes

---

## 📂 Repository Structure

```
python-ai-refactor-template/
├── .aiconfig.md                    # AI Agent Contract (binding rules)
├── .github/
│   └── workflows/
│       └── refactor-checks.yml     # CI/CD pipeline
├── docs/                           # Comprehensive documentation
│   ├── architecture.md             # System architecture guidelines
│   ├── environment.md              # Environment setup guide
│   ├── error-handling.md           # Error handling & security
│   ├── developer-guidelines.md     # Code style & workflows
│   ├── security.md                 # Security best practices
│   ├── tasks.md                    # Development task workflows
│   └── changelog.md                # Change tracking
├── specs/                          # Spec-Kit specifications
│   └── README.md                   # Spec-Kit workflow guide
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🤖 AI Agent Integration

This template is designed for AI-driven development with binding contracts:

### Spec-Driven Development (SDD)
Every new feature follows the **Spec Kit** workflow:
1. **Constitution** → Project principles and standards
2. **Specify** → Define what and why
3. **Plan** → Define how (technical approach)
4. **Tasks** → Break into atomic steps
5. **Implement** → Code based on the plan

### Context7 MCP Integration
Use Context7 MCP (`use context7`) for:
- Library and API documentation
- Best practices lookup
- Code pattern examples
- Dependency recommendations

### Binding AI Contract
All AI agents must follow the rules in `.aiconfig.md`:
- Spec-driven workflow for all features
- TDD approach (Red → Green → Refactor)
- Atomic commits with proper message format
- Documentation updates in `/docs/`
- Security-first development

---

## 🚀 Quick Start

### 1. Use This Template
Click "Use this template" on GitHub or:
```bash
git clone https://github.com/Ryangcastillo/template-repo.git your-project-name
cd your-project-name
```

### 2. Set Up Environment
```bash
# Option 1: Using Poetry (recommended)
pip install poetry
poetry install

# Option 2: Using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Your Project
```bash
# Update project name in files
# Customize requirements.txt for your needs
# Update .env with your configuration

# Initialize Git
git remote set-url origin https://github.com/your-username/your-repo.git
```

### 4. Start Development
```bash
# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Start development server (when you add FastAPI)
uvicorn src.main:app --reload
```

---

## 📋 Development Workflow

### For AI Agents
1. **Read `.aiconfig.md`** - Follow all binding rules
2. **Check `/docs/`** - Understand architecture and guidelines
3. **Use Spec Kit** - Create specs in `/specs/` before coding
4. **Follow TDD** - Write tests first, then implement
5. **Commit atomically** - Use proper commit message format
6. **Update docs** - Keep documentation current

### For Human Developers
1. **Environment Setup** - Follow `/docs/environment.md`
2. **Code Guidelines** - Follow `/docs/developer-guidelines.md`
3. **Security Practices** - Follow `/docs/security.md`
4. **Task Management** - Use workflows in `/docs/tasks.md`

---

## 🛡️ Security & Quality

This template includes:
- **Input validation** patterns and middleware
- **Authentication** with JWT tokens
- **Error handling** with centralized error management
- **Rate limiting** and security headers
- **Automated security audits** in CI/CD
- **Code quality checks** with linting and formatting

---

## 📚 Documentation

Complete documentation is available in the `/docs/` folder:

- **[Architecture](docs/architecture.md)** - System design and patterns
- **[Environment](docs/environment.md)** - Setup and configuration
- **[Error Handling](docs/error-handling.md)** - Error management and security
- **[Developer Guidelines](docs/developer-guidelines.md)** - Code style and workflows
- **[Security](docs/security.md)** - Security best practices
- **[Tasks](docs/tasks.md)** - Development workflows and automation
- **[Changelog](docs/changelog.md)** - Project history and changes

---

## 🤝 Contributing

1. **Read the AI Contract** - Understand the binding rules in `.aiconfig.md`
2. **Create Specifications** - Use Spec Kit workflow for new features
3. **Follow TDD** - Write tests first, then implement
4. **Use Proper Commits** - Follow the commit message format
5. **Update Documentation** - Keep `/docs/` current
6. **Run Quality Checks** - Ensure all tests and linting pass

---

## 📄 License

This template is MIT licensed. Feel free to use it for your projects.

---

## 🎯 Template Features

✅ **AI-Driven Development Ready**  
✅ **Spec-Kit Integration**  
✅ **Context7 MCP Compatible**  
✅ **Security Hardened**  
✅ **TDD Workflow**  
✅ **Comprehensive Documentation**  
✅ **GitHub Actions CI/CD**  
✅ **Modern Python Stack**  
✅ **Scalable Architecture**  
✅ **Developer Experience Optimized**  

---

**Ready to build something amazing with AI-assisted development? Start with this template and follow the playbook!** 🚀
