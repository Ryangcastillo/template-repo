# Developer Guidelines

## Code Standards
- Use consistent code formatting (prettier, black, gofmt, rustfmt, etc.)
- Follow language-specific naming conventions
- Write self-documenting code with meaningful names
- Keep functions small and focused
- Maintain high test coverage

## Workflow
1. **Spec First**: Every feature starts with a specification in `/specs/`
2. **TDD Cycle**: Red → Green → Refactor
3. **Documentation**: Update relevant docs with every change
4. **Small Commits**: Make atomic commits with descriptive messages
5. **Code Review**: All changes require review before merging

## Commit Message Format
All commit messages must start with one of these prefixes:
- `Add:` - New features or files
- `Update:` - Changes to existing functionality
- `Fix:` - Bug fixes
- `Refactor:` - Code improvements without functional changes
- `Remove:` - Deleting code or files
- `Docs:` - Documentation changes
- `Spec:` - Specification updates

Example: `Add: user authentication endpoint with JWT tokens`

## Testing Requirements
- All new code must include tests
- Tests should be readable and maintainable
- Use the project's established testing framework
- Aim for >80% code coverage
- Test both happy paths and error conditions

## Code Review Checklist
- [ ] Follows coding standards
- [ ] Includes adequate tests
- [ ] Updates relevant documentation
- [ ] Follows the AI contract rules
- [ ] Has clear commit messages
- [ ] Doesn't break existing functionality