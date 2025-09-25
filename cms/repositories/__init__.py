"""
Repository pattern implementation for data access.

This module provides a consistent interface for database operations
following the repository pattern for better testability and separation of concerns.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from cms.models import Base, User, Article, Category
from cms.exceptions import DatabaseError, ValidationError


T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T], ABC):
    """Abstract base repository providing common database operations."""
    
    def __init__(self, db: Session, model_class: Type[T]):
        self.db = db
        self.model_class = model_class
    
    def create(self, **kwargs) -> T:
        """Create a new entity."""
        try:
            entity = self.model_class(**kwargs)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except IntegrityError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create {self.model_class.__name__}", details={"error": str(e)})
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        return self.db.query(self.model_class).filter(self.model_class.id == entity_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        return self.db.query(self.model_class).offset(skip).limit(limit).all()
    
    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Update entity by ID."""
        try:
            entity = self.get_by_id(entity_id)
            if not entity:
                return None
            
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except IntegrityError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update {self.model_class.__name__}", details={"error": str(e)})
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID."""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        
        self.db.delete(entity)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Count total entities."""
        return self.db.query(self.model_class).count()


class UserRepository(BaseRepository[User]):
    """Repository for User entity operations."""
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.db.query(User).filter(User.email == email.lower()).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return self.db.query(User).filter(User.email == email.lower()).first() is not None
    
    def username_exists(self, username: str) -> bool:
        """Check if username already exists."""
        return self.db.query(User).filter(User.username == username).first() is not None
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users only."""
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_user(self, email: str, username: str, password_hash: str, **kwargs) -> User:
        """Create a new user with validation."""
        # Check for existing email or username
        if self.email_exists(email):
            raise ValidationError("Email address already exists")
        
        if self.username_exists(username):
            raise ValidationError("Username already exists")
        
        return self.create(
            email=email.lower(),
            username=username,
            password_hash=password_hash,
            **kwargs
        )


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entity operations."""
    
    def __init__(self, db: Session):
        super().__init__(db, Category)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug."""
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def get_active_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Get active categories only."""
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if slug already exists."""
        query = self.db.query(Category).filter(Category.slug == slug)
        if exclude_id:
            query = query.filter(Category.id != exclude_id)
        return query.first() is not None


class ArticleRepository(BaseRepository[Article]):
    """Repository for Article entity operations."""
    
    def __init__(self, db: Session):
        super().__init__(db, Article)
    
    def get_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug."""
        return self.db.query(Article).filter(Article.slug == slug).first()
    
    def get_published_articles(self, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get published articles only."""
        return (
            self.db.query(Article)
            .filter(Article.is_published == True)
            .order_by(Article.published_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get articles by author."""
        return (
            self.db.query(Article)
            .filter(Article.author_id == author_id)
            .order_by(Article.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get articles by category."""
        return (
            self.db.query(Article)
            .filter(Article.category_id == category_id)
            .filter(Article.is_published == True)
            .order_by(Article.published_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if slug already exists."""
        query = self.db.query(Article).filter(Article.slug == slug)
        if exclude_id:
            query = query.filter(Article.id != exclude_id)
        return query.first() is not None
    
    def search_articles(self, query: str, skip: int = 0, limit: int = 100) -> List[Article]:
        """Search articles by title and content."""
        return (
            self.db.query(Article)
            .filter(
                (Article.title.contains(query)) | 
                (Article.content.contains(query))
            )
            .filter(Article.is_published == True)
            .order_by(Article.published_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )