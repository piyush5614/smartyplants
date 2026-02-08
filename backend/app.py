"""
Main Flask application factory and initialization.
Smart Plant Health Assistant Backend API.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from models.database_models import db


# Setup logging
logger = logging.getLogger(__name__)


def create_app(env=None):
    """
    Application factory for Flask app creation.
    
    Args:
        env: Environment name (development, testing, production).
             Defaults to FLASK_ENV environment variable.
    
    Returns:
        Configured Flask application instance
    
    Raises:
        ValueError: If required environment variables are missing
    """
    # Initialize configuration
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set environment-specific settings
    if env == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    elif env == 'production':
        app.config['DEBUG'] = False
        # Validate production configuration
        Config.validate_required_keys()
    else:  # development
        app.config['DEBUG'] = True
    
    # Initialize directories
    Config.init_directories()
    
    # Initialize database
    db.init_app(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:3000']),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Configure logging
    _configure_logging(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    # Register status routes
    _register_status_routes(app)
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
        logger.info("Database initialized successfully")
    
    logger.info(f"Flask app initialized for {env or 'development'} environment")
    
    return app


def _configure_logging(app):
    """
    Configure application-wide logging.
    
    Args:
        app: Flask application instance
    """
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'), logging.INFO)
    
    # Create logger
    app.logger.setLevel(log_level)
    
    # File handler
    log_file = app.config.get('LOG_FILE')
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    # Console handler (always)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)


def _register_blueprints(app):
    """
    Register application blueprints.
    
    Args:
        app: Flask application instance
    """
    # Import blueprints here to avoid circular imports
    try:
        from routes import health_bp, analysis_bp
        from routes.auth_routes import auth_routes
        
        app.register_blueprint(health_bp, url_prefix='/api/v1')
        app.register_blueprint(analysis_bp, url_prefix='/api/v1')
        app.register_blueprint(auth_routes)
        
        logger.info("Blueprints registered successfully")
    except ImportError as e:
        logger.warning(f"Could not load all blueprints: {e}")


def _register_error_handlers(app):
    """
    Register global error handlers.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error.description or error),
            'status': 400
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'status': 401
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'Access denied',
            'status': 403
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(413)
    def handle_payload_too_large(error):
        """Handle 413 Payload Too Large errors."""
        max_size = app.config.get('MAX_UPLOAD_SIZE_MB', 10)
        return jsonify({
            'success': False,
            'error': 'Payload Too Large',
            'message': f'File size exceeds maximum limit ({max_size}MB)',
            'status': 413
        }), 413
    
    @app.errorhandler(500)
    def handle_server_error(error):
        """Handle 500 Server errors."""
        logger.error(f"Server error: {error}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status': 500
        }), 500


# Status and health routes
def _register_status_routes(app):
    """Register status and health check routes."""
    
    frontend_dir = Path(app.config.get('FRONTEND_DIR', Config.FRONTEND_DIR)).resolve()
    
    @app.route('/', methods=['GET'])
    def root():
        """Serve the main app UI."""
        return send_from_directory(str(frontend_dir), 'index.html', mimetype='text/html')
    
    @app.route('/css/<path:path>')
    def serve_css(path):
        """Serve frontend CSS files."""
        return send_from_directory(frontend_dir / 'css', path)
    
    @app.route('/js/<path:path>')
    def serve_js(path):
        """Serve frontend JS files."""
        return send_from_directory(frontend_dir / 'js', path)
    
    @app.route('/assets/<path:path>')
    def serve_assets(path):
        """Serve frontend assets (images, logos, etc.)."""
        return send_from_directory(frontend_dir / 'assets', path)
    
    @app.route('/login')
    def serve_login():
        """Serve login page."""
        return send_from_directory(frontend_dir, 'login.html')
    
    @app.route('/api/v1/status', methods=['GET'])
    def status():
        """API status endpoint."""
        try:
            # Check database connection
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            db_status = 'unhealthy'
        
        return jsonify({
            'success': True,
            'status': 'operational',
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/api/v1/config', methods=['GET'])
    def config_info():
        """API configuration info (non-sensitive)."""
        return jsonify({
            'success': True,
            'config': app.config.to_dict() if hasattr(app.config, 'to_dict') else {}
        }), 200


if __name__ == '__main__':
    # Create application
    app = create_app('development')
    
    # Run development server
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=True
    )
