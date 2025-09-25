# Project Architecture

## Overview
This project follows a generic, language-agnostic structure that can be adapted for any type of application (backend, frontend, fullstack, or CLI tool).

## Folder Structure
```
project-template/
├── .aiconfig.md          # AI agent contract and rules
├── .github/workflows/    # CI/CD automation
├── docs/                 # All documentation
├── specs/               # Feature specifications (Spec Kit)
├── postman/             # API monitoring and testing
├── src/                 # Main source code
├── tests/               # Unit and integration tests
└── [language files]     # requirements.txt, package.json, etc.
```

## Design Principles
- **Spec-Driven Development**: All features start with specifications
- **Test-Driven Development**: Red → Green → Refactor cycle
- **Documentation First**: Keep docs updated with every change
- **Language Agnostic**: Works with any programming language
- **CI/CD Enforced**: Automated checks for quality and compliance