"""Routes package - API endpoints."""

from .health_routes import health_bp
from .analysis_routes import analysis_bp

__all__ = ['health_bp', 'analysis_bp']
