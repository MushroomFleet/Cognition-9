"""
Homeostatic control mechanisms for multi-agent systems
Maintains multiple objectives in dynamic equilibrium
"""

import time
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class ObjectiveStatus(Enum):
    """Status of homeostatic objective"""
    STABLE = "stable"
    DRIFTING = "drifting"
    CRITICAL = "critical"

@dataclass
class HomeostaticObjective:
    """Represents a single objective to maintain in equilibrium"""
    name: str
    setpoint: float  # Target value
    tolerance: float  # Acceptable deviation
    priority: int  # Higher number = higher priority (1-10)
    current_value: float = 0.0
    history: List[float] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
    
    def deviation(self) -> float:
        """Calculate deviation from setpoint"""
        return abs(self.setpoint - self.current_value)
    
    def urgency(self) -> float:
        """Calculate urgency based on deviation and priority"""
        dev = self.deviation()
        if dev < self.tolerance:
            return 0.0
        # Urgency increases with deviation and priority
        normalized_deviation = dev / self.tolerance
        return normalized_deviation * self.priority
    
    def status(self) -> ObjectiveStatus:
        """Determine current status of objective"""
        dev = self.deviation()
        if dev < self.tolerance:
            return ObjectiveStatus.STABLE
        elif dev < self.tolerance * 2:
            return ObjectiveStatus.DRIFTING
        else:
            return ObjectiveStatus.CRITICAL
    
    def update_value(self, new_value: float):
        """Update current value and history"""
        self.history.append(self.current_value)
        self.current_value = new_value
        
        # Keep history manageable
        if len(self.history) > 100:
            self.history = self.history[-100:]

