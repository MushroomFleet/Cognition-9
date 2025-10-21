"""
Test script for Stage 2: Core Patterns & Observability
Tests orchestration patterns, CRITIC validation, and metrics collection
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validators import OutputValidator, FeedbackGenerator
from src.metrics import MetricsCollector, AgentMetrics, OrchestratorMetrics
import time

def test_validators():
    """Test the CRITIC pattern validators"""
    print("\n" + "=" * 60)
    print("TEST 1: CRITIC Pattern Validators")
    print("=" * 60)
    
    validator = OutputValidator()
    feedback_gen = FeedbackGenerator(validator)
    
    # Test content with various quality levels
    test_content = """
# Python Async/Await Guide

## Introduction

Python's async/await syntax enables concurrent programming.

## Basic Usage

```python
async def example():
    await asyncio.sleep(1)
```

## Best Practices

Always use asyncio.create_task() for concurrency.
"""
    
    requirements = ["Introduction", "Basic Usage", "Best Practices"]
    
    print("\nRunning validation on sample content...")
    report = validator.run_full_validation(test_content, requirements)
    
    print(f"\nOverall Score: {report['overall_score']:.1%}")
    print(f"Quality Grade: {report['quality_grade']}")
    print(f"Status: {'✅ PASSED' if report['passed'] else '❌ FAILED'}")
    
    print("\nDimension Scores:")
    for dim, result in report['dimensions'].items():
        status = "✅" if result['passed'] else "❌"
        print(f"  {status} {dim.title()}: {result['score']:.1%}")
    
    if report['issues']:
        print("\nIssues Found:")
        for issue in report['issues'][:3]:  # Show first 3
            print(f"  - {issue}")
    
    print("\n✓ Validator test complete")

def test_metrics():
    """Test the metrics collection system"""
    print("\n" + "=" * 60)
    print("TEST 2: Metrics Collection System")
    print("=" * 60)
    
    collector = MetricsCollector()
    
    # Record sample agent executions
    agents = ["researcher", "writer", "critic-reviewer"]
    
    print("\nRecording agent execution metrics...")
    for i, agent in enumerate(agents):
        metrics = AgentMetrics(
            agent_name=agent,
            task_id=f"task_{i+1:03d}",
            start_time=time.time(),
            end_time=time.time() + (60 + i * 30),
            duration=60.0 + i * 30,
            quality_score=0.85 + (i * 0.05),
            token_usage=10000 + (i * 5000),
            refinement_iterations=i % 2,
            success=True
        )
        collector.record_agent_execution(metrics)
        print(f"  ✓ Recorded: {agent}")
    
    # Record sample orchestrations
    print("\nRecording orchestration metrics...")
    patterns = ["parallel", "sequential", "hub-spoke"]
    
    for i, pattern in enumerate(patterns):
        metrics = OrchestratorMetrics(
            orchestration_id=f"orch_{i+1:03d}",
            pattern=pattern,
            start_time=time.time(),
            end_time=time.time() + 300,
            total_duration=300.0,
            agents_used=["orchestrator"] + agents[:i+1],
            tasks_completed=i + 2,
            tasks_failed=0,
            average_quality=0.88 + (i * 0.02),
            total_tokens=30000 + (i * 10000),
            refinement_cycles=i
        )
        collector.record_orchestration(metrics)
        print(f"  ✓ Recorded: {pattern}")
    
    # Generate statistics
    print("\n" + "-" * 60)
    print("Agent Statistics Summary:")
    print("-" * 60)
    
    for agent in agents:
        stats = collector.get_agent_statistics(agent)
        if stats:
            print(f"\n{agent}:")
            print(f"  Executions: {stats['total_executions']}")
            print(f"  Success Rate: {stats['success_rate']:.1%}")
            print(f"  Avg Quality: {stats['average_quality']:.1%}")
    
    print("\n" + "-" * 60)
    print("Orchestration Statistics Summary:")
    print("-" * 60)
    
    for pattern in patterns:
        stats = collector.get_orchestration_statistics(pattern)
        if stats:
            print(f"\n{pattern}:")
            print(f"  Orchestrations: {stats['total_orchestrations']}")
            print(f"  Success Rate: {stats['success_rate']:.1%}")
            print(f"  Avg Quality: {stats['average_quality']:.1%}")
    
    print("\n✓ Metrics test complete")

def test_agent_configuration():
    """Test that all Stage 2 agents are configured"""
    print("\n" + "=" * 60)
    print("TEST 3: Agent Configuration")
    print("=" * 60)
    
    stage2_agents = [
        '.claude/agents/parallel-orchestrator.md',
        '.claude/agents/sequential-orchestrator.md',
        '.claude/agents/hub-orchestrator.md',
        '.claude/agents/critic-reviewer.md'
    ]
    
    print("\nChecking Stage 2 agent files...")
    all_exist = True
    for agent_file in stage2_agents:
        exists = os.path.exists(agent_file)
        status = "✓" if exists else "✗"
        print(f"  {status} {agent_file}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All Stage 2 agents configured")
    else:
        print("\n❌ Some Stage 2 agents missing")
    
    return all_exist

def test_src_modules():
    """Test that all src modules are present"""
    print("\n" + "=" * 60)
    print("TEST 4: Source Modules")
    print("=" * 60)
    
    modules = [
        'src/validators.py',
        'src/metrics.py'
    ]
    
    print("\nChecking source modules...")
    all_exist = True
    for module in modules:
        exists = os.path.exists(module)
        status = "✓" if exists else "✗"
        print(f"  {status} {module}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All source modules present")
    else:
        print("\n❌ Some source modules missing")
    
    return all_exist

def run_all_tests():
    """Run all Stage 2 tests"""
    print("\n" + "=" * 60)
    print("STAGE 2: CORE PATTERNS & OBSERVABILITY")
    print("Test Suite")
    print("=" * 60)
    
    results = {
        'validators': False,
        'metrics': False,
        'agents': False,
        'modules': False
    }
    
    try:
        # Test 1: Validators
        test_validators()
        results['validators'] = True
    except Exception as e:
        print(f"\n❌ Validator test failed: {e}")
    
    try:
        # Test 2: Metrics
        test_metrics()
        results['metrics'] = True
    except Exception as e:
        print(f"\n❌ Metrics test failed: {e}")
    
    try:
        # Test 3: Agent Configuration
        results['agents'] = test_agent_configuration()
    except Exception as e:
        print(f"\n❌ Agent configuration test failed: {e}")
    
    try:
        # Test 4: Source Modules
        results['modules'] = test_src_modules()
    except Exception as e:
        print(f"\n❌ Source modules test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    for test_name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {test_name.replace('_', ' ').title()}")
    
    if passed == total:
        print("\n🎉 Stage 2 Implementation: COMPLETE")
        print("\nWhat you've built:")
        print("  ✓ Three orchestration patterns (Parallel, Sequential, Hub-Spoke)")
        print("  ✓ CRITIC pattern for tool-based validation")
        print("  ✓ Metrics collection and reporting")
        print("  ✓ Quality assessment framework")
        print("\nReady for: Stage 3 - Cybernetic Architecture")
    else:
        print("\n⚠️  Some tests failed. Please review and fix issues.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_all_tests()
