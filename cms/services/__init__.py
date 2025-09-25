"""
Business logic services for the CMS application.

This module implements the business logic layer, handling complex operations
and coordinating between repositories and external services.
"""

import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from cms.models import User, Article, Category
from cms.repositories import UserRepository, ArticleRepository, CategoryRepository
from cms.validators.input_validator import ValidationHelper
from cms.utils.error_manager import error_manager, ErrorSeverity
from cms.exceptions import (
    ValidationError, AuthenticationError, BusinessLogicError, 
    SecurityException, DatabaseError
)


class AuthenticationService:
    """Service for handling user authentication and authorization."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new user with validation.
        
        Args:
            user_data: Dictionary containing user registration data
            
        Returns:
            Dictionary with success status and user information
            
        Raises:
            ValidationError: When input data is invalid
            DatabaseError: When database operation fails
        """
        try:
            # Validate input data
            validated_data = ValidationHelper.validate_user_registration(user_data)
            
            # Hash password
            password_hash = self._hash_password(validated_data['password'])
            
            # Create user
            user = self.user_repo.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password_hash=password_hash,
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name
                },
                "message": "User registered successfully"
            }
            
        except (ValidationError, DatabaseError) as e:
            error_response = error_manager.handle_error(
                e, ErrorSeverity.MEDIUM, 
                context={"operation": "user_registration"},
                user_message="Registration failed. Please check your input."
            )
            raise ValidationError(error_response["message"], details=error_response)
    
    def authenticate_user(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate user with email and password.
        
        Args:
            login_data: Dictionary containing email and password
            
        Returns:
            Dictionary with authentication result and user information
            
        Raises:
            AuthenticationError: When authentication fails
        """
        try:
            # Validate input data
            validated_data = ValidationHelper.validate_user_login(login_data)
            
            # Get user by email
            user = self.user_repo.get_by_email(validated_data['email'])
            if not user:
                raise AuthenticationError("Invalid email or password")
            
            # Check if user is active
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # Verify password
            if not self._verify_password(validated_data['password'], user.password_hash):
                raise AuthenticationError("Invalid email or password")
            
            # Update last login
            self.user_repo.update(user.id, last_login=datetime.utcnow())
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser
                },
                "message": "Authentication successful"
            }
            
        except AuthenticationError as e:
            error_response = error_manager.handle_error(
                e, ErrorSeverity.MEDIUM,
                context={"operation": "user_authentication", "email": login_data.get('email')},
                user_message="Authentication failed. Please check your credentials."
            )
            raise AuthenticationError(error_response["message"], details=error_response)
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password with current password verification.
        
        Args:
            user_id: ID of the user
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            Dictionary with operation result
            
        Raises:
            AuthenticationError: When current password is invalid
            ValidationError: When new password doesn't meet requirements
        """
        # Get user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found")
        
        # Verify current password
        if not self._verify_password(current_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        
        # Validate new password
        from cms.validators.input_validator import InputValidator
        if not InputValidator.validate_password(new_password):
            raise ValidationError("New password doesn't meet requirements")
        
        # Hash and update password
        new_password_hash = self._hash_password(new_password)
        self.user_repo.update(user_id, password_hash=new_password_hash)
        
        return {
            "success": True,
            "message": "Password changed successfully"
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class ArticleService:
    """Service for handling article operations."""
    
    def __init__(self, article_repo: ArticleRepository, category_repo: CategoryRepository):
        self.article_repo = article_repo
        self.category_repo = category_repo
    
    def create_article(self, article_data: Dict[str, Any], author_id: int) -> Dict[str, Any]:
        """Create a new article.
        
        Args:
            article_data: Dictionary containing article data
            author_id: ID of the author
            
        Returns:
            Dictionary with success status and article information
        """
        try:
            # Validate required fields
            if not article_data.get('title'):
                raise ValidationError("Title is required")
            
            if not article_data.get('content'):
                raise ValidationError("Content is required")
            
            # Generate slug from title
            slug = self._generate_slug(article_data['title'])
            
            # Ensure slug is unique
            original_slug = slug
            counter = 1
            while self.article_repo.slug_exists(slug):
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Validate category if provided
            category_id = article_data.get('category_id')
            if category_id:
                category = self.category_repo.get_by_id(category_id)
                if not category or not category.is_active:
                    raise ValidationError("Invalid category selected")
            
            # Sanitize content
            from cms.validators.input_validator import InputValidator
            sanitized_content = InputValidator.sanitize_html(article_data['content'])
            
            # Create article
            article = self.article_repo.create(
                title=article_data['title'].strip(),
                slug=slug,
                content=sanitized_content,
                excerpt=article_data.get('excerpt', '').strip() or None,
                author_id=author_id,
                category_id=category_id,
                is_published=article_data.get('is_published', False)
            )
            
            # Set published_at if publishing
            if article.is_published:
                article.publish()
                self.article_repo.db.commit()
            
            return {
                "success": True,
                "article": {
                    "id": article.id,
                    "title": article.title,
                    "slug": article.slug,
                    "is_published": article.is_published,
                    "created_at": article.created_at.isoformat()
                },
                "message": "Article created successfully"
            }
            
        except (ValidationError, DatabaseError) as e:
            error_response = error_manager.handle_error(
                e, ErrorSeverity.MEDIUM,
                context={"operation": "article_creation", "author_id": author_id}
            )
            raise ValidationError(error_response["message"], details=error_response)
    
    def update_article(self, article_id: int, article_data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Update an existing article.
        
        Args:
            article_id: ID of the article to update
            article_data: Dictionary containing updated article data
            user_id: ID of the user making the update
            
        Returns:
            Dictionary with success status and updated article information
        """
        # Get article
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise BusinessLogicError("Article not found")
        
        # Check permissions (user must be author or staff)
        from cms.repositories import UserRepository
        user_repo = UserRepository(self.article_repo.db)
        user = user_repo.get_by_id(user_id)
        
        if not (user and (article.author_id == user_id or user.is_staff)):
            raise BusinessLogicError("You don't have permission to edit this article")
        
        # Prepare update data
        update_data = {}
        
        if 'title' in article_data:
            update_data['title'] = article_data['title'].strip()
            
            # Update slug if title changed
            if update_data['title'] != article.title:
                new_slug = self._generate_slug(update_data['title'])
                original_slug = new_slug
                counter = 1
                while self.article_repo.slug_exists(new_slug, exclude_id=article_id):
                    new_slug = f"{original_slug}-{counter}"
                    counter += 1
                update_data['slug'] = new_slug
        
        if 'content' in article_data:
            from cms.validators.input_validator import InputValidator
            update_data['content'] = InputValidator.sanitize_html(article_data['content'])
        
        if 'excerpt' in article_data:
            update_data['excerpt'] = article_data['excerpt'].strip() or None
        
        if 'category_id' in article_data:
            category_id = article_data['category_id']
            if category_id:
                category = self.category_repo.get_by_id(category_id)
                if not category or not category.is_active:
                    raise ValidationError("Invalid category selected")
            update_data['category_id'] = category_id
        
        if 'is_published' in article_data:
            is_published = bool(article_data['is_published'])
            update_data['is_published'] = is_published
            
            # Set/unset published_at
            if is_published and not article.is_published:
                update_data['published_at'] = datetime.utcnow()
            elif not is_published and article.is_published:
                update_data['published_at'] = None
        
        # Update article
        updated_article = self.article_repo.update(article_id, **update_data)
        
        return {
            "success": True,
            "article": {
                "id": updated_article.id,
                "title": updated_article.title,
                "slug": updated_article.slug,
                "is_published": updated_article.is_published,
                "updated_at": updated_article.updated_at.isoformat()
            },
            "message": "Article updated successfully"
        }
    
    def delete_article(self, article_id: int, user_id: int) -> Dict[str, Any]:
        """Delete an article.
        
        Args:
            article_id: ID of the article to delete
            user_id: ID of the user requesting deletion
            
        Returns:
            Dictionary with success status
        """
        # Get article
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise BusinessLogicError("Article not found")
        
        # Check permissions
        from cms.repositories import UserRepository
        user_repo = UserRepository(self.article_repo.db)
        user = user_repo.get_by_id(user_id)
        
        if not (user and (article.author_id == user_id or user.is_staff)):
            raise BusinessLogicError("You don't have permission to delete this article")
        
        # Delete article
        self.article_repo.delete(article_id)
        
        return {
            "success": True,
            "message": "Article deleted successfully"
        }
    
    def get_articles(self, published_only: bool = True, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get articles with pagination.
        
        Args:
            published_only: Whether to return only published articles
            skip: Number of articles to skip
            limit: Maximum number of articles to return
            
        Returns:
            Dictionary with articles list and pagination info
        """
        if published_only:
            articles = self.article_repo.get_published_articles(skip=skip, limit=limit)
            total = self.article_repo.db.query(self.article_repo.model_class).filter(
                self.article_repo.model_class.is_published == True
            ).count()
        else:
            articles = self.article_repo.get_all(skip=skip, limit=limit)
            total = self.article_repo.count()
        
        return {
            "articles": [
                {
                    "id": article.id,
                    "title": article.title,
                    "slug": article.slug,
                    "excerpt": article.excerpt,
                    "author": article.author.display_name,
                    "category": article.category.name if article.category else None,
                    "is_published": article.is_published,
                    "published_at": article.published_at.isoformat() if article.published_at else None,
                    "created_at": article.created_at.isoformat()
                }
                for article in articles
            ],
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total,
                "has_next": skip + limit < total
            }
        }
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        import re
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
        slug = re.sub(r'[-\s]+', '-', slug)   # Replace spaces/hyphens with single hyphen
        slug = slug.strip('-')                # Remove leading/trailing hyphens
        return slug[:100]  # Limit length


class CategoryService:
    """Service for handling category operations."""
    
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category.
        
        Args:
            category_data: Dictionary containing category data
            
        Returns:
            Dictionary with success status and category information
        """
        try:
            # Validate required fields
            if not category_data.get('name'):
                raise ValidationError("Category name is required")
            
            # Generate slug from name
            slug = self._generate_slug(category_data['name'])
            
            # Ensure slug is unique
            original_slug = slug
            counter = 1
            while self.category_repo.slug_exists(slug):
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Create category
            category = self.category_repo.create(
                name=category_data['name'].strip(),
                slug=slug,
                description=category_data.get('description', '').strip() or None,
                is_active=category_data.get('is_active', True)
            )
            
            return {
                "success": True,
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug,
                    "description": category.description,
                    "is_active": category.is_active
                },
                "message": "Category created successfully"
            }
            
        except (ValidationError, DatabaseError) as e:
            error_response = error_manager.handle_error(
                e, ErrorSeverity.MEDIUM,
                context={"operation": "category_creation"}
            )
            raise ValidationError(error_response["message"], details=error_response)
    
    def get_categories(self, active_only: bool = True, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get categories with pagination.
        
        Args:
            active_only: Whether to return only active categories
            skip: Number of categories to skip
            limit: Maximum number of categories to return
            
        Returns:
            Dictionary with categories list and pagination info
        """
        if active_only:
            categories = self.category_repo.get_active_categories(skip=skip, limit=limit)
            total = self.category_repo.db.query(self.category_repo.model_class).filter(
                self.category_repo.model_class.is_active == True
            ).count()
        else:
            categories = self.category_repo.get_all(skip=skip, limit=limit)
            total = self.category_repo.count()
        
        return {
            "categories": [
                {
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug,
                    "description": category.description,
                    "is_active": category.is_active,
                    "created_at": category.created_at.isoformat()
                }
                for category in categories
            ],
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total,
                "has_next": skip + limit < total
            }
        }
    
    def _generate_slug(self, name: str) -> str:
        """Generate URL-friendly slug from name."""
        import re
        slug = name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        return slug[:100]