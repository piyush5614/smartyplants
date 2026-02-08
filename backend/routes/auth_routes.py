"""
Authentication routes for Smart Plant Health Assistant.
Handles user login, logout, and session validation endpoints.
"""

from flask import Blueprint, request, jsonify, session
from auth import get_auth_manager

# Create blueprint
auth_routes = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Get auth manager
auth_mgr = get_auth_manager()


@auth_routes.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request JSON:
        email (str): User email
        password (str): User password
        username (str): Display name
    
    Response:
        success (bool): Registration success
        message (str): Response message
        user (dict): User info if successful
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        username = data.get('username', '').strip()
        
        # Validate required fields
        if not email or not password or not username:
            return jsonify({
                'success': False,
                'message': 'Email, password, and username are required'
            }), 400
        
        # Attempt registration
        success, message = auth_mgr.register_user(email, password, username)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and create session.
    
    Request JSON:
        email (str): User email
        password (str): User password
    
    Response:
        success (bool): Login success
        message (str): Response message
        session_id (str): Session ID if successful
        user (dict): User info if successful
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validate required fields
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Attempt login
        session_id, message, user = auth_mgr.login(email, password)
        
        if session_id:
            return jsonify({
                'success': True,
                'message': message,
                'session_id': session_id,
                'user': user.to_dict() if user else None
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 401
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/guest', methods=['POST'])
def guest_login():
    """
    Create guest session (no authentication required).
    
    Response:
        success (bool): Login success
        message (str): Response message
        session_id (str): Session ID
        user (dict): Guest user info
    """
    try:
        session_id, message, guest_user = auth_mgr.login_guest()
        
        return jsonify({
            'success': True,
            'message': message,
            'session_id': session_id,
            'user': guest_user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/validate', methods=['POST'])
def validate_session():
    """
    Validate session and get user info.
    
    Request JSON:
        session_id (str): Session ID to validate
    
    Response:
        success (bool): Validation result
        message (str): Response message
        user (dict): User info if valid
        is_valid (bool): Session validity
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'is_valid': False,
                'message': 'Request body is required'
            }), 400
        
        session_id = data.get('session_id', '').strip()
        
        if not session_id:
            return jsonify({
                'success': False,
                'is_valid': False,
                'message': 'Session ID is required'
            }), 400
        
        # Validate session
        is_valid, user = auth_mgr.validate_session(session_id)
        
        if is_valid:
            return jsonify({
                'success': True,
                'is_valid': True,
                'message': 'Session is valid',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': True,
                'is_valid': False,
                'message': 'Session is invalid or expired'
            }), 401
    
    except Exception as e:
        return jsonify({
            'success': False,
            'is_valid': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/session-info', methods=['POST'])
def session_info():
    """
    Get detailed session information.
    
    Request JSON:
        session_id (str): Session ID
    
    Response:
        success (bool): Operation success
        message (str): Response message
        session (dict): Session info if valid
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        session_id = data.get('session_id', '').strip()
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Session ID is required'
            }), 400
        
        # Get session info
        session_info = auth_mgr.get_session_info(session_id)
        
        if session_info:
            return jsonify({
                'success': True,
                'message': 'Session info retrieved',
                'session': session_info
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Session not found or expired'
            }), 401
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/logout', methods=['POST'])
def logout():
    """
    Logout user and invalidate session.
    
    Request JSON:
        session_id (str): Session ID to logout
    
    Response:
        success (bool): Logout success
        message (str): Response message
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        session_id = data.get('session_id', '').strip()
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Session ID is required'
            }), 400
        
        # Logout
        success = auth_mgr.logout(session_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Logout successful'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@auth_routes.route('/demo-credentials', methods=['GET'])
def get_demo_credentials():
    """
    Get demo credentials for testing.
    
    Response:
        success (bool): Always True
        credentials (list): List of (email, password) tuples
    """
    try:
        credentials = auth_mgr.get_all_demo_credentials()
        
        return jsonify({
            'success': True,
            'credentials': [
                {'email': email, 'password': password}
                for email, password in credentials
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
