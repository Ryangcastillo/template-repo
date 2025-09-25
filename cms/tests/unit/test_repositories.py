"""Unit tests for repositories."""

import pytest
from cms.repositories import UserRepository, ArticleRepository, CategoryRepository
from cms.models import User, Article, Category
from cms.exceptions import DatabaseError, ValidationError


class TestUserRepository:
    """Test suite for UserRepository class."""
    
    def setup_method(self):
        """Setup for each test method."""
        # Repository will be initialized with session fixture in tests
        pass
    
    def test_create_user_with_valid_data(self, session):
        """Test creating user with valid data."""
        # Arrange
        repo = UserRepository(session)
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "password_hash": "hashed_password",
            "first_name": "New",
            "last_name": "User"
        }
        
        # Act
        user = repo.create(**user_data)
        
        # Assert
        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.username == "newuser"
        assert user.password_hash == "hashed_password"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.is_active is True
        assert user.created_at is not None
    
    def test_get_by_email_existing_user(self, session, sample_user):
        """Test getting user by email address."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        user = repo.get_by_email("test@example.com")
        
        # Assert
        assert user is not None
        assert user.email == "test@example.com"
        assert user.id == sample_user.id
    
    def test_get_by_email_nonexistent_user(self, session):
        """Test getting user by non-existent email."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        user = repo.get_by_email("nonexistent@example.com")
        
        # Assert
        assert user is None
    
    def test_get_by_username_existing_user(self, session, sample_user):
        """Test getting user by username."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        user = repo.get_by_username("testuser")
        
        # Assert
        assert user is not None
        assert user.username == "testuser"
        assert user.id == sample_user.id
    
    def test_email_exists_returns_true_for_existing_email(self, session, sample_user):
        """Test email_exists returns True for existing email."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        exists = repo.email_exists("test@example.com")
        
        # Assert
        assert exists is True
    
    def test_email_exists_returns_false_for_nonexistent_email(self, session):
        """Test email_exists returns False for non-existent email."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        exists = repo.email_exists("nonexistent@example.com")
        
        # Assert
        assert exists is False
    
    def test_username_exists_returns_true_for_existing_username(self, session, sample_user):
        """Test username_exists returns True for existing username."""
        # Arrange
        repo = UserRepository(session)
        
        # Act
        exists = repo.username_exists("testuser")
        
        # Assert
        assert exists is True
    
    def test_create_user_with_duplicate_email_raises_validation_error(self, session, sample_user):
        """Test creating user with duplicate email raises ValidationError."""
        # Arrange
        repo = UserRepository(session)
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            repo.create_user(
                email="test@example.com",  # duplicate email
                username="newuser",
                password_hash="hashed_password"
            )
        
        assert "Email address already exists" in str(exc_info.value)
    
    def test_create_user_with_duplicate_username_raises_validation_error(self, session, sample_user):
        """Test creating user with duplicate username raises ValidationError."""
        # Arrange
        repo = UserRepository(session)
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            repo.create_user(
                email="new@example.com",
                username="testuser",  # duplicate username
                password_hash="hashed_password"
            )
        
        assert "Username already exists" in str(exc_info.value)
    
    def test_get_active_users_returns_only_active_users(self, session):
        """Test get_active_users returns only active users."""
        # Arrange
        repo = UserRepository(session)
        
        # Create active and inactive users
        active_user = User(
            email="active@example.com",
            username="activeuser",
            password_hash="hash",
            is_active=True
        )
        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser",
            password_hash="hash",
            is_active=False
        )
        session.add_all([active_user, inactive_user])
        session.commit()
        
        # Act
        active_users = repo.get_active_users()
        
        # Assert
        active_emails = [user.email for user in active_users]
        assert "active@example.com" in active_emails
        assert "inactive@example.com" not in active_emails


class TestArticleRepository:
    """Test suite for ArticleRepository class."""
    
    def test_create_article_with_valid_data(self, session, sample_user, sample_category):
        """Test creating article with valid data."""
        # Arrange
        repo = ArticleRepository(session)
        article_data = {
            "title": "New Article",
            "slug": "new-article",
            "content": "Article content here.",
            "author_id": sample_user.id,
            "category_id": sample_category.id,
            "is_published": True
        }
        
        # Act
        article = repo.create(**article_data)
        
        # Assert
        assert article.id is not None
        assert article.title == "New Article"
        assert article.slug == "new-article"
        assert article.content == "Article content here."
        assert article.author_id == sample_user.id
        assert article.category_id == sample_category.id
        assert article.is_published is True
    
    def test_get_by_slug_existing_article(self, session, sample_article):
        """Test getting article by slug."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Act
        article = repo.get_by_slug("test-article")
        
        # Assert
        assert article is not None
        assert article.slug == "test-article"
        assert article.id == sample_article.id
    
    def test_get_published_articles_returns_only_published(self, session, sample_user, sample_category):
        """Test get_published_articles returns only published articles."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Create published and unpublished articles
        published_article = Article(
            title="Published Article",
            slug="published-article",
            content="Content",
            author_id=sample_user.id,
            category_id=sample_category.id,
            is_published=True
        )
        draft_article = Article(
            title="Draft Article",
            slug="draft-article",
            content="Content",
            author_id=sample_user.id,
            category_id=sample_category.id,
            is_published=False
        )
        session.add_all([published_article, draft_article])
        session.commit()
        
        # Act
        published_articles = repo.get_published_articles()
        
        # Assert
        published_titles = [article.title for article in published_articles]
        assert "Published Article" in published_titles
        assert "Draft Article" not in published_titles
    
    def test_get_by_author_returns_articles_by_specific_author(self, session, sample_article):
        """Test get_by_author returns articles by specific author."""
        # Arrange
        repo = ArticleRepository(session)
        author_id = sample_article.author_id
        
        # Act
        articles = repo.get_by_author(author_id)
        
        # Assert
        assert len(articles) > 0
        for article in articles:
            assert article.author_id == author_id
    
    def test_slug_exists_returns_true_for_existing_slug(self, session, sample_article):
        """Test slug_exists returns True for existing slug."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Act
        exists = repo.slug_exists("test-article")
        
        # Assert
        assert exists is True
    
    def test_slug_exists_returns_false_for_nonexistent_slug(self, session):
        """Test slug_exists returns False for non-existent slug."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Act
        exists = repo.slug_exists("nonexistent-slug")
        
        # Assert
        assert exists is False
    
    def test_slug_exists_with_exclude_id(self, session, sample_article):
        """Test slug_exists with exclude_id parameter."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Act
        exists = repo.slug_exists("test-article", exclude_id=sample_article.id)
        
        # Assert
        assert exists is False  # Should be False because we excluded the existing article
    
    def test_search_articles_finds_by_title(self, session, sample_user, sample_category):
        """Test search_articles finds articles by title."""
        # Arrange
        repo = ArticleRepository(session)
        
        # Create searchable article
        searchable_article = Article(
            title="Python Programming Guide",
            slug="python-guide",
            content="Learn Python basics",
            author_id=sample_user.id,
            category_id=sample_category.id,
            is_published=True
        )
        session.add(searchable_article)
        session.commit()
        
        # Act
        results = repo.search_articles("Python")
        
        # Assert
        assert len(results) > 0
        found_titles = [article.title for article in results]
        assert "Python Programming Guide" in found_titles


