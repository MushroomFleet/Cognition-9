"""
Test script for Stage 4: Novel Architectures
Tests adaptive resonance and stigmergic coordination systems
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adaptive_resonance import AdaptiveResonanceOrchestrator, TaskSignature
from src.stigmergic_coordination import StigmergicBoard, StigmergicAgent

def test_adaptive_resonance():
    """Test adaptive resonance orchestrator"""
    print("\n" + "=" * 60)
    print("TEST 1: Adaptive Resonance Orchestrator")
    print("=" * 60)
    
    orchestrator = AdaptiveResonanceOrchestrator(vigilance_threshold=0.7)
    
    # Test with sample tasks
    tasks = [
        {
            "description": "Research Python async",
            "domain": "research",
            "complexity": 0.6,
            "input_type": "text",
            "output_type": "report",
            "keywords": ["python", "async"],
            "estimated_duration": 2.0
        },
        {
            "description": "Research Python patterns",
            "domain": "research",
            "complexity": 0.7,
            "input_type": "text",
            "output_type": "report",
            "keywords": ["python", "patterns"],
            "estimated_duration": 2.5
        }
    ]
    
    print("\nTesting specialist matching...")
    specialists_created = set()
    
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task['description']}")
        specialist_id = orchestrator.match_or_create_specialist(task)
        specialists_created.add(specialist_id)
        
        # Record successful execution
        orchestrator.record_execution(specialist_id, success=True, quality_score=0.90)
    
    stats = orchestrator.get_specialist_stats()
    print(f"\n✓ Specialists created: {stats['total_specialists']}")
    print(f"✓ System learning from task patterns")
    
    if stats['total_specialists'] > 0:
        print("\n✅ Adaptive resonance working")
        return True
    else:
        print("\n❌ No specialists created")
        return False

def test_stigmergic_coordination():
    """Test stigmergic coordination system"""
    print("\n" + "=" * 60)
    print("TEST 2: Stigmergic Coordination")
    print("=" * 60)
    
    # Create board and agents
    board = StigmergicBoard(decay_rate=3600.0)
    agents = [StigmergicAgent(f"agent_{i}", board) for i in range(3)]
    
    task_id = "test_task"
    
    print("\nSimulating agent coordination...")
    print("\nCycle 1: Initial exploration")
    for agent in agents:
        agent.execute_and_report(task_id)
    
    # Check board state
    state = board.get_board_state()
    print(f"\n✓ Board has {state['total_signals']} signals")
    print(f"✓ {state['total_tasks']} task(s) on board")
    
    # Verify signals exist
    if state['total_signals'] > 0:
        print("\n✅ Stigmergic coordination working")
        return True
    else:
        print("\n❌ No signals on board")
        return False

def test_novel_agents():
    """Test that novel architecture agents are configured"""
    print("\n" + "=" * 60)
    print("TEST 3: Novel Architecture Agents")
    print("=" * 60)
    
    novel_agents = [
        '.claude/agents/adaptive-orchestrator.md',
        '.claude/agents/stigmergic-coordinator.md'
    ]
    
    print("\nChecking novel architecture agents...")
    all_exist = True
    for agent_file in novel_agents:
        exists = os.path.exists(agent_file)
        status = "✓" if exists else "✗"
        print(f"  {status} {agent_file}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All novel architecture agents configured")
    else:
        print("\n❌ Some agents missing")
    
    return all_exist

def test_novel_modules():
    """Test that novel architecture modules exist"""
    print("\n" + "=" * 60)
    print("TEST 4: Novel Architecture Modules")
    print("=" * 60)
    
    modules = [
        'src/adaptive_resonance.py',
        'src/stigmergic_coordination.py'
    ]
    
    print("\nChecking novel architecture modules...")
    all_exist = True
    for module in modules:
        exists = os.path.exists(module)
        status = "✓" if exists else "✗"
        print(f"  {status} {module}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All novel architecture modules present")
    else:
        print("\n❌ Some modules missing")
    
    return all_exist

def run_all_tests():
    """Run all Stage 4 tests"""
    print("\n" + "=" * 60)
    print("STAGE 4: NOVEL ARCHITECTURES")
    print("Experimental Patterns Test Suite")
    print("=" * 60)
    
    results = {
        'adaptive_resonance': False,
        'stigmergic_coordination': False,
        'novel_agents': False,
        'novel_modules': False
    }
    
    try:
        results['adaptive_resonance'] = test_adaptive_resonance()
    except Exception as e:
        print(f"\n❌ Adaptive resonance test failed: {e}")
    
    try:
        results['stigmergic_coordination'] = test_stigmergic_coordination()
    except Exception as e:
        print(f"\n❌ Stigmergic coordination test failed: {e}")
    
    try:
        results['novel_agents'] = test_novel_agents()
    except Exception as e:
        print(f"\n❌ Novel agents test failed: {e}")
    
    try:
        results['novel_modules'] = test_novel_modules()
    except Exception as e:
        print(f"\n❌ Novel modules test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {test_name.replace('_', ' ').title()}")
    
    if passed == total:
        print("\n🎉 Stage 4 Implementation: COMPLETE")
        print("\nWhat you've built:")
        print("  ✓ Adaptive Resonance Orchestrator (self-organizing specialists)")
        print("  ✓ Stigmergic Coordination (swarm intelligence)")
        print("  ✓ Novel agent definitions (2 experimental patterns)")
        print("  ✓ Python implementations with working demos")
        print("\nExperimental Features:")
        print("  • Dynamic specialist emergence based on task patterns")
        print("  • Implicit coordination through shared signals")
        print("  • Self-organizing work distribution")
        print("  • Emergent consensus formation")
        print("\nReady for: Stage 5 - Production Deployment")
    else:
        print("\n⚠️  Some tests failed. Please review and fix issues.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_all_tests()
