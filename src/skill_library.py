"""
Skill Library for multi-agent systems
Stores and retrieves successful task patterns for continuous learning
"""

import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class TaskPattern:
    """Represents a successful task execution pattern"""
    pattern_id: str
    task_type: str
    description: str
    solution_template: Dict[str, Any]
    success_metrics: Dict[str, float]
    context: Dict[str, Any]
    timestamp: float
    usage_count: int = 0
    success_rate: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskPattern':
        """Create from dictionary"""
        return cls(**data)

class SkillLibrary:
    """
    Stores and retrieves successful task execution patterns
    Enables continuous learning through pattern reuse
    """
    
    def __init__(self, library_path: str = "data/skill_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.patterns: Dict[str, TaskPattern] = {}
        self.load_library()
    
    def _generate_pattern_id(self, task_type: str, description: str) -> str:
        """Generate unique pattern ID"""
        content = f"{task_type}:{description}:{time.time()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def store_pattern(
        self,
        task_type: str,
        description: str,
        solution_template: Dict[str, Any],
        success_metrics: Dict[str, float],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a successful task pattern
        Returns pattern ID
        """
        # Only store if quality meets threshold
        if success_metrics.get('quality', 0) < 0.8:
            return None
        
        pattern_id = self._generate_pattern_id(task_type, description)
        
        pattern = TaskPattern(
            pattern_id=pattern_id,
            task_type=task_type,
            description=description,
            solution_template=solution_template,
            success_metrics=success_metrics,
            context=context or {},
            timestamp=time.time()
        )
        
        self.patterns[pattern_id] = pattern
        self._persist_pattern(pattern)
        
        return pattern_id
    
    def retrieve_similar(
        self,
        task_type: str,
        description: str,
        min_similarity: float = 0.7,
        min_success_rate: float = 0.8
    ) -> List[TaskPattern]:
        """
        Retrieve patterns similar to given task
        Returns list of matching patterns sorted by relevance
        """
        matching_patterns = []
        
        for pattern in self.patterns.values():
            # Filter by task type
            if pattern.task_type != task_type:
                continue
            
            # Filter by success rate
            if pattern.success_rate < min_success_rate:
                continue
            
            # Calculate similarity
            similarity = self._calculate_similarity(description, pattern.description)
            
            if similarity >= min_similarity:
                matching_patterns.append((similarity, pattern))
        
        # Sort by similarity (descending) and success rate
        matching_patterns.sort(
            key=lambda x: (x[0], x[1].success_rate),
            reverse=True
        )
        
        return [pattern for _, pattern in matching_patterns]
    
    def _calculate_similarity(self, desc1: str, desc2: str) -> float:
        """
        Calculate similarity between two task descriptions
        Simple word-based similarity for now
        """
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def record_usage(
        self,
        pattern_id: str,
        success: bool,
        actual_metrics: Dict[str, float]
    ):
        """
        Record pattern usage and update success rate
        """
        if pattern_id not in self.patterns:
            return
        
        pattern = self.patterns[pattern_id]
        pattern.usage_count += 1
        
        # Update success rate using exponential moving average
        alpha = 0.3  # Weight for new observation
        if success:
            pattern.success_rate = (alpha * 1.0) + ((1 - alpha) * pattern.success_rate)
        else:
            pattern.success_rate = (alpha * 0.0) + ((1 - alpha) * pattern.success_rate)
        
        # Update pattern metrics based on actual performance
        for metric, value in actual_metrics.items():
            if metric in pattern.success_metrics:
                # Update with exponential moving average
                pattern.success_metrics[metric] = (
                    (alpha * value) + ((1 - alpha) * pattern.success_metrics[metric])
                )
        
        self._persist_pattern(pattern)
    
    def adapt_pattern(
        self,
        pattern_id: str,
        new_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapt a stored pattern to new context
        Returns adapted solution template
        """
        if pattern_id not in self.patterns:
            return None
        
        pattern = self.patterns[pattern_id]
        adapted_template = pattern.solution_template.copy()
        
        # Simple adaptation: merge new context
        if 'parameters' in adapted_template:
            adapted_template['parameters'].update(new_context)
        else:
            adapted_template['context'] = new_context
        
        return adapted_template
    
    def get_best_patterns(
        self,
        task_type: Optional[str] = None,
        limit: int = 10
    ) -> List[TaskPattern]:
        """
        Get best performing patterns
        Optionally filtered by task type
        """
        patterns = list(self.patterns.values())
        
        if task_type:
            patterns = [p for p in patterns if p.task_type == task_type]
        
        # Sort by success rate and usage count
        patterns.sort(
            key=lambda x: (x.success_rate, x.usage_count),
            reverse=True
        )
        
        return patterns[:limit]
    
    def prune_library(
        self,
        min_success_rate: float = 0.5,
        min_usage_count: int = 3
    ):
        """
        Remove poorly performing patterns
        Keeps library size manageable
        """
        patterns_to_remove = []
        
        for pattern_id, pattern in self.patterns.items():
            # Keep if usage count too low to judge
            if pattern.usage_count < min_usage_count:
                continue
            
            # Remove if success rate too low
            if pattern.success_rate < min_success_rate:
                patterns_to_remove.append(pattern_id)
        
        for pattern_id in patterns_to_remove:
            self._remove_pattern(pattern_id)
    
    def _persist_pattern(self, pattern: TaskPattern):
        """Save pattern to disk"""
        filename = f"pattern_{pattern.pattern_id}.json"
        filepath = self.library_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(pattern.to_dict(), f, indent=2)
    
    def _remove_pattern(self, pattern_id: str):
        """Remove pattern from library and disk"""
        if pattern_id in self.patterns:
            del self.patterns[pattern_id]
        
        filename = f"pattern_{pattern_id}.json"
        filepath = self.library_path / filename
        
        if filepath.exists():
            filepath.unlink()
    
    def load_library(self):
        """Load all patterns from disk"""
        self.patterns = {}
        
        for filepath in self.library_path.glob("pattern_*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    pattern = TaskPattern.from_dict(data)
                    self.patterns[pattern.pattern_id] = pattern
            except Exception as e:
                print(f"Error loading pattern from {filepath}: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics"""
        if not self.patterns:
            return {
                'total_patterns': 0,
                'task_types': [],
                'average_success_rate': 0.0,
                'total_usage_count': 0
            }
        
        task_types = {}
        total_usage = 0
        total_success = 0.0
        
        for pattern in self.patterns.values():
            task_types[pattern.task_type] = task_types.get(pattern.task_type, 0) + 1
            total_usage += pattern.usage_count
            total_success += pattern.success_rate
        
        return {
            'total_patterns': len(self.patterns),
            'task_types': task_types,
            'average_success_rate': total_success / len(self.patterns),
            'total_usage_count': total_usage,
            'most_common_type': max(task_types, key=task_types.get) if task_types else None
        }
    
    def generate_report(self) -> str:
        """Generate human-readable library report"""
        stats = self.get_statistics()
        best_patterns = self.get_best_patterns(limit=5)
        
        report_parts = [
            "# Skill Library Report",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Statistics\n",
            f"- **Total Patterns**: {stats['total_patterns']}",
            f"- **Average Success Rate**: {stats['average_success_rate']:.1%}",
            f"- **Total Usage Count**: {stats['total_usage_count']}",
            f"- **Most Common Type**: {stats['most_common_type'] or 'N/A'}\n",
            "## Task Types\n"
        ]
        
        for task_type, count in stats['task_types'].items():
            report_parts.append(f"- **{task_type}**: {count} patterns")
        
        if best_patterns:
            report_parts.extend([
                "\n## Top Performing Patterns\n"
            ])
            
            for i, pattern in enumerate(best_patterns, 1):
                report_parts.extend([
                    f"### {i}. {pattern.task_type}",
                    f"- **Description**: {pattern.description}",
                    f"- **Success Rate**: {pattern.success_rate:.1%}",
                    f"- **Usage Count**: {pattern.usage_count}",
                    f"- **Quality**: {pattern.success_metrics.get('quality', 0):.1%}\n"
                ])
        
        return "\n".join(report_parts)


# Example usage
if __name__ == "__main__":
    # Create skill library
    library = SkillLibrary()
    
    # Store a successful pattern
    pattern_id = library.store_pattern(
        task_type='research',
        description='Python async/await best practices research',
        solution_template={
            'approach': 'multi-source comprehensive research',
            'sources': ['official docs', 'academic papers', 'tutorials'],
            'organization': 'thematic with citations',
            'validation': 'cross-reference claims'
        },
        success_metrics={
            'quality': 0.92,
            'completeness': 0.88,
            'citation_ratio': 0.85
        },
        context={
            'domain': 'programming',
            'complexity': 'intermediate',
            'audience': 'developers'
        }
    )
    
    print(f"Stored pattern: {pattern_id}\n")
    
    # Retrieve similar patterns
    similar = library.retrieve_similar(
        task_type='research',
        description='Python asyncio patterns and practices'
    )
    
    print(f"Found {len(similar)} similar patterns\n")
    
    # Record usage
    if similar:
        library.record_usage(
            pattern_id=similar[0].pattern_id,
            success=True,
            actual_metrics={'quality': 0.90, 'completeness': 0.85}
        )
        print("Recorded usage\n")
    
    # Get statistics
    print(library.generate_report())
