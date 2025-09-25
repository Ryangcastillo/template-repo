"""
HTTP controllers for the CMS application.

This module handles HTTP requests and coordinates between
the presentation layer and business logic services.
"""

from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session

from cms.services import AuthenticationService, ArticleService, CategoryService
from cms.repositories import UserRepository, ArticleRepository, CategoryRepository
from cms.utils.error_manager import error_manager, ErrorSeverity
from cms.exceptions import (
    ValidationError, AuthenticationError, BusinessLogicError,
    SecurityException, CMSException
)


class BaseController:
    """Base controller with common functionality."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle controller errors consistently."""
        if isinstance(error, ValidationError):
            severity = ErrorSeverity.MEDIUM
            status_code = 400
        elif isinstance(error, AuthenticationError):
            severity = ErrorSeverity.MEDIUM
            status_code = 401
        elif isinstance(error, BusinessLogicError):
            severity = ErrorSeverity.MEDIUM
            status_code = 422
        elif isinstance(error, SecurityException):
            severity = ErrorSeverity.HIGH
            status_code = 400
        else:
            severity = ErrorSeverity.HIGH
            status_code = 500
        
        error_response = error_manager.handle_error(error, severity)
        return {
            "error": error_response,
            "status_code": status_code
        }
    
    def success_response(self, data: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
        """Create consistent success response."""
        return {
            "success": True,
            "data": data,
            "status_code": status_code
        }


class AuthController(BaseController):
    """Controller for authentication endpoints."""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.user_repo = UserRepository(db)
        self.auth_service = AuthenticationService(self.user_repo)
    
    def register(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user registration.
        
        Args:
            user_data: User registration data from request
            
        Returns:
            Response dictionary with success/error status
        """
        try:
            result = self.auth_service.register_user(user_data)
            return self.success_response(result, status_code=201)
        except CMSException as e:
            return self.handle_error(e)
    
    def login(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user login.
        
        Args:
            login_data: Login credentials from request
            
        Returns:
            Response dictionary with authentication result
        """
        try:
            result = self.auth_service.authenticate_user(login_data)
            return self.success_response(result)
        except CMSException as e:
            return self.handle_error(e)
    
    def change_password(self, user_id: int, password_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle password change.
        
        Args:
            user_id: ID of the user changing password
            password_data: Current and new password data
            
        Returns:
            Response dictionary with operation result
        """
        try:
            result = self.auth_service.change_password(
                user_id,
                password_data.get('current_password', ''),
                password_data.get('new_password', '')
            )
            return self.success_response(result)
        except CMSException as e:
            return self.handle_error(e)


class ArticleController(BaseController):
    """Controller for article endpoints."""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.article_repo = ArticleRepository(db)
        self.category_repo = CategoryRepository(db)
        self.article_service = ArticleService(self.article_repo, self.category_repo)
    
    def create_article(self, article_data: Dict[str, Any], author_id: int) -> Dict[str, Any]:
        """Handle article creation.
        
        Args:
            article_data: Article data from request
            author_id: ID of the article author
            
        Returns:
            Response dictionary with creation result
        """
        try:
            result = self.article_service.create_article(article_data, author_id)
            return self.success_response(result, status_code=201)
        except CMSException as e:
            return self.handle_error(e)
    
    def update_article(self, article_id: int, article_data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Handle article update.
        
        Args:
            article_id: ID of the article to update
            article_data: Updated article data
            user_id: ID of the user making the update
            
        Returns:
            Response dictionary with update result
        """
        try:
            result = self.article_service.update_article(article_id, article_data, user_id)
            return self.success_response(result)
        except CMSException as e:
            return self.handle_error(e)
    
    def delete_article(self, article_id: int, user_id: int) -> Dict[str, Any]:
        """Handle article deletion.
        
        Args:
            article_id: ID of the article to delete
            user_id: ID of the user requesting deletion
            
        Returns:
            Response dictionary with deletion result
        """
        try:
            result = self.article_service.delete_article(article_id, user_id)
            return self.success_response(result)
        except CMSException as e:
            return self.handle_error(e)
    
    def get_articles(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting articles with pagination.
        
        Args:
            query_params: Query parameters from request
            
        Returns:
            Response dictionary with articles list
        """
        try:
            published_only = query_params.get('published_only', 'true').lower() == 'true'
            skip = int(query_params.get('skip', 0))
            limit = min(int(query_params.get('limit', 20)), 100)  # Max 100 per page
            
            result = self.article_service.get_articles(
                published_only=published_only,
                skip=skip,
                limit=limit
            )
            return self.success_response(result)
        except (ValueError, CMSException) as e:
            return self.handle_error(e)
    
    def get_article_by_slug(self, slug: str) -> Dict[str, Any]:
        """Handle getting single article by slug.
        
        Args:
            slug: Article slug
            
        Returns:
            Response dictionary with article data
        """
        try:
            article = self.article_repo.get_by_slug(slug)
            if not article:
                return {
                    "error": {"message": "Article not found"},
                    "status_code": 404
                }
            
            # Only return published articles for public access
            if not article.is_published:
                return {
                    "error": {"message": "Article not found"},
                    "status_code": 404
                }
            
            article_data = {
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "content": article.content,
                "excerpt": article.excerpt,
                "author": article.author.display_name,
                "category": article.category.name if article.category else None,
                "published_at": article.published_at.isoformat() if article.published_at else None,
                "created_at": article.created_at.isoformat(),
                "updated_at": article.updated_at.isoformat()
            }
            
            return self.success_response({"article": article_data})
        except CMSException as e:
            return self.handle_error(e)


class CategoryController(BaseController):
    """Controller for category endpoints."""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.category_repo = CategoryRepository(db)
        self.category_service = CategoryService(self.category_repo)
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle category creation.
        
        Args:
            category_data: Category data from request
            
        Returns:
            Response dictionary with creation result
        """
        try:
            result = self.category_service.create_category(category_data)
            return self.success_response(result, status_code=201)
        except CMSException as e:
            return self.handle_error(e)
    
    def get_categories(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting categories with pagination.
        
        Args:
            query_params: Query parameters from request
            
        Returns:
            Response dictionary with categories list
        """
        try:
            active_only = query_params.get('active_only', 'true').lower() == 'true'
            skip = int(query_params.get('skip', 0))
            limit = min(int(query_params.get('limit', 100)), 100)  # Max 100 per page
            
            result = self.category_service.get_categories(
                active_only=active_only,
                skip=skip,
                limit=limit
            )
            return self.success_response(result)
        except (ValueError, CMSException) as e:
            return self.handle_error(e)
    
    def get_category_by_slug(self, slug: str) -> Dict[str, Any]:
        """Handle getting single category by slug.
        
        Args:
            slug: Category slug
            
        Returns:
            Response dictionary with category data
        """
        try:
            category = self.category_repo.get_by_slug(slug)
            if not category or not category.is_active:
                return {
                    "error": {"message": "Category not found"},
                    "status_code": 404
                }
            
            category_data = {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
                "created_at": category.created_at.isoformat()
            }
            
            return self.success_response({"category": category_data})
        except CMSException as e:
            return self.handle_error(e)


# Example Flask app integration (for demonstration)
def create_cms_app(database_session: Session) -> Flask:
    """Create Flask application with CMS routes.
    
    This is an example integration showing how the controllers
    can be used with a web framework like Flask.
    """
    app = Flask(__name__)
    
    # Initialize controllers
    auth_controller = AuthController(database_session)
    article_controller = ArticleController(database_session)
    category_controller = CategoryController(database_session)
    
    # Authentication routes
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        response = auth_controller.register(request.json)
        return jsonify(response), response['status_code']
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        response = auth_controller.login(request.json)
        return jsonify(response), response['status_code']
    
    # Article routes
    @app.route('/api/articles', methods=['GET'])
    def get_articles():
        response = article_controller.get_articles(request.args.to_dict())
        return jsonify(response), response['status_code']
    
    @app.route('/api/articles', methods=['POST'])
    def create_article():
        # In real app, you'd get author_id from authentication
        author_id = request.json.get('author_id', 1)
        response = article_controller.create_article(request.json, author_id)
        return jsonify(response), response['status_code']
    
    @app.route('/api/articles/<slug>', methods=['GET'])
    def get_article(slug):
        response = article_controller.get_article_by_slug(slug)
        return jsonify(response), response['status_code']
    
    # Category routes
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        response = category_controller.get_categories(request.args.to_dict())
        return jsonify(response), response['status_code']
    
    @app.route('/api/categories', methods=['POST'])
    def create_category():
        response = category_controller.create_category(request.json)
        return jsonify(response), response['status_code']
    
    @app.route('/api/categories/<slug>', methods=['GET'])
    def get_category(slug):
        response = category_controller.get_category_by_slug(slug)
        return jsonify(response), response['status_code']
    
    return app