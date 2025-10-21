"""
Security infrastructure for multi-agent API
Handles authentication, authorization, and encryption
Note: Requires PyJWT library (pip install pyjwt)
"""

import hashlib
import secrets
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# PyJWT import with fallback
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("Warning: PyJWT not installed. JWT functionality will be limited.")
    print("Install with: pip install pyjwt")

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
        self.api_keys: Dict[str, str] = {}
        self.token_blacklist: Set[str] = set()
    
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
    
    def authenticate_password(self, username: str, password: str) -> Optional[str]:
        """Authenticate with username/password, returns JWT token"""
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user or not user.active:
            return None
        
        if not self._verify_password(password, user.password_hash):
            return None
        
        if JWT_AVAILABLE:
            token = self._generate_jwt(user)
            return token
        else:
            # Fallback: return user_id as token (insecure, for testing only)
            return f"fallback_token_{user.user_id}"
    
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
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        if token in self.token_blacklist:
            return None
        
        if not JWT_AVAILABLE:
            # Fallback verification
            if token.startswith("fallback_token_"):
                user_id = token.replace("fallback_token_", "")
                if user_id in self.users:
                    user = self.users[user_id]
                    return {
                        "user_id": user.user_id,
                        "username": user.username,
                        "permissions": [p.value for p in user.permissions]
                    }
            return None
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            if datetime.utcnow().timestamp() > payload.get("exp", 0):
                return None
            
            return payload
        except:
            return None
    
    def revoke_token(self, token: str):
        """Revoke JWT token"""
        self.token_blacklist.add(token)
    
    def authorize(self, user_id: str, required_permission: Permission) -> bool:
        """Check if user has required permission"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        
        if not user.active:
            return False
        
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
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except:
            return False
    
    def _generate_jwt(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "permissions": [p.value for p in user.permissions],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token


if __name__ == "__main__":
    print("=" * 60)
    print("SECURITY MANAGER DEMO")
    print("=" * 60)
    
    security = SecurityManager(secret_key="demo-secret-key")
    
    print("\n--- Creating Users ---")
    admin = security.create_user("admin", "admin_pass", [Permission.ADMIN])
    print(f"Created admin: {admin.user_id}")
    
    worker = security.create_user("worker", "worker_pass", [Permission.READ_TASKS, Permission.EXECUTE_TASKS])
    print(f"Created worker: {worker.user_id}")
    
    print("\n--- Authentication ---")
    token = security.authenticate_password("admin", "admin_pass")
    print(f"Admin token: {token[:50] if token else 'None'}...")
    
    print("\n--- API Key Generation ---")
    api_key = security.generate_api_key(worker.user_id)
    print(f"Worker API key: {api_key[:30]}...")
    
    print("\n--- Authorization ---")
    print(f"Admin can delete tasks: {security.authorize(admin.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can delete tasks: {security.authorize(worker.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can execute tasks: {security.authorize(worker.user_id, Permission.EXECUTE_TASKS)}")