class TestCategoryRepository:
    """Test suite for CategoryRepository class."""
    
    def test_create_category_with_valid_data(self, session):
        """Test creating category with valid data."""
        # Arrange
        repo = CategoryRepository(session)
        category_data = {
            "name": "Science",
            "slug": "science",
            "description": "Science related articles",
            "is_active": True
        }
        
        # Act
        category = repo.create(**category_data)
        
        # Assert
        assert category.id is not None
        assert category.name == "Science"
        assert category.slug == "science"
        assert category.description == "Science related articles"
        assert category.is_active is True
    
    def test_get_by_slug_existing_category(self, session, sample_category):
        """Test getting category by slug."""
        # Arrange
        repo = CategoryRepository(session)
        
        # Act
        category = repo.get_by_slug("technology")
        
        # Assert
        assert category is not None
        assert category.slug == "technology"
        assert category.id == sample_category.id
    
    def test_get_active_categories_returns_only_active(self, session):
        """Test get_active_categories returns only active categories."""
        # Arrange
        repo = CategoryRepository(session)
        
        # Create active and inactive categories
        active_category = Category(
            name="Active Category",
            slug="active-category",
            is_active=True
        )
        inactive_category = Category(
            name="Inactive Category",
            slug="inactive-category",
            is_active=False
        )
        session.add_all([active_category, inactive_category])
        session.commit()
        
        # Act
        active_categories = repo.get_active_categories()
        
        # Assert
        active_names = [category.name for category in active_categories]
        assert "Active Category" in active_names
        assert "Inactive Category" not in active_names