"""
Durable Execution Framework
Provides checkpointing, recovery, and state persistence for long-running workflows
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
    Manages durable execution with checkpointing and recovery
    """
    
    def __init__(self, storage_path: str = "data/executions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.current_execution: Optional[str] = None
        self.execution_state: Dict[str, Any] = {}
    
    def start_execution(self, execution_id: str, workflow: Dict[str, Any]) -> str:
        """Start a new durable execution"""
        self.current_execution = execution_id
        
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
        
        checkpoint_id = self._generate_checkpoint_id(self.current_execution, phase)
        
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
        
        if not execution_record["checkpoints"]:
            raise ValueError(f"No checkpoints found for: {execution_id}")
        
        latest_checkpoint = execution_record["checkpoints"][-1]
        
        self.current_execution = execution_id
        self.execution_state = execution_record
        
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
        execution_record["duration"] = execution_record["end_time"] - execution_record["start_time"]
        
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


if __name__ == "__main__":
    print("=" * 60)
    print("DURABLE EXECUTION DEMO")
    print("=" * 60)
    
    executor = DurableExecution()
    
    execution_id = "exec_demo_001"
    workflow = {
        "name": "Research and Write Tutorial",
        "steps": ["research", "outline", "write", "review"]
    }
    
    print(f"\nStarting execution: {execution_id}")
    executor.start_execution(execution_id, workflow)
    
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
    
    print("\n--- Simulating Crash & Recovery ---")
    executor.current_execution = None
    
    resume_data = executor.resume_execution(execution_id)
    print(f"Resumed at phase: {resume_data['phase']}")
    print(f"State: {resume_data['state']}")
    print(f"Pending: {resume_data['pending_steps']}")
    
    print("\n--- Completing Execution ---")
    executor.complete_execution({"artifact": "tutorial.md", "quality": 0.89})
    
    status = executor.get_execution_status(execution_id)
    print(f"\nFinal Status: {json.dumps(status, indent=2)}")
