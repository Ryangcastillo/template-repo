# Security Guidelines

## Security Principles

### Defense in Depth

Implement multiple layers of security controls:

1. **Network Security**: Firewalls, VPNs, network segmentation
2. **Application Security**: Input validation, authentication, authorization
3. **Data Security**: Encryption at rest and in transit
4. **Infrastructure Security**: Secure configurations, monitoring
5. **Operational Security**: Access controls, audit logging

### Zero Trust Architecture

- **Never trust, always verify**: Authenticate and authorize every request
- **Principle of least privilege**: Grant minimum necessary permissions
- **Assume breach**: Design systems expecting security compromises

## Authentication & Authorization

### JWT Token Security

```python
# src/auth/jwt_handler.py
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import secrets

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = timedelta(hours=24)
    
    def generate_token(self, user_id: str, roles: list = None) -> str:
        """Generate JWT token with secure claims"""
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + self.token_expiry,
            "jti": secrets.token_urlsafe(16),  # Unique token ID
            "roles": roles or []
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
```

### Password Security

```python
# src/auth/password.py
import bcrypt
import secrets
from typing import str

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt with random salt"""
        salt = bcrypt.gensalt(rounds=12)  # CPU cost factor
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate cryptographically secure random password"""
        return secrets.token_urlsafe(length)
```

## Input Validation & Sanitization

### SQL Injection Prevention

```python
# src/database/queries.py
from sqlalchemy import text
from typing import List, Dict, Any

class SecureQueries:
    def __init__(self, session):
        self.session = session
    
    def get_user_by_id(self, user_id: str) -> Dict:
        """Secure parameterized query"""
        # Good: Parameterized query
        query = text("SELECT * FROM users WHERE id = :user_id")
        result = self.session.execute(query, {"user_id": user_id})
        return result.fetchone()
    
    def search_users(self, search_term: str) -> List[Dict]:
        """Secure search with input sanitization"""
        # Sanitize input
        sanitized_term = search_term.replace("'", "").replace(";", "")
        
        # Use parameterized query
        query = text("SELECT id, name, email FROM users WHERE name LIKE :term")
        result = self.session.execute(query, {"term": f"%{sanitized_term}%"})
        return result.fetchall()
```

### XSS Prevention

```python
# src/utils/sanitizers.py
import html
import re
from typing import str

class InputSanitizer:
    @staticmethod
    def sanitize_html(input_text: str) -> str:
        """Remove/escape HTML to prevent XSS"""
        # Escape HTML characters
        escaped = html.escape(input_text)
        
        # Remove script tags completely
        escaped = re.sub(r'<script.*?</script>', '', escaped, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove javascript: URLs
        escaped = re.sub(r'javascript:', '', escaped, flags=re.IGNORECASE)
        
        return escaped
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove directory traversal attempts
        filename = filename.replace('..', '').replace('/', '').replace('\\', '')
        
        # Remove null bytes and control characters
        filename = ''.join(char for char in filename if ord(char) > 31)
        
        # Limit length
        return filename[:255]
```

## HTTPS & TLS Configuration

### FastAPI HTTPS Setup

```python
# src/main.py
from fastapi import FastAPI, HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Force HTTPS in production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Never use "*" in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Security Headers

```python
# src/middleware/security_headers.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response
```

## Data Protection

### Encryption at Rest

```python
# src/utils/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class DataEncryption:
    def __init__(self, password: bytes):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data).decode()
```

### Secure Data Storage

```python
# src/models/secure_user.py
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from .encryption import DataEncryption

Base = declarative_base()

class SecureUser(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    encrypted_pii = Column(Text)  # Encrypted personally identifiable information
    
    def set_pii(self, pii_data: dict, encryption_key: bytes):
        """Store PII data encrypted"""
        encryptor = DataEncryption(encryption_key)
        self.encrypted_pii = encryptor.encrypt(json.dumps(pii_data))
    
    def get_pii(self, encryption_key: bytes) -> dict:
        """Retrieve PII data decrypted"""
        if not self.encrypted_pii:
            return {}
        
        encryptor = DataEncryption(encryption_key)
        decrypted_data = encryptor.decrypt(self.encrypted_pii.encode())
        return json.loads(decrypted_data)
```

## API Security

### Rate Limiting

```python
# src/middleware/rate_limiter.py
import time
from typing import Dict
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 3600):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        if client_ip in self.clients:
            self.clients[client_ip] = [
                req_time for req_time in self.clients[client_ip] 
                if now - req_time < self.period
            ]
        else:
            self.clients[client_ip] = []
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Add current request
        self.clients[client_ip].append(now)
        
        response = await call_next(request)
        return response
```

### Input Validation Middleware

```python
# src/middleware/input_validation.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import json

class InputValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            # Check content length
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 1024 * 1024:  # 1MB limit
                raise HTTPException(status_code=413, detail="Request too large")
            
            # Validate JSON structure
            if "application/json" in request.headers.get("content-type", ""):
                try:
                    body = await request.body()
                    if body:
                        json.loads(body.decode())
                except json.JSONDecodeError:
                    raise HTTPException(status_code=400, detail="Invalid JSON")
        
        response = await call_next(request)
        return response
```

## Security Monitoring

### Audit Logging

```python
# src/utils/audit_logger.py
import logging
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit")
        handler = logging.FileHandler("audit.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_authentication(self, user_id: str, success: bool, ip_address: str):
        """Log authentication attempts"""
        status = "SUCCESS" if success else "FAILURE"
        self.logger.info(
            f"AUTH_{status}: user={user_id}, ip={ip_address}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )
    
    def log_data_access(self, user_id: str, resource: str, action: str, ip_address: str):
        """Log data access events"""
        self.logger.info(
            f"DATA_ACCESS: user={user_id}, resource={resource}, "
            f"action={action}, ip={ip_address}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        self.logger.warning(
            f"SECURITY_EVENT: type={event_type}, "
            f"details={json.dumps(details)}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )
```

## Security Checklist

### Pre-Deployment Security Review

- [ ] All inputs validated and sanitized
- [ ] SQL injection protection implemented
- [ ] XSS protection in place
- [ ] HTTPS/TLS properly configured
- [ ] Authentication and authorization working
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Sensitive data encrypted
- [ ] Audit logging implemented
- [ ] Dependencies updated and scanned
- [ ] Error messages don't leak information
- [ ] File upload restrictions in place
- [ ] Session management secure
- [ ] CORS properly configured

### Regular Security Maintenance

- [ ] Weekly dependency updates
- [ ] Monthly security scans
- [ ] Quarterly penetration testing
- [ ] Annual security audit
- [ ] Regular log review
- [ ] Access control review
- [ ] Certificate renewal monitoring

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Python Security Guidelines](https://python.org/dev/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)