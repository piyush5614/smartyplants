"""Health check and status routes."""

from flask import Blueprint, jsonify, current_app

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')


@health_bp.route('', methods=['GET'])
@health_bp.route('/status', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Plant Health Assistant',
        'version': '1.0.0',
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }), 200


@health_bp.route('/info', methods=['GET'])
def service_info():
    """Get service information."""
    return jsonify({
        'name': 'Smart Plant Health Assistant',
        'version': '1.0.0',
        'description': 'AI-powered plant disease detection and care advice system',
        'features': [
            'Image-based plant disease detection',
            'Severity analysis',
            'Personalized care recommendations',
            'Plant analysis history'
        ],
        'endpoints': {
            'health': '/api/v1/health',
            'analyze': '/api/v1/analyze',
            'history': '/api/v1/history'
        }
    }), 200