class HomeostaticController:
    """
    Maintains multiple objectives in dynamic equilibrium
    Implements homeostatic control loops for quality, speed, cost, etc.
    """
    
    def __init__(self):
        self.objectives: Dict[str, HomeostaticObjective] = {}
        self.correction_history: List[Dict[str, Any]] = []
        self.intervention_log_path = Path("logs/homeostasis")
        self.intervention_log_path.mkdir(parents=True, exist_ok=True)
    
    def add_objective(self, objective: HomeostaticObjective):
        """Add a new objective to monitor"""
        self.objectives[objective.name] = objective
    
    def update_measurement(self, objective_name: str, value: float):
        """Update measured value for an objective"""
        if objective_name in self.objectives:
            self.objectives[objective_name].update_value(value)
    
    def check_equilibrium(self) -> Dict[str, Any]:
        """
        Check if all objectives are in equilibrium
        Returns status and most urgent objective if intervention needed
        """
        urgencies = {
            name: obj.urgency()
            for name, obj in self.objectives.items()
        }
        
        most_urgent_name = max(urgencies, key=urgencies.get) if urgencies else None
        most_urgent_value = urgencies.get(most_urgent_name, 0.0) if most_urgent_name else 0.0
        
        statuses = {
            name: obj.status().value
            for name, obj in self.objectives.items()
        }
        
        all_stable = all(
            obj.status() == ObjectiveStatus.STABLE
            for obj in self.objectives.values()
        )
        
        any_critical = any(
            obj.status() == ObjectiveStatus.CRITICAL
            for obj in self.objectives.values()
        )
        
        return {
            'equilibrium': all_stable,
            'critical': any_critical,
            'most_urgent': most_urgent_name,
            'urgency_level': most_urgent_value,
            'statuses': statuses,
            'urgencies': urgencies
        }
    
    def intervene(self, objective_name: str) -> Dict[str, Any]:
        """
        Apply corrective action for specific objective
        Returns recommended interventions
        """
        if objective_name not in self.objectives:
            return {'error': f'Unknown objective: {objective_name}'}
        
        obj = self.objectives[objective_name]
        current = obj.current_value
        target = obj.setpoint
        deviation = obj.deviation()
        
        # Determine intervention strategy based on objective type
        intervention = self._generate_intervention(obj, current, target, deviation)
        
        # Log intervention
        self.correction_history.append({
            'timestamp': time.time(),
            'objective': objective_name,
            'current_value': current,
            'target': target,
            'deviation': deviation,
            'intervention': intervention
        })
        
        self._persist_intervention(intervention)
        
        return intervention
    
    def _generate_intervention(
        self,
        objective: HomeostaticObjective,
        current: float,
        target: float,
        deviation: float
    ) -> Dict[str, Any]:
        """Generate specific intervention based on objective type"""
        
        if objective.name == 'quality':
            if current < target:
                return {
                    'type': 'quality_improvement',
                    'actions': [
                        'Increase refinement iterations',
                        'Apply stricter validation criteria',
                        'Request human review for borderline outputs',
                        'Enable CRITIC pattern validation'
                    ],
                    'expected_improvement': deviation * 0.5,
                    'priority': 'high' if deviation > objective.tolerance * 1.5 else 'medium'
                }
            else:
                return {
                    'type': 'quality_stable',
                    'actions': ['Maintain current quality processes'],
                    'expected_improvement': 0,
                    'priority': 'low'
                }
        
        elif objective.name == 'speed':
            if current > target:  # Too slow
                return {
                    'type': 'speed_optimization',
                    'actions': [
                        'Reduce task complexity where possible',
                        'Use parallel execution patterns',
                        'Employ faster model tiers for routine subtasks',
                        'Reduce refinement iterations if quality permits'
                    ],
                    'expected_improvement': deviation * 0.4,
                    'priority': 'high' if deviation > objective.tolerance * 1.5 else 'medium'
                }
            else:
                return {
                    'type': 'speed_stable',
                    'actions': ['Maintain current execution speed'],
                    'expected_improvement': 0,
                    'priority': 'low'
                }
        
        elif objective.name == 'cost':
            if current > target:  # Too expensive
                return {
                    'type': 'cost_reduction',
                    'actions': [
                        'Use more efficient model tiers',
                        'Reduce token usage through summarization',
                        'Cache and reuse common patterns',
                        'Limit refinement cycles',
                        'Implement early termination when threshold met'
                    ],
                    'expected_improvement': deviation * 0.6,
                    'priority': 'high' if deviation > objective.tolerance * 1.5 else 'medium'
                }
            else:
                return {
                    'type': 'cost_stable',
                    'actions': ['Maintain current cost efficiency'],
                    'expected_improvement': 0,
                    'priority': 'low'
                }
        
        elif objective.name == 'novelty':
            if current < target:  # Not novel enough
                return {
                    'type': 'novelty_enhancement',
                    'actions': [
                        'Inject creative variation in prompts',
                        'Explore alternative perspectives',
                        'Increase temperature for content generation',
                        'Encourage unconventional approaches'
                    ],
                    'expected_improvement': deviation * 0.3,
                    'priority': 'medium'
                }
            else:
                return {
                    'type': 'novelty_stable',
                    'actions': ['Maintain current creativity level'],
                    'expected_improvement': 0,
                    'priority': 'low'
                }
        
        else:
            return {
                'type': 'unknown_objective',
                'actions': ['Manual intervention required'],
                'expected_improvement': 0,
                'priority': 'medium'
            }
    
    def _persist_intervention(self, intervention: Dict[str, Any]):
        """Save intervention to log file"""
        timestamp = int(time.time())
        filename = f"intervention_{timestamp}.json"
        filepath = self.intervention_log_path / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'intervention': intervention
            }, f, indent=2)
    
    def auto_regulate(self) -> List[Dict[str, Any]]:
        """
        Automatically check and correct all objectives
        Returns list of interventions applied
        """
        equilibrium = self.check_equilibrium()
        interventions = []
        
        if not equilibrium['equilibrium']:
            # Sort objectives by urgency
            urgent_objectives = sorted(
                self.objectives.items(),
                key=lambda x: x[1].urgency(),
                reverse=True
            )
            
            # Apply interventions to most urgent objectives
            for name, obj in urgent_objectives:
                if obj.urgency() > 0:
                    intervention = self.intervene(name)
                    interventions.append({
                        'objective': name,
                        'intervention': intervention
                    })
                    
                    # Stop after addressing most critical issues
                    if len(interventions) >= 3:
                        break
        
        return interventions
    
    def get_status_report(self) -> str:
        """Generate human-readable status report"""
        equilibrium = self.check_equilibrium()
        
        report_parts = [
            "# Homeostatic Control Status Report",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**System Equilibrium**: {'✅ STABLE' if equilibrium['equilibrium'] else '⚠️ REGULATING'}\n"
        ]
        
        if equilibrium['critical']:
            report_parts.append("🚨 **CRITICAL**: One or more objectives in critical state\n")
        
        report_parts.append("## Objective Status\n")
        
        for name, obj in self.objectives.items():
            status = obj.status()
            urgency = obj.urgency()
            
            status_icon = {
                ObjectiveStatus.STABLE: "✅",
                ObjectiveStatus.DRIFTING: "⚠️",
                ObjectiveStatus.CRITICAL: "🚨"
            }[status]
            
            report_parts.extend([
                f"### {status_icon} {name.title()}",
                f"- **Target**: {obj.setpoint:.2f}",
                f"- **Current**: {obj.current_value:.2f}",
                f"- **Deviation**: {obj.deviation():.2f}",
                f"- **Tolerance**: ±{obj.tolerance:.2f}",
                f"- **Status**: {status.value}",
                f"- **Urgency**: {urgency:.2f}",
                f"- **Priority**: {obj.priority}/10\n"
            ])
        
        if equilibrium['most_urgent'] and equilibrium['urgency_level'] > 0:
            report_parts.extend([
                "## Recommended Action\n",
                f"**Most Urgent**: {equilibrium['most_urgent']}",
                f"**Urgency Level**: {equilibrium['urgency_level']:.2f}\n"
            ])
        
        return "\n".join(report_parts)


