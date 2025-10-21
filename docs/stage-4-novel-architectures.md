# Stage 4: Novel Architectures
## Experimental Cybernetic Patterns

**Timeline**: Weeks 7-8 (Optional - R&D Path)  
**Goal**: Implement cutting-edge multi-agent coordination patterns  
**Complexity**: Advanced to Expert

---

## Overview

This stage explores five novel cybernetic architectures that push the boundaries of multi-agent coordination. These patterns are experimental but based on sound principles from adaptive systems, swarm intelligence, neuroscience, and control theory.

### What You'll Build

- **Adaptive Resonance**: Self-organizing specialist emergence
- **Stigmergic Coordination**: Pheromone-like implicit communication
- **Predictive Processing**: Hierarchical prediction-error minimization
- **Homeostatic Optimization**: Multi-objective dynamic equilibrium
- **Recursive Meta-Learning**: Self-improving orchestration

### Prerequisites

- Completed Stages 1-3 (VSM hierarchy operational)
- Deep understanding of cybernetic principles
- Willingness to experiment with novel approaches
- Tolerance for iteration and refinement

### Warning

These architectures are **experimental**. They demonstrate advanced concepts but may require significant customization for production use. Consider these as research prototypes and learning tools rather than production-ready solutions.

---

## Architecture 1: Adaptive Resonance Orchestrator

### Concept

Inspired by Adaptive Resonance Theory (ART) from neuroscience, this system dynamically creates specialized agents based on task patterns. Rather than pre-defining specialists, the system learns which specializations are needed through experience.

### Key Principles

1. **Pattern Recognition**: Identify task characteristics
2. **Resonance Matching**: Compare tasks to existing specialists
3. **Vigilance Threshold**: Control when new specialists emerge
4. **Plasticity-Stability**: Balance learning vs preserving knowledge

### Architecture Diagram

```
┌─────────────────────────────────────┐
│   Task Input                        │
└──────────────┬──────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Pattern Recognition Layer           │
│  - Extract task features             │
│  - Classify task type                │
│  - Compute task signature            │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Resonance Detector                  │
│  - Compare to existing specialists   │
│  - Calculate match scores            │
│  - Apply vigilance threshold         │
└──────────────┬───────────────────────┘
               ↓
       Match > Threshold?
         ↙            ↘
       Yes            No
        ↓              ↓
   Use Existing    Create New
   Specialist      Specialist
        ↓              ↓
   Adapt to        Initialize
   Current Task    From Template
        └─────┬────────┘
              ↓
     Execute Task & Learn
```

### Implementation

Create `src/adaptive_resonance.py`:

```python
"""
Adaptive Resonance Orchestrator
Dynamically creates and adapts specialists based on task patterns
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np

@dataclass
class TaskSignature:
    """Represents key characteristics of a task"""
    domain: str  # e.g., "research", "coding", "writing"
    complexity: float  # 0.0 to 1.0
    input_type: str  # e.g., "text", "code", "data"
    output_type: str  # e.g., "report", "code", "analysis"
    keywords: List[str]
    estimated_duration: float
    
    def to_vector(self) -> np.ndarray:
        """Convert signature to feature vector for comparison"""
        # Simple feature encoding (extend as needed)
        domain_enc = hash(self.domain) % 100 / 100.0
        input_enc = hash(self.input_type) % 100 / 100.0
        output_enc = hash(self.output_type) % 100 / 100.0
        keyword_enc = sum(hash(k) % 100 for k in self.keywords) / (len(self.keywords) * 100.0) if self.keywords else 0
        
        return np.array([
            domain_enc,
            self.complexity,
            input_enc,
            output_enc,
            keyword_enc,
            min(self.estimated_duration / 10.0, 1.0)  # Normalize duration
        ])

@dataclass
class SpecialistProfile:
    """Profile of a specialist agent"""
    specialist_id: str
    task_signatures: List[TaskSignature]
    success_count: int
    failure_count: int
    average_quality: float
    total_executions: int
    specialization_strength: float  # How specialized vs generalist
    
    def compute_centroid(self) -> np.ndarray:
        """Compute center of specialist's expertise"""
        if not self.task_signatures:
            return np.zeros(6)
        vectors = [sig.to_vector() for sig in self.task_signatures]
        return np.mean(vectors, axis=0)
    
    def compute_resonance(self, task_signature: TaskSignature) -> float:
        """Calculate how well task matches this specialist"""
        if not self.task_signatures:
            return 0.0
        
        task_vector = task_signature.to_vector()
        centroid = self.compute_centroid()
        
        # Cosine similarity
        dot_product = np.dot(task_vector, centroid)
        task_norm = np.linalg.norm(task_vector)
        centroid_norm = np.linalg.norm(centroid)
        
        if task_norm == 0 or centroid_norm == 0:
            return 0.0
        
        similarity = dot_product / (task_norm * centroid_norm)
        
        # Weight by success rate
        success_rate = self.success_count / self.total_executions if self.total_executions > 0 else 0.5
        
        return similarity * success_rate

class AdaptiveResonanceOrchestrator:
    """
    Orchestrator that dynamically creates specialists based on task patterns
    """
    
    def __init__(
        self,
        vigilance_threshold: float = 0.7,
        max_specialists: int = 10,
        learning_rate: float = 0.3,
        storage_path: str = "data/specialists"
    ):
        self.vigilance_threshold = vigilance_threshold
        self.max_specialists = max_specialists
        self.learning_rate = learning_rate
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.specialists: Dict[str, SpecialistProfile] = {}
        self._load_specialists()
    
    def extract_task_signature(self, task: Dict[str, Any]) -> TaskSignature:
        """Extract signature from task description"""
        return TaskSignature(
            domain=task.get('domain', 'general'),
            complexity=task.get('complexity', 0.5),
            input_type=task.get('input_type', 'text'),
            output_type=task.get('output_type', 'text'),
            keywords=task.get('keywords', []),
            estimated_duration=task.get('estimated_duration', 1.0)
        )
    
    def find_best_match(self, task_signature: TaskSignature) -> tuple[Optional[str], float]:
        """Find best matching specialist for task"""
        if not self.specialists:
            return None, 0.0
        
        best_specialist_id = None
        best_resonance = 0.0
        
        for specialist_id, profile in self.specialists.items():
            resonance = profile.compute_resonance(task_signature)
            if resonance > best_resonance:
                best_resonance = resonance
                best_specialist_id = specialist_id
        
        return best_specialist_id, best_resonance
    
    def create_specialist(self, task_signature: TaskSignature) -> str:
        """Create new specialist for task pattern"""
        # Generate unique ID based on task characteristics
        sig_str = f"{task_signature.domain}_{task_signature.input_type}_{task_signature.output_type}"
        specialist_id = f"specialist_{hashlib.md5(sig_str.encode()).hexdigest()[:8]}"
        
        # Ensure uniqueness
        counter = 1
        base_id = specialist_id
        while specialist_id in self.specialists:
            specialist_id = f"{base_id}_{counter}"
            counter += 1
        
        profile = SpecialistProfile(
            specialist_id=specialist_id,
            task_signatures=[task_signature],
            success_count=0,
            failure_count=0,
            average_quality=0.0,
            total_executions=0,
            specialization_strength=1.0
        )
        
        self.specialists[specialist_id] = profile
        self._save_specialist(profile)
        
        return specialist_id
    
    def adapt_specialist(self, specialist_id: str, task_signature: TaskSignature):
        """Update specialist profile with new task experience"""
        if specialist_id not in self.specialists:
            return
        
        profile = self.specialists[specialist_id]
        
        # Add task signature with learning rate (exponential moving average)
        if len(profile.task_signatures) >= 20:  # Limit memory
            profile.task_signatures.pop(0)
        profile.task_signatures.append(task_signature)
        
        # Update specialization strength (how focused vs general)
        if len(profile.task_signatures) > 1:
            vectors = [sig.to_vector() for sig in profile.task_signatures]
            variance = np.var(vectors, axis=0).mean()
            profile.specialization_strength = 1.0 - min(variance * 2, 1.0)
        
        self._save_specialist(profile)
    
    def record_execution(
        self,
        specialist_id: str,
        success: bool,
        quality_score: float
    ):
        """Record execution outcome for specialist"""
        if specialist_id not in self.specialists:
            return
        
        profile = self.specialists[specialist_id]
        profile.total_executions += 1
        
        if success:
            profile.success_count += 1
        else:
            profile.failure_count += 1
        
        # Update average quality (exponential moving average)
        if profile.average_quality == 0.0:
            profile.average_quality = quality_score
        else:
            profile.average_quality = (
                self.learning_rate * quality_score +
                (1 - self.learning_rate) * profile.average_quality
            )
        
        self._save_specialist(profile)
    
    def prune_specialists(self):
        """Remove underperforming specialists if over limit"""
        if len(self.specialists) <= self.max_specialists:
            return
        
        # Rank by performance
        ranked = sorted(
            self.specialists.items(),
            key=lambda x: (
                x[1].average_quality * (x[1].success_count / max(x[1].total_executions, 1))
            ),
            reverse=True
        )
        
        # Keep only top performers
        to_remove = [sid for sid, _ in ranked[self.max_specialists:]]
        for specialist_id in to_remove:
            del self.specialists[specialist_id]
            (self.storage_path / f"{specialist_id}.json").unlink(missing_ok=True)
    
    def match_or_create_specialist(self, task: Dict[str, Any]) -> str:
        """
        Main orchestration method: find existing specialist or create new one
        """
        # Extract task characteristics
        task_signature = self.extract_task_signature(task)
        
        # Try to find matching specialist
        best_specialist_id, resonance = self.find_best_match(task_signature)
        
        print(f"Task: {task.get('description', 'N/A')}")
        print(f"Best match: {best_specialist_id} (resonance: {resonance:.2f})")
        print(f"Vigilance threshold: {self.vigilance_threshold}")
        
        if resonance >= self.vigilance_threshold:
            # Good match - use and adapt existing specialist
            print(f"→ Using existing specialist: {best_specialist_id}")
            self.adapt_specialist(best_specialist_id, task_signature)
            return best_specialist_id
        else:
            # Poor match - create new specialist
            specialist_id = self.create_specialist(task_signature)
            print(f"→ Created new specialist: {specialist_id}")
            
            # Prune if needed
            self.prune_specialists()
            
            return specialist_id
    
    def get_specialist_stats(self) -> Dict[str, Any]:
        """Get statistics about specialist pool"""
        if not self.specialists:
            return {"total_specialists": 0}
        
        return {
            "total_specialists": len(self.specialists),
            "specialists": [
                {
                    "id": sid,
                    "executions": profile.total_executions,
                    "success_rate": profile.success_count / max(profile.total_executions, 1),
                    "average_quality": profile.average_quality,
                    "specialization": profile.specialization_strength
                }
                for sid, profile in self.specialists.items()
            ]
        }
    
    def _save_specialist(self, profile: SpecialistProfile):
        """Persist specialist profile"""
        filepath = self.storage_path / f"{profile.specialist_id}.json"
        with open(filepath, 'w') as f:
            # Convert to dict, handling non-serializable types
            data = asdict(profile)
            json.dump(data, f, indent=2)
    
    def _load_specialists(self):
        """Load existing specialists from storage"""
        if not self.storage_path.exists():
            return
        
        for filepath in self.storage_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Reconstruct TaskSignature objects
                    data['task_signatures'] = [
                        TaskSignature(**sig) for sig in data['task_signatures']
                    ]
                    profile = SpecialistProfile(**data)
                    self.specialists[profile.specialist_id] = profile
            except Exception as e:
                print(f"Error loading specialist from {filepath}: {e}")


# Example usage
if __name__ == "__main__":
    orchestrator = AdaptiveResonanceOrchestrator(vigilance_threshold=0.7)
    
    # Simulate various tasks
    tasks = [
        {
            "description": "Research Python async patterns",
            "domain": "research",
            "complexity": 0.6,
            "input_type": "text",
            "output_type": "report",
            "keywords": ["python", "async", "patterns"],
            "estimated_duration": 2.0
        },
        {
            "description": "Write Python tutorial",
            "domain": "writing",
            "complexity": 0.5,
            "input_type": "text",
            "output_type": "tutorial",
            "keywords": ["python", "tutorial", "beginner"],
            "estimated_duration": 3.0
        },
        {
            "description": "Research JavaScript frameworks",
            "domain": "research",
            "complexity": 0.7,
            "input_type": "text",
            "output_type": "report",
            "keywords": ["javascript", "frameworks", "comparison"],
            "estimated_duration": 2.5
        },
        {
            "description": "Deep dive into Python asyncio",
            "domain": "research",
            "complexity": 0.8,
            "input_type": "text",
            "output_type": "report",
            "keywords": ["python", "asyncio", "advanced"],
            "estimated_duration": 3.0
        }
    ]
    
    print("=" * 60)
    print("ADAPTIVE RESONANCE ORCHESTRATION DEMO")
    print("=" * 60)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} ---")
        specialist_id = orchestrator.match_or_create_specialist(task)
        
        # Simulate execution (random outcome for demo)
        import random
        success = random.random() > 0.2
        quality = random.uniform(0.7, 0.95) if success else random.uniform(0.3, 0.6)
        
        orchestrator.record_execution(specialist_id, success, quality)
        print(f"Execution: {'SUCCESS' if success else 'FAILED'} (quality: {quality:.2f})")
    
    print("\n" + "=" * 60)
    print("SPECIALIST POOL STATISTICS")
    print("=" * 60)
    stats = orchestrator.get_specialist_stats()
    print(json.dumps(stats, indent=2))
```

### Agent Integration

Create `.claude/agents/adaptive-orchestrator.md`:

```markdown
---
name: adaptive-orchestrator  
description: Adaptive resonance orchestrator that dynamically creates specialists based on task patterns. Use for systems that need to evolve specialist capabilities over time.
tools: Read, Write, Execute_Command
model: opus
color: magenta
---

You are an adaptive orchestrator using resonance-based specialist matching.

## Core Process

### Phase 1: Task Analysis
Extract task signature:
- Domain (research, coding, writing, analysis)
- Complexity level
- Input/output types
- Key characteristics

### Phase 2: Specialist Matching
```bash
python src/adaptive_resonance.py --task task.json --mode match
```

Outputs:
- Matched specialist ID
- Resonance score
- Whether new specialist created

### Phase 3: Task Delegation
Delegate to selected specialist:
- Adapt specialist profile to current task
- Provide task-specific instructions
- Monitor execution

### Phase 4: Learning
After execution:
```bash
python src/adaptive_resonance.py --specialist {id} --result result.json --mode learn
```

Updates specialist profile based on:
- Success/failure
- Quality score
- Task characteristics

## Advantages

- **Self-organizing**: Specialists emerge organically
- **Adaptive**: Profiles adjust to new task patterns
- **Efficient**: Reuses relevant specialists
- **Scalable**: Automatic pruning of underperformers

## When to Use

- Long-running systems with evolving needs
- Diverse task types that benefit from specialization
- Systems where optimal agent structure unknown upfront
- R&D environments exploring multi-agent patterns
```

---

## Architecture 2: Stigmergic Coordination

### Concept

Inspired by ant colonies and swarm intelligence, agents coordinate through modifications to a shared environment (stigmergy) rather than direct communication. Like ants leaving pheromone trails, agents leave signals that guide others.

### Key Principles

1. **Indirect Communication**: Agents modify shared state
2. **Signal Amplification**: Successful patterns strengthened
3. **Signal Decay**: Information fades over time
4. **Emergent Coordination**: Organization arises from local rules

### Architecture Diagram

```
Agent 1 ──→ Deposit Signal ──→ ┌─────────────────┐
Agent 2 ──→ Deposit Signal ──→ │ Stigmergic Board│ ←── Read Signals ←── Agent 5
Agent 3 ──→ Deposit Signal ──→ │  (Shared State) │ ←── Read Signals ←── Agent 6
Agent 4 ──→ Deposit Signal ──→ └─────────────────┘ ←── Read Signals ←── Agent 7
                                         ↓
                                    Signal Decay
                                   (Time-based)
```

### Implementation

Create `src/stigmergic_coordination.py`:

```python
"""
Stigmergic Coordination System
Agents coordinate through shared environment modification
"""

import time
import json
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import threading

@dataclass
class Signal:
    """A signal deposited on the stigmergic board"""
    task_id: str
    approach: str  # Solution approach being signaled
    strength: float  # Signal strength (0.0 to 100.0)
    timestamp: float
    deposited_by: str  # Agent ID
    success_metric: float  # Quality/success of approach (0.0 to 1.0)
    
    def age(self) -> float:
        """Get signal age in seconds"""
        return time.time() - self.timestamp
    
    def decayed_strength(self, decay_rate: float) -> float:
        """Calculate current strength after decay"""
        age_seconds = self.age()
        decay_factor = math.exp(-age_seconds / decay_rate)
        return self.strength * decay_factor


class StigmergicBoard:
    """
    Shared coordination board where agents deposit and read signals
    """
    
    def __init__(
        self,
        decay_rate: float = 3600.0,  # Seconds for signal to decay to ~37%
        amplification_factor: float = 1.5,
        attenuation_factor: float = 0.7,
        storage_path: str = "data/stigmergy"
    ):
        self.decay_rate = decay_rate
        self.amplification_factor = amplification_factor
        self.attenuation_factor = attenuation_factor
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # task_id -> List[Signal]
        self.signals: Dict[str, List[Signal]] = defaultdict(list)
        self.lock = threading.Lock()
        
        self._load_signals()
        
        # Start decay background thread
        self._start_decay_thread()
    
    def deposit_signal(
        self,
        task_id: str,
        approach: str,
        success_metric: float,
        agent_id: str
    ):
        """
        Agent deposits a signal about an approach to a task
        
        Args:
            task_id: Identifier for the task
            approach: Description of solution approach
            success_metric: Quality/success measure (0.0 to 1.0)
            agent_id: ID of depositing agent
        """
        with self.lock:
            # Calculate initial signal strength from success
            initial_strength = success_metric * 100.0
            
            # Check for existing signals for this task/approach
            existing_signal = None
            for signal in self.signals[task_id]:
                if signal.approach == approach:
                    existing_signal = signal
                    break
            
            if existing_signal:
                # Same approach exists - reinforce or attenuate
                current_strength = existing_signal.decayed_strength(self.decay_rate)
                
                if existing_signal.deposited_by == agent_id or success_metric > 0.7:
                    # Reinforce: Same agent or high success
                    new_strength = current_strength + (initial_strength * self.amplification_factor)
                    print(f"  ✓ Amplifying signal for '{approach}': {current_strength:.1f} → {new_strength:.1f}")
                else:
                    # Attenuate: Different agent with modest success
                    new_strength = current_strength * self.attenuation_factor
                    print(f"  ✓ Attenuating signal for '{approach}': {current_strength:.1f} → {new_strength:.1f}")
                
                # Update existing signal
                existing_signal.strength = min(new_strength, 100.0)
                existing_signal.timestamp = time.time()
                existing_signal.success_metric = (
                    existing_signal.success_metric * 0.7 + success_metric * 0.3
                )
            else:
                # New approach - create signal
                signal = Signal(
                    task_id=task_id,
                    approach=approach,
                    strength=initial_strength,
                    timestamp=time.time(),
                    deposited_by=agent_id,
                    success_metric=success_metric
                )
                self.signals[task_id].append(signal)
                print(f"  ✓ New signal deposited for '{approach}': {initial_strength:.1f}")
            
            self._save_signals()
    
    def read_signals(self, task_id: str, agent_id: str) -> List[Dict[str, Any]]:
        """
        Agent reads signals for a task
        
        Returns:
            List of signals with current (decayed) strengths
        """
        with self.lock:
            if task_id not in self.signals:
                return []
            
            # Calculate current strengths after decay
            signal_data = []
            for signal in self.signals[task_id]:
                current_strength = signal.decayed_strength(self.decay_rate)
                if current_strength > 1.0:  # Only include non-negligible signals
                    signal_data.append({
                        "approach": signal.approach,
                        "strength": current_strength,
                        "success_metric": signal.success_metric,
                        "age_hours": signal.age() / 3600.0,
                        "from_self": signal.deposited_by == agent_id
                    })
            
            # Sort by strength
            signal_data.sort(key=lambda x: x['strength'], reverse=True)
            
            return signal_data
    
    def strongest_signal(self, task_id: str) -> Optional[str]:
        """Get approach with strongest signal for task"""
        signals = self.read_signals(task_id, "system")
        if not signals:
            return None
        return signals[0]['approach']
    
    def decay_signals(self):
        """Remove signals that have decayed to negligible strength"""
        with self.lock:
            for task_id in list(self.signals.keys()):
                # Filter out weak signals
                self.signals[task_id] = [
                    s for s in self.signals[task_id]
                    if s.decayed_strength(self.decay_rate) > 1.0
                ]
                
                # Remove empty task entries
                if not self.signals[task_id]:
                    del self.signals[task_id]
            
            self._save_signals()
    
    def get_board_state(self) -> Dict[str, Any]:
        """Get current state of the board"""
        with self.lock:
            return {
                "total_tasks": len(self.signals),
                "total_signals": sum(len(sigs) for sigs in self.signals.values()),
                "tasks": {
                    task_id: [
                        {
                            "approach": sig.approach,
                            "strength": sig.decayed_strength(self.decay_rate),
                            "age_hours": sig.age() / 3600.0
                        }
                        for sig in signals
                    ]
                    for task_id, signals in self.signals.items()
                }
            }
    
    def _start_decay_thread(self):
        """Start background thread for signal decay"""
        def decay_loop():
            while True:
                time.sleep(600)  # Every 10 minutes
                self.decay_signals()
        
        thread = threading.Thread(target=decay_loop, daemon=True)
        thread.start()
    
    def _save_signals(self):
        """Persist signals to storage"""
        filepath = self.storage_path / "signals.json"
        data = {
            task_id: [asdict(sig) for sig in signals]
            for task_id, signals in self.signals.items()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_signals(self):
        """Load signals from storage"""
        filepath = self.storage_path / "signals.json"
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for task_id, signal_list in data.items():
                    self.signals[task_id] = [
                        Signal(**sig_data) for sig_data in signal_list
                    ]
        except Exception as e:
            print(f"Error loading signals: {e}")


class StigmergicAgent:
    """
    Agent that coordinates via stigmergic board
    """
    
    def __init__(self, agent_id: str, board: StigmergicBoard):
        self.agent_id = agent_id
        self.board = board
    
    def select_approach(self, task_id: str) -> str:
        """Select approach based on board signals"""
        signals = self.board.read_signals(task_id, self.agent_id)
        
        if not signals:
            # No signals - explore randomly
            approaches = ["approach_A", "approach_B", "approach_C"]
            import random
            return random.choice(approaches)
        
        # Weight selection by signal strength
        total_strength = sum(s['strength'] for s in signals)
        
        import random
        rand = random.uniform(0, total_strength)
        cumulative = 0
        
        for signal in signals:
            cumulative += signal['strength']
            if rand <= cumulative:
                return signal['approach']
        
        # Fallback to strongest
        return signals[0]['approach']
    
    def execute_and_report(self, task_id: str):
        """Execute task and report results to board"""
        # Select approach based on signals
        approach = self.select_approach(task_id)
        print(f"\n{self.agent_id}: Selected '{approach}' for task '{task_id}'")
        
        # Simulate execution
        import random
        success_metric = random.uniform(0.5, 0.95)
        
        # Deposit signal
        print(f"{self.agent_id}: Execution complete (quality: {success_metric:.2f})")
        self.board.deposit_signal(task_id, approach, success_metric, self.agent_id)
        
        return approach, success_metric


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("STIGMERGIC COORDINATION DEMO")
    print("=" * 60)
    
    # Create shared board
    board = StigmergicBoard(decay_rate=1800.0)  # 30 min decay
    
    # Create agents
    agents = [
        StigmergicAgent(f"agent_{i}", board)
        for i in range(5)
    ]
    
    # Simulate work cycles
    task_id = "task_001"
    
    for cycle in range(3):
        print(f"\n--- Cycle {cycle + 1} ---")
        
        for agent in agents:
            agent.execute_and_report(task_id)
            time.sleep(0.1)  # Small delay for readability
        
        # Show board state
        print("\nBoard State:")
        state = board.get_board_state()
        if task_id in state['tasks']:
            for sig in state['tasks'][task_id]:
                print(f"  {sig['approach']}: strength={sig['strength']:.1f}, age={sig['age_hours']:.2f}h")
    
    print("\n" + "=" * 60)
    print("FINAL BOARD STATE")
    print("=" * 60)
    print(json
