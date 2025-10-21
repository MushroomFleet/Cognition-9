# Stage 5: Production Deployment
## Enterprise-Ready Multi-Agent Systems

**Timeline**: Weeks 7-8  
**Goal**: Deploy production-ready multi-agent orchestration  
**Complexity**: Advanced

---

## Overview

This stage transforms your multi-agent system from development prototype to production-ready service. You'll implement durable execution, comprehensive security, API endpoints, monitoring, and continuous improvement processes.

### What You'll Build

- **Durable execution**: Checkpointing and recovery
- **Security infrastructure**: Authentication, authorization, encryption
- **API layer**: REST/GraphQL endpoints for integration
- **Cost management**: Token budgets and optimization
- **Continuous improvement**: A/B testing and adaptation

### Prerequisites

- Completed Stages 1-3 (core multi-agent system operational)
- Understanding of API design and security principles
- Familiarity with deployment and DevOps practices
- Access to deployment infrastructure

---

## Phase 1: Durable Execution & Checkpointing

### Concept

Multi-agent workflows can be long-running and complex. Durable execution ensures work isn't lost due to failures and enables resumption from checkpoints.

### Implementation

Create `src/durable_execution.py`:

```python
"""
Durable Execution Framework
Provides checkpointing, recovery, and state persistence
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass
class Checkpoint:
    """Represents a checkpoint in execution"""
    checkpoint_id: str
    execution_id: str
    timestamp: float
    phase: str
    state: Dict[str, Any]
    completed_steps: List[str]
    pending_steps: List[str]
    metadata: Dict[str, Any]

class DurableExecution:
    """
    Manages durable execution with checkpointing
    """
    
    def __init__(self, storage_path: str = "data/executions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.current_execution: Optional[str] = None
        self.execution_state: Dict[str, Any] = {}
    
    def start_execution(
        self,
        execution_id: str,
        workflow: Dict[str, Any]
    ) -> str:
        """Start a new durable execution"""
        self.current_execution = execution_id
        
        # Initialize execution record
        execution_record = {
            "execution_id": execution_id,
            "workflow": workflow,
            "status": ExecutionStatus.RUNNING.value,
            "start_time": time.time(),
            "checkpoints": [],
            "completed_steps": [],
            "state": {}
        }
        
        self._save_execution(execution_record)
        self.execution_state = execution_record
        
        return execution_id
    
    def checkpoint(
        self,
        phase: str,
        state: Dict[str, Any],
        completed_steps: List[str],
        pending_steps: List[str]
    ) -> str:
        """Create a checkpoint during execution"""
        if not self.current_execution:
            raise ValueError("No active execution")
        
        checkpoint_id = self._generate_checkpoint_id(
            self.current_execution,
            phase
        )
        
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            execution_id=self.current_execution,
            timestamp=time.time(),
            phase=phase,
            state=state,
            completed_steps=completed_steps,
            pending_steps=pending_steps,
            metadata={}
        )
        
        # Update execution record
        execution_record = self._load_execution(self.current_execution)
        execution_record["checkpoints"].append(asdict(checkpoint))
        execution_record["completed_steps"] = completed_steps
        execution_record["state"] = state
        
        self._save_execution(execution_record)
        self.execution_state = execution_record
        
        print(f"✓ Checkpoint created: {checkpoint_id} (phase: {phase})")
        
        return checkpoint_id
    
    def resume_execution(self, execution_id: str) -> Dict[str, Any]:
        """Resume execution from latest checkpoint"""
        execution_record = self._load_execution(execution_id)
        
        if not execution_record:
            raise ValueError(f"Execution not found: {execution_id}")
        
        # Get latest checkpoint
        if not execution_record["checkpoints"]:
            raise ValueError(f"No checkpoints found for: {execution_id}")
        
        latest_checkpoint = execution_record["checkpoints"][-1]
        
        self.current_execution = execution_id
        self.execution_state = execution_record
        
        # Update status
        execution_record["status"] = ExecutionStatus.RUNNING.value
        self._save_execution(execution_record)
        
        print(f"✓ Resuming from checkpoint: {latest_checkpoint['checkpoint_id']}")
        
        return {
            "execution_id": execution_id,
            "phase": latest_checkpoint["phase"],
            "state": latest_checkpoint["state"],
            "completed_steps": latest_checkpoint["completed_steps"],
            "pending_steps": latest_checkpoint["pending_steps"]
        }
    
    def complete_execution(self, result: Dict[str, Any]):
        """Mark execution as completed"""
        if not self.current_execution:
            raise ValueError("No active execution")
        
        execution_record = self._load_execution(self.current_execution)
        execution_record["status"] = ExecutionStatus.COMPLETED.value
        execution_record["end_time"] = time.time()
        execution_record["result"] = result
        execution_record["duration"] = (
            execution_record["end_time"] - execution_record["start_time"]
        )
        
        self._save_execution(execution_record)
        
        print(f"✓ Execution completed: {self.current_execution}")
        
        self.current_execution = None
        self.execution_state = {}
    
    def fail_execution(self, error: str):
        """Mark execution as failed"""
        if not self.current_execution:
            raise ValueError("No active execution")
        
        execution_record = self._load_execution(self.current_execution)
        execution_record["status"] = ExecutionStatus.FAILED.value
        execution_record["end_time"] = time.time()
        execution_record["error"] = error
        
        self._save_execution(execution_record)
        
        print(f"✗ Execution failed: {self.current_execution}")
        print(f"  Error: {error}")
        
        self.current_execution = None
        self.execution_state = {}
    
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get current status of an execution"""
        execution_record = self._load_execution(execution_id)
        if not execution_record:
            return {"status": "not_found"}
        
        return {
            "execution_id": execution_id,
            "status": execution_record["status"],
            "checkpoints": len(execution_record.get("checkpoints", [])),
            "completed_steps": len(execution_record.get("completed_steps", [])),
            "duration": execution_record.get("duration")
        }
    
    def _generate_checkpoint_id(self, execution_id: str, phase: str) -> str:
        """Generate unique checkpoint ID"""
        data = f"{execution_id}_{phase}_{time.time()}"
        return f"ckpt_{hashlib.md5(data.encode()).hexdigest()[:12]}"
    
    def _save_execution(self, execution_record: Dict[str, Any]):
        """Persist execution record"""
        filepath = self.storage_path / f"{execution_record['execution_id']}.json"
        with open(filepath, 'w') as f:
            json.dump(execution_record, f, indent=2)
    
    def _load_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Load execution record"""
        filepath = self.storage_path / f"{execution_id}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            return json.load(f)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("DURABLE EXECUTION DEMO")
    print("=" * 60)
    
    executor = DurableExecution()
    
    # Start execution
    execution_id = "exec_demo_001"
    workflow = {
        "name": "Research and Write Tutorial",
        "steps": ["research", "outline", "write", "review"]
    }
    
    print(f"\nStarting execution: {execution_id}")
    executor.start_execution(execution_id, workflow)
    
    # Simulate work with checkpoints
    print("\n--- Phase 1: Research ---")
    time.sleep(0.5)
    executor.checkpoint(
        phase="research",
        state={"sources": 5, "findings": 12},
        completed_steps=["research"],
        pending_steps=["outline", "write", "review"]
    )
    
    print("\n--- Phase 2: Outline ---")
    time.sleep(0.5)
    executor.checkpoint(
        phase="outline",
        state={"sections": 7, "subsections": 23},
        completed_steps=["research", "outline"],
        pending_steps=["write", "review"]
    )
    
    # Simulate recovery
    print("\n--- Simulating Crash & Recovery ---")
    executor.current_execution = None  # Simulate crash
    
    resume_data = executor.resume_execution(execution_id)
    print(f"Resumed at phase: {resume_data['phase']}")
    print(f"State: {resume_data['state']}")
    print(f"Pending: {resume_data['pending_steps']}")
    
    # Complete execution
    print("\n--- Completing Execution ---")
    executor.complete_execution({"artifact": "tutorial.md", "quality": 0.89})
    
    # Check status
    status = executor.get_execution_status(execution_id)
    print(f"\nFinal Status: {json.dumps(status, indent=2)}")
```

