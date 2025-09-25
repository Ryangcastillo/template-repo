# Security Guidelines

## Security Principles

### Defense in Depth
Implement multiple layers of security controls:
1. **Input Validation**: Validate all inputs at entry points
2. **Output Encoding**: Encode all outputs to prevent XSS
3. **Authentication**: Strong user authentication
4. **Authorization**: Proper access controls
5. **Secure Communication**: HTTPS everywhere
6. **Logging & Monitoring**: Track security events

## Input Validation

### Validation Strategy

```python
from typing import Any, Dict
import re
from marshmallow import Schema, fields, validate, ValidationError

class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    
    email = fields.Email(required=True)
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=30),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Username contains invalid characters")
        ]
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                error="Password must contain uppercase, lowercase, number, and special character"
            )
        ]
    )

class InputValidator:
    """Centralized input validation."""
    
    @staticmethod
    def validate_user_registration(data: Dict[str, Any]) -> Dict[str, Any]:
        schema = UserRegistrationSchema()
        try:
            return schema.load(data)
        except ValidationError as e:
            raise SecurityException("Invalid input data", errors=e.messages)
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """Remove dangerous HTML tags and attributes."""
        import bleach
        
        allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
        allowed_attributes = {}
        
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)
```

## SQL Injection Prevention

### Use Parameterized Queries

```python
# ❌ NEVER do this - SQL injection vulnerability
def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# ✅ Always use parameterized queries
def get_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE id = %s"
    return db.execute(query, (user_id,))

# ✅ Using ORM (preferred)
def get_user_by_id(user_id: int):
    return User.objects.get(id=user_id)
```

### Repository Pattern with Security

```python
from typing import Optional, List
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email using parameterized query."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user_data: Dict[str, Any]) -> User:
        """Create user with validated data."""
        # Data should already be validated by service layer
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

## Authentication & Authorization

### JWT Authentication

```python
import jwt
from datetime import datetime, timedelta
from functools import wraps

class AuthenticationService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(hours=1)
        self.refresh_token_expire = timedelta(days=7)
    
    def create_access_token(self, user_id: int) -> str:
        """Create JWT access token."""
        payload = {
            "user_id": user_id,
            "type": "access",
            "exp": datetime.utcnow() + self.access_token_expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

# Authentication decorator
def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            raise AuthenticationError("Token required")
        
        try:
            auth_service = AuthenticationService(current_app.config['SECRET_KEY'])
            payload = auth_service.verify_token(token)
            request.current_user_id = payload['user_id']
        except AuthenticationError:
            raise
        
        return f(*args, **kwargs)
    return decorated
```

### Role-Based Access Control

```python
from enum import Enum

class Permission(Enum):
    READ_USER = "read_user"
    WRITE_USER = "write_user"
    DELETE_USER = "delete_user"
    ADMIN_ACCESS = "admin_access"

class Role(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ_USER, Permission.WRITE_USER, Permission.DELETE_USER, Permission.ADMIN_ACCESS],
    Role.EDITOR: [Permission.READ_USER, Permission.WRITE_USER],
    Role.VIEWER: [Permission.READ_USER]
}

def require_permission(permission: Permission):
    """Decorator to check user permissions."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            if not user:
                raise AuthorizationError("Authentication required")
            
            user_permissions = ROLE_PERMISSIONS.get(user.role, [])
            if permission not in user_permissions:
                raise AuthorizationError("Insufficient permissions")
            
            return f(*args, **kwargs)
        return decorated
    return decorator
```

## Password Security

### Password Hashing

```python
import bcrypt
import secrets

class PasswordService:
    """Secure password handling."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate cryptographically secure random token."""
        return secrets.token_urlsafe(length)
```

## CSRF Protection

```python
import secrets
from flask import session, request

class CSRFProtection:
    """CSRF token generation and validation."""
    
    @staticmethod
    def generate_token() -> str:
        """Generate CSRF token."""
        token = secrets.token_urlsafe(32)
        session['csrf_token'] = token
        return token
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate CSRF token."""
        expected_token = session.get('csrf_token')
        if not expected_token or not token:
            return False
        return secrets.compare_digest(expected_token, token)

def csrf_required(f):
    """Decorator to require CSRF token validation."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST':
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not CSRFProtection.validate_token(token):
                raise SecurityException("Invalid CSRF token")
        return f(*args, **kwargs)
    return decorated
```

## Security Headers

```python
from flask import Flask

def configure_security_headers(app: Flask):
    """Configure security headers for the application."""
    
    @app.after_request
    def set_security_headers(response):
        # Prevent XSS attacks
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Force HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'"
        )
        
        return response
```

## Dependency Security

### Dependency Scanning

```bash
# Install security scanners
pip install safety bandit

# Scan for known vulnerabilities
safety check

# Scan code for security issues
bandit -r cms/

# Keep dependencies updated
pip list --outdated
```

### Secure Dependency Management

```python
# requirements.txt - Pin exact versions
django==4.2.7
sqlalchemy==2.0.23
bcrypt==4.1.2
pyjwt==2.8.0

# Use hash verification (pip-tools)
pip-compile --generate-hashes requirements.in
```

## Security Monitoring

### Audit Logging

```python
import logging
from datetime import datetime

class SecurityLogger:
    """Security event logging."""
    
    def __init__(self):
        self.logger = logging.getLogger('security')
    
    def log_authentication_success(self, user_id: int, ip_address: str):
        """Log successful authentication."""
        self.logger.info(
            "Authentication success",
            extra={
                "event": "auth_success",
                "user_id": user_id,
                "ip_address": ip_address,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_authentication_failure(self, username: str, ip_address: str):
        """Log failed authentication attempt."""
        self.logger.warning(
            "Authentication failure",
            extra={
                "event": "auth_failure",
                "username": username,
                "ip_address": ip_address,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_authorization_failure(self, user_id: int, resource: str, action: str):
        """Log authorization failure."""
        self.logger.warning(
            "Authorization failure",
            extra={
                "event": "authz_failure",
                "user_id": user_id,
                "resource": resource,
                "action": action,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```