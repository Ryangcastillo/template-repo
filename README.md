# Generic Project Template 🚀

This is a **GitHub template repository** for any project (backend, frontend, fullstack, or CLI tool).
It enforces **Spec-Driven Development (SDD)**, **TDD**, **docs-first workflows**, and **API monitoring**.

---

## 🔥 Features
- ✅ Works with any language (Node.js, Python, Go, Rust, Java, etc.)
- ✅ Organized structure (`/src`, `/tests`, `/docs`, `/specs`)
- ✅ Spec Kit integration (`/specs/`)
- ✅ Enforced TDD (native test framework)
- ✅ CI/CD with GitHub Actions:
  - Docs checks
  - Dependency lock check
  - Tests across environments
  - Postman API monitoring
- ✅ AI Contract (`.aiconfig.md`) binding AI agents to rules

---

## 🧩 Workflow
1. Define feature → add spec in `/specs/`.
2. Add/update docs in `/docs/`.
3. Write failing test (Red).
4. Implement feature (Green).
5. Refactor into clean modules (Refactor).
6. Add/update Postman tests in `/postman/collection.json`.
7. Push → GitHub Actions enforces rules.

---

## 📂 Key Folders
- `/src/` → Source code (any language)
- `/tests/` → Unit + integration tests
- `/docs/` → Developer & architecture guides
- `/specs/` → Feature specifications
- `/postman/` → API monitoring

---

## 🚀 Quick Start
```bash
# Clone repo
git clone <your-repo> && cd project-template

# Initialize deps (example for Node.js)
npm install

# Run tests
npm test

# Run API monitoring (Postman)
npx newman run postman/collection.json
```
