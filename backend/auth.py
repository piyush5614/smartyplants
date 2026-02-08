"""
Authentication module for Smart Plant Health Assistant.
Handles user login, session management, and authentication.
"""

import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class User:
    """User data model."""
    
    def __init__(self, user_id: str, email: str, username: str, created_at: datetime = None):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.created_at = created_at or datetime.utcnow()
        self.is_guest = False
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'is_guest': self.is_guest
        }


class GuestUser(User):
    """Guest user (no authentication required)."""
    
    def __init__(self):
        user_id = f"guest_{uuid.uuid4().hex[:8]}"
        super().__init__(user_id, "guest@example.com", f"Guest_{uuid.uuid4().hex[:6]}")
        self.is_guest = True


class AuthenticationManager:
    """
    Manages user authentication and sessions.
    Handles login, logout, session validation.
    """
    
    def __init__(self):
        """Initialize authentication manager."""
        # In production, use actual database
        self.user_database = {}  # {email: password_hash}
        self.sessions = {}  # {session_id: (user, expiry)}
        self.users = {}  # {user_id: User}
        
        # Initialize demo users
        self._init_demo_users()
    
    def _init_demo_users(self):
        """Initialize demo users for testing."""
        demo_users = [
            ("demo@example.com", "demo123", "Demo User"),
            ("test@example.com", "test123", "Test User"),
            ("admin@example.com", "admin123", "Admin User"),
        ]
        
        for email, password, username in demo_users:
            self._create_user(email, password, username)
    
    def _create_user(self, email: str, password: str, username: str) -> User:
        """Create a new user in database."""
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Hash password
        password_hash = self._hash_password(password)
        self.user_database[email] = password_hash
        
        # Create user object
        user = User(user_id, email, username)
        self.users[user_id] = user
        
        return user
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return self._hash_password(password) == password_hash
    
    def register_user(self, email: str, password: str, username: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            email: User email
            password: User password
            username: Display name
            
        Returns:
            Tuple of (success, message)
        """
        # Validate input
        if not email or not password or not username:
            return False, "All fields are required"
        
        if "@" not in email:
            return False, "Invalid email format"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if email in self.user_database:
            return False, "Email already registered"
        
        try:
            self._create_user(email, password, username)
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, email: str, password: str) -> Tuple[Optional[str], str, Optional[User]]:
        """
        Authenticate user and create session.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (session_id, message, user)
        """
        # Validate input
        if not email or not password:
            return None, "Email and password are required", None
        
        # Check if user exists
        if email not in self.user_database:
            return None, "Invalid email or password", None
        
        # Verify password
        password_hash = self.user_database[email]
        if not self._verify_password(password, password_hash):
            return None, "Invalid email or password", None
        
        try:
            # Find user object
            user = None
            for u in self.users.values():
                if u.email == email:
                    user = u
                    break
            
            if not user:
                return None, "User not found", None
            
            # Create session
            session_id = self._create_session(user)
            
            return session_id, "Login successful", user
            
        except Exception as e:
            return None, f"Login failed: {str(e)}", None
    
    def login_guest(self) -> Tuple[str, str, GuestUser]:
        """
        Create guest session (no authentication).
        
        Returns:
            Tuple of (session_id, message, guest_user)
        """
        try:
            guest = GuestUser()
            self.users[guest.user_id] = guest
            
            session_id = self._create_session(guest)
            
            return session_id, "Guest login successful", guest
            
        except Exception as e:
            raise Exception(f"Guest login failed: {str(e)}")
    
    def _create_session(self, user: User) -> str:
        """
        Create a new session for user.
        
        Args:
            user: User object
            
        Returns:
            Session ID
        """
        session_id = f"session_{uuid.uuid4().hex}"
        expiry = datetime.utcnow() + timedelta(days=7)
        
        self.sessions[session_id] = {
            'user': user,
            'expiry': expiry,
            'created_at': datetime.utcnow()
        }
        
        return session_id
    
    def validate_session(self, session_id: str) -> Tuple[bool, Optional[User]]:
        """
        Validate session and return user if valid.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            Tuple of (is_valid, user)
        """
        if not session_id or session_id not in self.sessions:
            return False, None
        
        session_data = self.sessions[session_id]
        
        # Check expiry
        if datetime.utcnow() > session_data['expiry']:
            del self.sessions[session_id]
            return False, None
        
        return True, session_data['user']
    
    def logout(self, session_id: str) -> bool:
        """
        Logout user and invalidate session.
        
        Args:
            session_id: Session ID to invalidate
            
        Returns:
            Success status
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Get session information.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session info or None
        """
        is_valid, user = self.validate_session(session_id)
        
        if not is_valid:
            return None
        
        return {
            'session_id': session_id,
            'user': user.to_dict(),
            'created_at': self.sessions[session_id]['created_at'].isoformat(),
            'expires_at': self.sessions[session_id]['expiry'].isoformat()
        }
    
    def get_all_demo_credentials(self) -> list:
        """
        Get demo credentials for testing.
        
        Returns:
            List of (email, password) tuples
        """
        return [
            ("demo@example.com", "demo123"),
            ("test@example.com", "test123"),
            ("admin@example.com", "admin123"),
        ]


# Global authentication manager instance
auth_manager = AuthenticationManager()


def get_auth_manager() -> AuthenticationManager:
    """Get the global authentication manager instance."""
    return auth_manager
