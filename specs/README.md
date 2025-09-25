# Specs Folder

This folder is managed by **Spec Kit**.

Every new feature must follow the Spec Kit flow:  
1. `/constitution` → set project principles  
2. `/specify` → define the what/why  
3. `/plan` → define the how (tech choices)  
4. `/tasks` → break into atomic steps  
5. `/implement` → code based on the plan  

All specs must live here.

## Spec Kit Workflow

### 1. Constitution Phase
Create or reference the project constitution that defines:
- Core principles and values
- Technical standards and constraints
- Decision-making processes
- Quality gates and requirements

### 2. Specify Phase
For each new feature, create a specification that includes:
- **Problem Statement**: What problem are we solving?
- **User Stories**: Who benefits and how?
- **Success Criteria**: How do we measure success?
- **Constraints**: What limitations must we work within?

### 3. Plan Phase
Develop a technical implementation plan covering:
- **Architecture**: How does it fit into existing systems?
- **Technologies**: What tools and libraries will be used?
- **Dependencies**: What other components are required?
- **Risks**: What could go wrong and how to mitigate?

### 4. Tasks Phase
Break down the implementation into atomic, testable tasks:
- Each task should be completable in 1-4 hours
- Tasks should have clear acceptance criteria
- Dependencies between tasks should be explicit
- Tasks should include testing requirements

### 5. Implement Phase
Execute the tasks with continuous validation:
- Follow Test-Driven Development (TDD)
- Implement one task at a time
- Validate against specification at each step
- Update documentation as you go

## Spec Template

When creating new specifications, use this template:

```markdown
# Spec: [Feature Name]

## Constitution Reference
- Links to relevant constitutional principles
- Applicable technical standards
- Quality requirements

## Specification
### Problem Statement
[What problem does this solve?]

### User Stories
- As a [user type], I want [functionality] so that [benefit]
- As a [user type], I want [functionality] so that [benefit]

### Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

### Constraints
- [Technical constraint 1]
- [Business constraint 1]
- [Resource constraint 1]

## Technical Plan
### Architecture
[How does this fit into the existing system?]

### Technologies
- [Technology 1]: [Justification]
- [Technology 2]: [Justification]

### Dependencies
- [Internal dependency 1]
- [External dependency 1]

### Risks and Mitigations
- Risk: [Risk description]
  - Mitigation: [How to address]
- Risk: [Risk description]
  - Mitigation: [How to address]

## Task Breakdown
- [ ] Task 1: [Description with acceptance criteria]
- [ ] Task 2: [Description with acceptance criteria]
- [ ] Task 3: [Description with acceptance criteria]

## Implementation Notes
[Any additional implementation guidance]

## Testing Strategy
[How will this feature be tested?]

## Documentation Requirements
[What documentation needs to be created/updated?]
```

## Directory Structure

Organize specs using this structure:

```
specs/
├── constitution.md           # Project constitution
├── features/
│   ├── user-authentication.md
│   ├── data-processing.md
│   └── api-integration.md
├── architecture/
│   ├── database-design.md
│   ├── api-design.md
│   └── security-model.md
└── infrastructure/
    ├── deployment.md
    ├── monitoring.md
    └── scaling.md
```

## Integration with Development Process

Specs integrate with the development workflow:

1. **Before Development**: Every feature must have an approved spec
2. **During Development**: Implementation must follow the spec exactly
3. **During Code Review**: Reviewers check compliance with spec
4. **After Development**: Update spec with any deviations or learnings

## AI Agent Compliance

AI agents working on this repository must:

1. **Always create specs** before implementing new features
2. **Follow the Spec Kit workflow** exactly as defined
3. **Reference existing specs** when making related changes
4. **Update specs** when implementation deviates from plan
5. **Validate implementation** against specification requirements

This ensures all development is purposeful, well-planned, and properly documented.