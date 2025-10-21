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
            'total_tasks_completed': sum(m.tasks_completed for m in relevant_metrics),
            'total_tasks_failed': sum(m.tasks_failed for m in relevant_metrics),
            'overall_success_rate': sum(m.tasks_completed for m in relevant_metrics) / 
                                   (sum(m.tasks_completed for m in relevant_metrics) + 
                                    sum(m.tasks_failed for m in relevant_metrics)),
            'total_tokens': sum(m.total_tokens for m in relevant_metrics),
            'average_refinement_cycles': sum(m.refinement_cycles for m in relevant_metrics) / len(relevant_metrics)
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive metrics report"""
        report_parts = [
            "# Multi-Agent System Metrics Report",
            f"Generated: {datetime.now().isoformat()}\n",
            "## Overall Statistics\n"
        ]
        
        # Overall agent statistics
        overall_agent_stats = self.get_agent_statistics()
        if overall_agent_stats:
            report_parts.extend([
                "### Agent Performance",
                f"- Total Executions: {overall_agent_stats['total_executions']}",
                f"- Success Rate: {overall_agent_stats['success_rate']:.1%}",
                f"- Average Duration: {overall_agent_stats['average_duration']:.2f}s",
                f"- Average Quality: {overall_agent_stats['average_quality']:.1%}",
                f"- Total Tokens: {overall_agent_stats['total_tokens']:,}",
                f"- Average Refinements: {overall_agent_stats['average_refinements']:.2f}\n"
            ])
        
        # Per-agent statistics
        agent_names = set(m.agent_name for m in self.agent_metrics)
        if agent_names:
            report_parts.append("### Individual Agent Performance\n")
            for agent_name in sorted(agent_names):
                stats = self.get_agent_statistics(agent_name)
                report_parts.extend([
                    f"#### {agent_name}",
                    f"- Executions: {stats['total_executions']}",
                    f"- Success Rate: {stats['success_rate']:.1%}",
                    f"- Avg Duration: {stats['average_duration']:.2f}s",
                    f"- Avg Quality: {stats['average_quality']:.1%}",
                    f"- Tokens: {stats['total_tokens']:,}\n"
                ])
        
        # Orchestration statistics
        overall_orch_stats = self.get_orchestration_statistics()
        if overall_orch_stats:
            report_parts.extend([
                "## Orchestration Performance\n",
                f"- Total Orchestrations: {overall_orch_stats['total_orchestrations']}",
                f"- Average Duration: {overall_orch_stats['average_duration']:.2f}s",
                f"- Average Quality: {overall_orch_stats['average_quality']:.1%}",
                f"- Tasks Completed: {overall_orch_stats['total_tasks_completed']}",
                f"- Tasks Failed: {overall_orch_stats['total_tasks_failed']}",
                f"- Overall Success Rate: {overall_orch_stats['overall_success_rate']:.1%}",
                f"- Total Tokens: {overall_orch_stats['total_tokens']:,}\n"
            ])
        
        # Per-pattern statistics
        patterns = set(m.pattern for m in self.orchestrator_metrics)
        if patterns:
            report_parts.append("### By Orchestration Pattern\n")
            for pattern in sorted(patterns):
                stats = self.get_orchestration_statistics(pattern)
                report_parts.extend([
                    f"#### {pattern}",
                    f"- Orchestrations: {stats['total_orchestrations']}",
                    f"- Avg Duration: {stats['average_duration']:.2f}s",
                    f"- Avg Quality: {stats['average_quality']:.1%}",
                    f"- Success Rate: {stats['overall_success_rate']:.1%}\n"
                ])
        
        return "\n".join(report_parts)
    
    def load_historical_metrics(self):
        """Load metrics from previously saved files"""
        for filepath in self.metrics_dir.glob("agent_*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.agent_metrics.append(AgentMetrics(**data))
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        for filepath in self.metrics_dir.glob("orchestrator_*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.orchestrator_metrics.append(OrchestratorMetrics(**data))
            except Exception as e:
                print(f"Error loading {filepath}: {e}")


class MetricsContext:
    """Context manager for tracking agent/orchestrator execution"""
    
    def __init__(self, collector: MetricsCollector, is_agent: bool = True, **kwargs):
        self.collector = collector
        self.is_agent = is_agent
        self.start_time = None
        self.kwargs = kwargs
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        duration = end_time - self.start_time
        
        if self.is_agent:
            metrics = AgentMetrics(
                agent_name=self.kwargs['agent_name'],
                task_id=self.kwargs['task_id'],
                start_time=self.start_time,
                end_time=end_time,
                duration=duration,
                quality_score=self.kwargs.get('quality_score', 0.0),
                token_usage=self.kwargs.get('token_usage', 0),
                refinement_iterations=self.kwargs.get('refinement_iterations', 0),
                success=exc_type is None,
                error_message=str(exc_val) if exc_val else ""
            )
            self.collector.record_agent_execution(metrics)
        else:
            metrics = OrchestratorMetrics(
                orchestration_id=self.kwargs['orchestration_id'],
                pattern=self.kwargs['pattern'],
                start_time=self.start_time,
                end_time=end_time,
                total_duration=duration,
                agents_used=self.kwargs.get('agents_used', []),
                tasks_completed=self.kwargs.get('tasks_completed', 0),
                tasks_failed=self.kwargs.get('tasks_failed', 0),
                average_quality=self.kwargs.get('average_quality', 0.0),
                total_tokens=self.kwargs.get('total_tokens', 0),
                refinement_cycles=self.kwargs.get('refinement_cycles', 0)
            )
            self.collector.record_orchestration(metrics)


# Example usage
if __name__ == "__main__":
    collector = MetricsCollector()
    
    # Example agent execution
    with MetricsContext(collector, is_agent=True, 
                       agent_name="researcher", 
                       task_id="task_001",
                       quality_score=0.85,
                       token_usage=1500,
                       refinement_iterations=1):
        # Simulate work
        time.sleep(0.1)
    
    # Example orchestration
    with MetricsContext(collector, is_agent=False,
                       orchestration_id="orch_001",
                       pattern="parallel",
                       agents_used=["researcher", "writer"],
                       tasks_completed=2,
                       tasks_failed=0,
                       average_quality=0.87,
                       total_tokens=3000,
                       refinement_cycles=1):
        # Simulate orchestration
        time.sleep(0.2)
    
    # Generate report
    print(collector.generate_report())
