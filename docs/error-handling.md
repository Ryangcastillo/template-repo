# Error Handling Guidelines

## Principles
- **Centralized Error Handling**: Use consistent error handling patterns across the codebase
- **Meaningful Error Messages**: Provide clear, actionable error messages
- **Proper Logging**: Log errors with appropriate context
- **Graceful Degradation**: Handle errors without crashing the application

## Error Categories
1. **Validation Errors**: Input validation failures
2. **Business Logic Errors**: Domain-specific rule violations  
3. **System Errors**: Database, network, file system failures
4. **Security Errors**: Authentication, authorization failures

## Language-Specific Patterns

### Node.js
```javascript
try {
  // risky operation
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new ApplicationError('User-friendly message', error);
}
```

### Python
```python
try:
    # risky operation
except SpecificException as e:
    logger.error(f"Operation failed: {e}", extra={"context": context})
    raise ApplicationError("User-friendly message") from e
```

### Go
```go
if err != nil {
    log.Error().Err(err).Str("context", context).Msg("Operation failed")
    return fmt.Errorf("user-friendly message: %w", err)
}
```

## Best Practices
- Always log errors with sufficient context
- Use structured logging when possible
- Don't expose internal error details to end users
- Implement proper error recovery mechanisms
- Test error paths as thoroughly as success paths