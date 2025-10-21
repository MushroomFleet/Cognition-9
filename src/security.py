"""
Security infrastructure for multi-agent API
Handles authentication, authorization, and encryption
"""

import hashlib
import secrets
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class Permission(Enum):
    """System permissions"""
    READ_TASKS = "read:tasks"
    CREATE_TASKS = "create:tasks"
    EXECUTE_TASKS = "execute:tasks"
    DELETE_TASKS = "delete:tasks"
    READ_ARTIFACTS = "read:artifacts"
    WRITE_ARTIFACTS = "write:artifacts"
    ADMIN = "admin:all"

@dataclass
class User:
    """User account"""
    user_id: str
    username: str
    password_hash: str
    permissions: Set[Permission]
    api_key: Optional[str] = None
    active: bool = True

class SecurityManager:
    """
    Manages authentication, authorization, and security
    """
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, str] = {}  # api_key -> user_id
        self.sessions: Dict[str, Dict] = {}  # session_id -> session_data
    
    def create_user(
        self,
        username: str,
        password: str,
        permissions: List[Permission]
    ) -> User:
        """Create new user account"""
        user_id = self._generate_user_id(username)
        password_hash = self._hash_password(password)
        
        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            permissions=set(permissions)
        )
        
        self.users[user_id] = user
        return user
    
    def authenticate_password(
        self,
        username: str,
        password: str
    ) -> Optional[str]:
        """Authenticate with username/password, returns session token"""
        # Find user
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user or not user.active:
            return None
        
        # Verify password
        if not self._verify_password(password, user.password_hash):
            return None
        
        # Generate session token
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "user_id": user.user_id,
            "username": user.username,
            "permissions": [p.value for p in user.permissions],
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        
        return session_id
    
    def authenticate_api_key(self, api_key: str) -> Optional[str]:
        """Authenticate with API key, returns user_id"""
        return self.api_keys.get(api_key)
    
    def generate_api_key(self, user_id: str) -> str:
        """Generate API key for user"""
        if user_id not in self.users:
            raise ValueError(f"User not found: {user_id}")
        
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = user_id
        self.users[user_id].api_key = api_key
        
        return api_key
    
    def verify_session(self, session_id: str) -> Optional[Dict]:
        """Verify session token and return session data"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        # Check expiration
        if datetime.utcnow() > session["expires_at"]:
            del self.sessions[session_id]
            return None
        
        return session
    
    def revoke_session(self, session_id: str):
        """Revoke session token"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def authorize(
        self,
        user_id: str,
        required_permission: Permission
    ) -> bool:
        """Check if user has required permission"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        
        if not user.active:
            return False
        
        # Admin has all permissions
        if Permission.ADMIN in user.permissions:
            return True
        
        return required_permission in user.permissions
    
    def _generate_user_id(self, username: str) -> str:
        """Generate unique user ID"""
        data = f"{username}_{datetime.utcnow().isoformat()}"
        return f"user_{hashlib.sha256(data.encode()).hexdigest()[:16]}"
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return f"{salt}${pwd_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt.encode(),
                100000
            )
            return new_hash.hex() == pwd_hash
        except Exception:
            return False


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("SECURITY MANAGER DEMO")
    print("=" * 60)
    
    # Initialize security manager
    security = SecurityManager(secret_key="your-secret-key-here")
    
    # Create users
    print("\n--- Creating Users ---")
    admin = security.create_user(
        "admin",
        "admin_password",
        [Permission.ADMIN]
    )
    print(f"Created admin: {admin.user_id}")
    
    worker = security.create_user(
        "worker",
        "worker_password",
        [Permission.READ_TASKS, Permission.EXECUTE_TASKS]
    )
    print(f"Created worker: {worker.user_id}")
    
    # Authenticate
    print("\n--- Authentication ---")
    session_id = security.authenticate_password("admin", "admin_password")
    print(f"Admin session: {session_id[:30]}...")
    
    # Generate API key
    print("\n--- API Key Generation ---")
    api_key = security.generate_api_key(worker.user_id)
    print(f"Worker API key: {api_key[:30]}...")
    
    # Authorization
    print("\n--- Authorization ---")
    print(f"Admin can delete tasks: {security.authorize(admin.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can delete tasks: {security.authorize(worker.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can execute tasks: {security.authorize(worker.user_id, Permission.EXECUTE_TASKS)}")