---

## Phase 2: Security Infrastructure

### Authentication & Authorization

Create `src/security.py`:

```python
"""
Security infrastructure for multi-agent API
Handles authentication, authorization, and encryption
"""

import jwt
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
    
    def authenticate_password(
        self,
        username: str,
        password: str
    ) -> Optional[str]:
        """Authenticate with username/password, returns JWT token"""
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
        
        # Generate JWT token
        token = self._generate_jwt(user)
        return token
    
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
        
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            
            # Check expiration
            if datetime.utcnow().timestamp() > payload.get("exp", 0):
                return None
            
            return payload
        except jwt.InvalidTokenError:
            return None
    
    def revoke_token(self, token: str):
        """Revoke JWT token (add to blacklist)"""
        self.token_blacklist.add(token)
    
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
    token = security.authenticate_password("admin", "admin_password")
    print(f"Admin token: {token[:50]}...")
    
    # Generate API key
    print("\n--- API Key Generation ---")
    api_key = security.generate_api_key(worker.user_id)
    print(f"Worker API key: {api_key[:30]}...")
    
    # Authorization
    print("\n--- Authorization ---")
    print(f"Admin can delete tasks: {security.authorize(admin.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can delete tasks: {security.authorize(worker.user_id, Permission.DELETE_TASKS)}")
    print(f"Worker can execute tasks: {security.authorize(worker.user_id, Permission.EXECUTE_TASKS)}")
```

