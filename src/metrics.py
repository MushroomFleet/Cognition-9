"""
Metrics collection and reporting for multi-agent systems
Tracks performance, quality, and execution patterns
"""

import time
import json
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class AgentMetrics:
    """Metrics for a single agent execution"""
    agent_name: str
    task_id: str
    start_time: float
    end_time: float
    duration: float
    quality_score: float
    token_usage: int
    refinement_iterations: int
    success: bool
    error_message: str = ""

@dataclass
class OrchestratorMetrics:
    """Metrics for overall orchestration"""
    orchestration_id: str
    pattern: str  # parallel, sequential, hub-spoke
    start_time: float
    end_time: float
    total_duration: float
    agents_used: List[str]
    tasks_completed: int
    tasks_failed: int
    average_quality: float
    total_tokens: int
    refinement_cycles: int

class MetricsCollector:
    """Collects and aggregates metrics across executions"""
    
    def __init__(self, metrics_dir: str = "logs/metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent_metrics: List[AgentMetrics] = []
        self.orchestrator_metrics: List[OrchestratorMetrics] = []
        
    def record_agent_execution(self, metrics: AgentMetrics):
        """Record metrics from agent execution"""
        self.agent_metrics.append(metrics)
        self._persist_agent_metrics(metrics)
    
    def record_orchestration(self, metrics: OrchestratorMetrics):
        """Record metrics from orchestration"""
        self.orchestrator_metrics.append(metrics)
        self._persist_orchestrator_metrics(metrics)
    
    def _persist_agent_metrics(self, metrics: AgentMetrics):
        """Save agent metrics to file"""
        filename = f"agent_{metrics.agent_name}_{int(time.time())}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
    
    def _persist_orchestrator_metrics(self, metrics: OrchestratorMetrics):
        """Save orchestrator metrics to file"""
        filename = f"orchestrator_{metrics.orchestration_id}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
    
    def get_agent_statistics(self, agent_name: str = None) -> Dict[str, Any]:
        """Get aggregated statistics for agent(s)"""
        relevant_metrics = [
            m for m in self.agent_metrics
            if agent_name is None or m.agent_name == agent_name
        ]
        
        if not relevant_metrics:
            return {}
        
        return {
            'agent_name': agent_name or 'all',
            'total_executions': len(relevant_metrics),
            'successful_executions': sum(1 for m in relevant_metrics if m.success),
            'failed_executions': sum(1 for m in relevant_metrics if not m.success),
            'success_rate': sum(1 for m in relevant_metrics if m.success) / len(relevant_metrics),
            'average_duration': sum(m.duration for m in relevant_metrics) / len(relevant_metrics),
            'average_quality': sum(m.quality_score for m in relevant_metrics) / len(relevant_metrics),
            'total_tokens': sum(m.token_usage for m in relevant_metrics),
            'average_refinements': sum(m.refinement_iterations for m in relevant_metrics) / len(relevant_metrics)
        }
    
    def get_orchestration_statistics(self, pattern: str = None) -> Dict[str, Any]:
        """Get aggregated statistics for orchestrations"""
        relevant_metrics = [
            m for m in self.orchestrator_metrics
            if pattern is None or m.pattern == pattern
        ]
        
        if not relevant_metrics:
            return {}
        
        return {
            'pattern': pattern or 'all',
            'total_orchestrations': len(relevant_metrics),
            'average_duration': sum(m.total_duration for m in relevant_metrics) / len(relevant_metrics),
            'average_quality': sum(m.average_quality for m in relevant_metrics) / len(relevant_metrics),
            'average_agents_used': sum(len(m.agents_used) for m in relevant_metrics) / len(relevant_metrics),
            'total_tokens': sum(m.total_tokens for m in relevant_metrics),
            'average_refinements': sum(m.refinement_cycles for m in relevant_metrics) / len(relevant_metrics),
            'success_rate': sum(1 for m in relevant_metrics if m.tasks_failed == 0) / len(relevant_metrics)
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive metrics report"""
        report_parts = [
            "# Multi-Agent System Metrics Report\n",
            f"Generated: {datetime.now().isoformat()}\n",
            "=" * 60,
            "\n"
        ]
        
        # Agent statistics
        report_parts.append("\n## Agent Performance\n")
        for agent in set(m.agent_name for m in self.agent_metrics):
            stats = self.get_agent_statistics(agent)
            if stats:
                report_parts.append(f"\n### {agent}")
                report_parts.append(f"- Total Executions: {stats['total_executions']}")
                report_parts.append(f"- Success Rate: {stats['success_rate']:.1%}")
                report_parts.append(f"- Average Duration: {stats['average_duration']:.2f}s")
                report_parts.append(f"- Average Quality: {stats['average_quality']:.1%}")
                report_parts.append(f"- Total Tokens: {stats['total_tokens']:,}")
        
        # Orchestration statistics
        report_parts.append("\n\n## Orchestration Performance\n")
        for pattern in set(m.pattern for m in self.orchestrator_metrics):
            stats = self.get_orchestration_statistics(pattern)
            if stats:
                report_parts.append(f"\n### {pattern}")
                report_parts.append(f"- Total Orchestrations: {stats['total_orchestrations']}")
                report_parts.append(f"- Success Rate: {stats['success_rate']:.1%}")
                report_parts.append(f"- Average Duration: {stats['average_duration']:.2f}s")
                report_parts.append(f"- Average Quality: {stats['average_quality']:.1%}")
        
        return "\n".join(report_parts)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("METRICS COLLECTION DEMO")
    print("=" * 60)
    
    collector = MetricsCollector()
    
    # Record sample agent execution
    agent_metrics = AgentMetrics(
        agent_name="researcher",
        task_id="task_001",
        start_time=time.time(),
        end_time=time.time() + 120,
        duration=120.0,
        quality_score=0.92,
        token_usage=15000,
        refinement_iterations=1,
        success=True
    )
    
    collector.record_agent_execution(agent_metrics)
    print("\n✓ Recorded agent execution metrics")
    
    # Record sample orchestration
    orch_metrics = OrchestratorMetrics(
        orchestration_id="orch_001",
        pattern="sequential",
        start_time=time.time(),
        end_time=time.time() + 300,
        total_duration=300.0,
        agents_used=["researcher", "writer"],
        tasks_completed=2,
        tasks_failed=0,
        average_quality=0.90,
        total_tokens=35000,
        refinement_cycles=1
    )
    
    collector.record_orchestration(orch_metrics)
    print("✓ Recorded orchestration metrics")
    
    # Generate report
    print("\n" + "=" * 60)
    print(collector.generate_report())
