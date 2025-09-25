"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cms.models import Base, User, Article, Category


@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create database session for tests."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_user(session):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User",
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_category(session):
    """Create a sample category for testing."""
    category = Category(
        name="Technology",
        slug="technology",
        description="Technology related articles",
        is_active=True
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.fixture
def sample_article(session, sample_user, sample_category):
    """Create a sample article for testing."""
    article = Article(
        title="Test Article",
        slug="test-article",
        content="This is a test article content.",
        excerpt="Test excerpt",
        author_id=sample_user.id,
        category_id=sample_category.id,
        is_published=True
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    return article