---

## Phase 3: API Layer

### REST API Implementation

Create `src/api.py`:

```python
"""
REST API for multi-agent orchestration
Provides HTTP endpoints for task management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from typing import Dict, Any
import json

from security import SecurityManager, Permission
from durable_execution import DurableExecution

app = Flask(__name__)
CORS(app)

# Initialize components
security = SecurityManager(secret_key="your-secret-key-change-in-production")
executor = DurableExecution()

# In-memory task storage (replace with database in production)
tasks: Dict[str, Dict[str, Any]] = {}

def require_auth(permission: Permission = None):
    """Decorator for authentication and authorization"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get token from header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"error": "No authorization header"}), 401
            
            try:
                scheme, token = auth_header.split(' ')
                if scheme.lower() != 'bearer':
                    return jsonify({"error": "Invalid auth scheme"}), 401
            except ValueError:
                return jsonify({"error": "Invalid auth header"}), 401
            
            # Verify token
            payload = security.verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid token"}), 401
            
            # Check permission if required
            if permission:
                if not security.authorize(payload['user_id'], permission):
                    return jsonify({"error": "Insufficient permissions"}), 403
            
            # Add user info to request
            request.user_id = payload['user_id']
            request.username = payload['username']
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400
    
    token = security.authenticate_password(username, password)
    if not token:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"token": token})

@app.route('/api/tasks', methods=['POST'])
@require_auth(Permission.CREATE_TASKS)
def create_task():
    """Create new task"""
    data = request.get_json()
    
    task_id = f"task_{len(tasks) + 1:04d}"
    task = {
        "task_id": task_id,
        "description": data.get('description'),
        "requirements": data.get('requirements', {}),
        "status": "pending",
        "created_by": request.user_id,
        "created_at": None  # Would use datetime
    }
    
    tasks[task_id] = task
    
    return jsonify(task), 201

@app.route('/api/tasks/<task_id>', methods=['GET'])
@require_auth(Permission.READ_TASKS)
def get_task(task_id: str):
    """Get task details"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task)

@app.route('/api/tasks/<task_id>/execute', methods=['POST'])
@require_auth(Permission.EXECUTE_TASKS)
def execute_task(task_id: str):
    """Execute task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    # Start durable execution
    execution_id = f"exec_{task_id}"
    workflow = {
        "task_id": task_id,
        "steps": ["analyze", "delegate", "execute", "validate"]
    }
    
    executor.start_execution(execution_id, workflow)
    
    task["status"] = "running"
    task["execution_id"] = execution_id
    
    return jsonify({
        "task_id": task_id,
        "execution_id": execution_id,
        "status": "running"
    })

@app.route('/api/executions/<execution_id>', methods=['GET'])
@require_auth(Permission.READ_TASKS)
def get_execution_status(execution_id: str):
    """Get execution status"""
    status = executor.get_execution_status(execution_id)
    return jsonify(status)

@app.route('/api/tasks', methods=['GET'])
@require_auth(Permission.READ_TASKS)
def list_tasks():
    """List all tasks"""
    # Apply filters
    status_filter = request.args.get('status')
    
    filtered_tasks = [
        task for task in tasks.values()
        if not status_filter or task['status'] == status_filter
    ]
    
    return jsonify({
        "tasks": filtered_tasks,
        "total": len(filtered_tasks)
    })

if __name__ == '__main__':
    # Create default admin user
    admin = security.create_user(
        "admin",
        "admin123",
        [Permission.ADMIN]
    )
    print(f"Created admin user: {admin.username}")
    print("Login with: username=admin, password=admin123")
    
    app.run(debug=True, port=5000)
```

---

## Phase 4: Cost Management

### Token Budget System

Create `src/cost_management.py`:

```python
"""
Cost management and token budgeting
Tracks and limits token usage across executions
"""

import json
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta

@dataclass
class TokenBudget:
    """Token budget for a user or project"""
    budget_id: str
    total_budget: int  # Total tokens allocated
    used_tokens: int  # Tokens used so far
    period_start: float
    period_end: float
    
    def remaining(self) -> int:
        """Get remaining tokens"""
        return max(0, self.total_budget - self.used_tokens)
    
    def utilization(self) -> float:
        """Get budget utilization percentage"""
        if self.total_budget == 0:
            return 0.0
        return (self.used_tokens / self.total_budget) * 100.0
    
    def is_exceeded(self) -> bool:
        """Check if budget exceeded"""
        return self.used_tokens >= self.total_budget

class CostManager:
    """
    Manages token budgets and cost tracking
    """
    
    # Pricing per 1M tokens (example rates)
    MODEL_COSTS = {
        "opus": {"input": 15.0, "output": 75.0},
        "sonnet": {"input": 3.0, "output": 15.0},
        "haiku": {"input": 0.25, "output": 1.25}
    }
    
    def __init__(self, storage_path: str = "data/budgets"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.budgets: Dict[str, TokenBudget] = {}
        self._load_budgets()
    
    def create_budget(
        self,
        budget_id: str,
        total_tokens: int,
        period_days: int = 30
    ) -> TokenBudget:
        """Create new token budget"""
        now = datetime.utcnow().timestamp()
        
        budget = TokenBudget(
            budget_id=budget_id,
            total_budget=total_tokens,
            used_tokens=0,
            period_start=now,
            period_end=now + (period_days * 86400)
        )
        
        self.budgets[budget_id] = budget
        self._save_budget(budget)
        
        return budget
    
    def check_budget(
        self,
        budget_id: str,
        requested_tokens: int
    ) -> tuple[bool, str]:
        """
        Check if budget allows requested tokens
        
        Returns:
            (allowed, message)
        """
        budget = self.budgets.get(budget_id)
        if not budget:
            return False, f"Budget not found: {budget_id}"
        
        # Check if period expired
        now = datetime.utcnow().timestamp()
        if now > budget.period_end:
            return False, "Budget period expired"
        
        # Check if sufficient tokens
        if budget.used_tokens + requested_tokens > budget.total_budget:
            remaining = budget.remaining()
            return False, f"Insufficient tokens (have: {remaining}, need: {requested_tokens})"
        
        return True, "OK"
    
    def consume_tokens(
        self,
        budget_id: str,
        tokens_used: int,
        model: str = "sonnet"
    ) -> Dict:
        """
        Record token usage
        
        Returns:
            Usage details including cost
        """
        budget = self.budgets.get(budget_id)
        if not budget:
            raise ValueError(f"Budget not found: {budget_id}")
        
        budget.used_tokens += tokens_used
        self._save_budget(budget)
        
        # Calculate cost
        cost = self._calculate_cost(tokens_used, model)
        
        return {
            "tokens_used": tokens_used,
            "budget_remaining": budget.remaining(),
            "budget_utilization": budget.utilization(),
            "estimated_cost_usd": cost
        }
    
    def get_budget_status(self, budget_id: str) -> Dict:
        """Get current budget status"""
        budget = self.budgets.get(budget_id)
        if not budget:
            return {"error": "Budget not found"}
        
        now = datetime.utcnow().timestamp()
        days_remaining = (budget.period_end - now) / 86400.0
        
        return {
            "budget_id": budget_id,
            "total_budget": budget.total_budget,
            "used_tokens": budget.used_tokens,
            "remaining_tokens": budget.remaining(),
            "utilization_percent": round(budget.utilization(), 2),
            "days_remaining": round(days_remaining, 1),
            "status": "exceeded" if budget.is_exceeded() else "active"
        }
    
    def _calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        if model not in self.MODEL_COSTS:
            model = "sonnet"  # Default
        
        # Simplified: assume 50/50 input/output split
        input_tokens = tokens // 2
        output_tokens = tokens - input_tokens
        
        rates = self.MODEL_COSTS[model]
        cost = (
            (input_tokens / 1_000_000) * rates["input"] +
            (output_tokens / 1_000_000) * rates["output"]
        )
        
        return round(cost, 4)
    
    def _save_budget(self, budget: TokenBudget):
        """Persist budget"""
        filepath = self.storage_path / f"{budget.budget_id}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(budget), f, indent=2)
    
    def _load_budgets(self):
        """Load existing budgets"""
        if not self.storage_path.exists():
            return
        
        for filepath in self.storage_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    budget = TokenBudget(**data)
                    self.budgets[budget.budget_id] = budget
            except Exception as e:
                print(f"Error loading budget from {filepath}: {e}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("COST MANAGEMENT DEMO")
    print("=" * 60)
    
    cost_mgr = CostManager()
    
    # Create budget
    print("\n--- Creating Budget ---")
    budget = cost_mgr.create_budget(
        budget_id="project_alpha",
        total_tokens=1_000_000,
        period_days=30
    )
    print(f"Created budget: {budget.budget_id}")
    print(f"Total tokens: {budget.total_budget:,}")
    
    # Check budget
    print("\n--- Checking Budget ---")
    allowed, msg = cost_mgr.check_budget("project_alpha", 50_000)
    print(f"Request 50k tokens: {msg}")
    
    # Consume tokens
    print("\n--- Consuming Tokens ---")
    usage = cost_mgr.consume_tokens("project_alpha", 50_000, model="opus")
    print(f"Tokens used: {usage['tokens_used']:,}")
    print(f"Estimated cost: ${usage['estimated_cost_usd']}")
    print(f"Remaining: {usage['budget_remaining']:
