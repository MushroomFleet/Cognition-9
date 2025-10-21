"""
Adaptive Resonance Orchestrator
Dynamically creates and adapts specialists based on task patterns
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

# Simple numpy-free implementation for compatibility
class TaskSignature:
    """Represents key characteristics of a task"""
    def __init__(self, domain: str, complexity: float, input_type: str, 
                 output_type: str, keywords: List[str], estimated_duration: float):
        self.domain = domain
        self.complexity = complexity
        self.input_type = input_type
        self.output_type = output_type
        self.keywords = keywords
        self.estimated_duration = estimated_duration
    
    def to_dict(self):
        return {
            'domain': self.domain,
            'complexity': self.complexity,
            'input_type': self.input_type,
            'output_type': self.output_type,
            'keywords': self.keywords,
            'estimated_duration': self.estimated_duration
        }
    
    def to_vector(self) -> List[float]:
        """Convert signature to feature vector for comparison"""
        domain_enc = (hash(self.domain) % 100) / 100.0
        input_enc = (hash(self.input_type) % 100) / 100.0
        output_enc = (hash(self.output_type) % 100) / 100.0
        keyword_enc = sum(hash(k) % 100 for k in self.keywords) / (len(self.keywords) * 100.0) if self.keywords else 0
        
        return [
            domain_enc,
            self.complexity,
            input_enc,
            output_enc,
            keyword_enc,
            min(self.estimated_duration / 10.0, 1.0)
        ]


@dataclass
class SpecialistProfile:
    """Profile of a specialist agent"""
    specialist_id: str
    task_signatures: List[Dict]
    success_count: int
    failure_count: int
    average_quality: float
    total_executions: int
    specialization_strength: float
    
    def compute_centroid(self) -> List[float]:
        """Compute center of specialist's expertise"""
        if not self.task_signatures:
            return [0.0] * 6
        
        # Convert task signatures back to TaskSignature objects
        signatures = [TaskSignature(**sig) for sig in self.task_signatures]
        vectors = [sig.to_vector() for sig in signatures]
        
        # Compute mean
        centroid = [sum(v[i] for v in vectors) / len(vectors) for i in range(6)]
        return centroid
    
    def compute_resonance(self, task_signature: TaskSignature) -> float:
        """Calculate how well task matches this specialist"""
        if not self.task_signatures:
            return 0.0
        
        task_vector = task_signature.to_vector()
        centroid = self.compute_centroid()
        
        # Cosine similarity
        dot_product = sum(a * b for a, b in zip(task_vector, centroid))
        task_norm = sum(x ** 2 for x in task_vector) ** 0.5
        centroid_norm = sum(x ** 2 for x in centroid) ** 0.5
        
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
    
    def find_best_match(self, task_signature: TaskSignature) -> tuple:
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
            task_signatures=[task_signature.to_dict()],
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
        
        if len(profile.task_signatures) >= 20:
            profile.task_signatures.pop(0)
        profile.task_signatures.append(task_signature.to_dict())
        
        # Update specialization strength
        if len(profile.task_signatures) > 1:
            signatures = [TaskSignature(**sig) for sig in profile.task_signatures]
            vectors = [sig.to_vector() for sig in signatures]
            
            # Calculate variance
            means = [sum(v[i] for v in vectors) / len(vectors) for i in range(6)]
            variance = sum(sum((v[i] - means[i]) ** 2 for v in vectors) / len(vectors) for i in range(6)) / 6
            
            profile.specialization_strength = 1.0 - min(variance * 2, 1.0)
        
        self._save_specialist(profile)
    
    def record_execution(self, specialist_id: str, success: bool, quality_score: float):
        """Record execution outcome for specialist"""
        if specialist_id not in self.specialists:
            return
        
        profile = self.specialists[specialist_id]
        profile.total_executions += 1
        
        if success:
            profile.success_count += 1
        else:
            profile.failure_count += 1
        
        if profile.average_quality == 0.0:
            profile.average_quality = quality_score
        else:
            profile.average_quality = (
                self.learning_rate * quality_score +
                (1 - self.learning_rate) * profile.average_quality
            )
        
        self._save_specialist(profile)
    
    def match_or_create_specialist(self, task: Dict[str, Any]) -> str:
        """Main orchestration method"""
        task_signature = self.extract_task_signature(task)
        best_specialist_id, resonance = self.find_best_match(task_signature)
        
        print(f"Task: {task.get('description', 'N/A')}")
        print(f"Best match: {best_specialist_id} (resonance: {resonance:.2f})")
        
        if resonance >= self.vigilance_threshold:
            print(f"→ Using existing specialist: {best_specialist_id}")
            self.adapt_specialist(best_specialist_id, task_signature)
            return best_specialist_id
        else:
            specialist_id = self.create_specialist(task_signature)
            print(f"→ Created new specialist: {specialist_id}")
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
            json.dump(asdict(profile), f, indent=2)
    
    def _load_specialists(self):
        """Load existing specialists from storage"""
        if not self.storage_path.exists():
            return
        
        for filepath in self.storage_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    profile = SpecialistProfile(**data)
                    self.specialists[profile.specialist_id] = profile
            except Exception as e:
                print(f"Error loading specialist from {filepath}: {e}")


if __name__ == "__main__":
    import random
    
    orchestrator = AdaptiveResonanceOrchestrator(vigilance_threshold=0.7)
    
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
            "keywords": ["python", "tutorial"],
            "estimated_duration": 3.0
        }
    ]
    
    print("=" * 60)
    print("ADAPTIVE RESONANCE DEMO")
    print("=" * 60)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} ---")
        specialist_id = orchestrator.match_or_create_specialist(task)
        
        success = random.random() > 0.2
        quality = random.uniform(0.7, 0.95) if success else random.uniform(0.3, 0.6)
        
        orchestrator.record_execution(specialist_id, success, quality)
        print(f"Execution: {'SUCCESS' if success else 'FAILED'} (quality: {quality:.2f})")
    
    print("\n" + "=" * 60)
    stats = orchestrator.get_specialist_stats()
    print(json.dumps(stats, indent=2))