# Example usage
if __name__ == "__main__":
    # Create homeostatic controller
    controller = HomeostaticController()
    
    # Define objectives
    quality_obj = HomeostaticObjective(
        name='quality',
        setpoint=0.85,  # Target 85% quality
        tolerance=0.05,  # ±5% acceptable
        priority=10  # Highest priority
    )
    
    speed_obj = HomeostaticObjective(
        name='speed',
        setpoint=2.0,  # Target 2 hours per task
        tolerance=0.5,  # ±30 minutes acceptable
        priority=7
    )
    
    cost_obj = HomeostaticObjective(
        name='cost',
        setpoint=50000,  # Target 50k tokens
        tolerance=10000,  # ±10k acceptable
        priority=8
    )
    
    novelty_obj = HomeostaticObjective(
        name='novelty',
        setpoint=0.7,  # Target 70% novelty
        tolerance=0.1,  # ±10% acceptable
        priority=5
    )
    
    # Add objectives
    controller.add_objective(quality_obj)
    controller.add_objective(speed_obj)
    controller.add_objective(cost_obj)
    controller.add_objective(novelty_obj)
    
    # Simulate measurements
    controller.update_measurement('quality', 0.72)  # Below target
    controller.update_measurement('speed', 2.8)  # Too slow
    controller.update_measurement('cost', 55000)  # Slightly over
    controller.update_measurement('novelty', 0.68)  # Close to target
    
    # Check equilibrium
    equilibrium = controller.check_equilibrium()
    print("Equilibrium Status:", equilibrium)
    print()
    
    # Apply auto-regulation
    interventions = controller.auto_regulate()
    print("Interventions Applied:")
    for intervention in interventions:
        print(f"\n{intervention['objective']}:")
        print(json.dumps(intervention['intervention'], indent=2))
    
    print("\n" + "="*60)
    print(controller.get_status_report())
