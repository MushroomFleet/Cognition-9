"""
Automated Agent Demonstration Script
====================================
Demonstrates all 11 Cognition-9 agents with sample tasks

This script simulates real agent interactions to show:
- What each agent does
- Expected inputs and outputs
- Quality validation
- Typical workflows

Run: python tests/test-agents-demo.py
"""

import sys
import os
import time
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.validators import OutputValidator
    from src.metrics import MetricsCollector, AgentMetrics
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    print("⚠️  Metrics not available - running in demo mode only")

class AgentDemo:
    """Base class for agent demonstrations"""
    
    def __init__(self, agent_name, color="white"):
        self.agent_name = agent_name
        self.color = color
        self.metrics = []
        
    def print_header(self, title):
        print("\n" + "=" * 70)
        print(f"{title}")
        print("=" * 70)
        
    def print_section(self, title):
        print("\n" + "-" * 70)
        print(f"{title}")
        print("-" * 70)
        
    def simulate_task(self, description, duration=0.5):
        """Simulate a task with progress indicator"""
        print(f"\n→ {description}")
        time.sleep(duration)
        print(f"  ✓ Completed (simulated)")
        
    def show_quality(self, score, threshold=80):
        """Display quality score with pass/fail indicator"""
        status = "✅ PASS" if score >= threshold else "❌ FAIL"
        print(f"\n  Quality Score: {score}% {status}")
        return score >= threshold

# ============================================================================
# ORCHESTRATOR AGENTS
# ============================================================================

def demo_orchestrator():
    """Demo 1: Basic Orchestrator - Coordinate multi-step workflow"""
    demo = AgentDemo("orchestrator", "purple")
    demo.print_header("DEMO 1: ORCHESTRATOR")
    
    print("\n📋 Agent: Basic Orchestrator")
    print("Use Case: Coordinate research and writing workflow")
    print("Pattern: Task decomposition → Delegation → Quality control → Synthesis")
    
    demo.print_section("USER REQUEST")
    print('Task: "Research Python async/await and create a beginner tutorial"')
    print("Expected Output: Comprehensive tutorial with examples")
    
    demo.print_section("ORCHESTRATOR: Task Analysis")
    demo.simulate_task("Analyzing user request...", 0.3)
    print("\nIdentified Subtasks:")
    print("  1. Research Phase (researcher)")
    print("     → Output: artifacts/async-research.md")
    print("     → Quality threshold: 85%")
    print("\n  2. Writing Phase (writer)")
    print("     → Input: Research findings")
    print("     → Output: artifacts/async-tutorial.md")
    print("     → Quality threshold: 85%")
    
    demo.print_section("EXECUTION: Research Phase")
    demo.simulate_task("Delegating to researcher agent...", 0.5)
    print("\nResearcher deliverables:")
    print("  ✓ 12 key concepts identified")
    print("  ✓ 8 code examples provided")
    print("  ✓ 6 sources cited")
    demo.show_quality(92, 85)
    
    demo.print_section("EXECUTION: Writing Phase")
    demo.simulate_task("Delegating to writer agent...", 0.5)
    print("\nWriter deliverables:")
    print("  ✓ Tutorial structure: Intro → Concepts → Examples → Exercises")
    print("  ✓ 5 runnable code examples")
    print("  ✓ Clear explanations for beginners")
    demo.show_quality(89, 85)
    
    demo.print_section("SYNTHESIS")
    demo.simulate_task("Integrating outputs into final deliverable...", 0.3)
    print("\nFinal Output:")
    print("  📄 artifacts/async-tutorial-final.md")
    print("  📊 Overall Quality: 90%")
    print("  ⏱️  Total Duration: ~3 hours (actual)")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Orchestrator manages multi-step workflows with quality gates")
    return True

def demo_parallel_orchestrator():
    """Demo 2: Parallel Orchestrator - Concurrent execution"""
    demo = AgentDemo("parallel-orchestrator", "orange")
    demo.print_header("DEMO 2: PARALLEL ORCHESTRATOR")
    
    print("\n📋 Agent: Parallel Orchestrator")
    print("Use Case: Research from multiple independent sources simultaneously")
    print("Pattern: Concurrent delegation → Monitor completion → Aggregate results")
    
    demo.print_section("USER REQUEST")
    print('Task: "Research async/await from 3 perspectives: academic, tutorial, production"')
    print("Benefit: 3× faster than sequential (tasks run concurrently)")
    
    demo.print_section("TASK INDEPENDENCE ANALYSIS")
    demo.simulate_task("Analyzing task dependencies...", 0.3)
    print("\nIndependence Check:")
    print("  ✓ Task 1: Academic research - INDEPENDENT")
    print("  ✓ Task 2: Tutorial research - INDEPENDENT")
    print("  ✓ Task 3: Production research - INDEPENDENT")
    print("\n→ All tasks can run in parallel!")
    
    demo.print_section("PARALLEL EXECUTION")
    print("\nDelegating all tasks simultaneously at T+0:00...")
    time.sleep(0.3)
    
    print("\n  Agent A (Academic)   → Started at 10:00:00")
    print("  Agent B (Tutorials)  → Started at 10:00:00")
    print("  Agent C (Production) → Started at 10:00:00")
    
    print("\nMonitoring concurrent execution...")
    time.sleep(0.5)
    
    print("\n  ✓ Agent B completed at 10:45:00 (45 min)")
    print("  ✓ Agent A completed at 11:10:00 (70 min)")
    print("  ✓ Agent C completed at 11:20:00 (80 min)")
    
    print("\n⏱️  Total Time: 80 minutes (longest task)")
    print("⚡ Sequential would take: 195 minutes (45+70+80)")
    print("🚀 Speedup: 2.4× faster!")
    
    demo.print_section("RESULTS AGGREGATION")
    demo.simulate_task("Synthesizing all perspectives...", 0.4)
    print("\nAggregated Output:")
    print("  📄 artifacts/parallel-async-comprehensive.md")
    print("  📊 Contains all 3 perspectives integrated")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Use parallel for independent tasks to maximize speed")
    return True

def demo_sequential_orchestrator():
    """Demo 3: Sequential Orchestrator - Pipeline with quality gates"""
    demo = AgentDemo("sequential-orchestrator", "yellow")
    demo.print_header("DEMO 3: SEQUENTIAL ORCHESTRATOR")
    
    print("\n📋 Agent: Sequential Orchestrator")
    print("Use Case: Content production pipeline with dependencies")
    print("Pattern: Stage → Quality Gate → Next Stage")
    
    demo.print_section("USER REQUEST")
    print('Task: "Create guide through: Research → Outline → Write → Review"')
    print("Key Feature: Quality gates between each stage")
    
    demo.print_section("PIPELINE DESIGN")
    print("\nStages identified:")
    print("  Stage 1: Research → artifacts/stage-1-research.md")
    print("  Stage 2: Outline  → artifacts/stage-2-outline.md")
    print("  Stage 3: Write    → artifacts/stage-3-draft.md")
    print("  Stage 4: Review   → artifacts/stage-4-final.md")
    
    demo.print_section("STAGE 1: Research")
    demo.simulate_task("Executing research phase...", 0.4)
    print("\n  Output: stage-1-research.md")
    
    print("\n  Quality Gate 1→2:")
    print("    Completeness: 9/10 ✓")
    print("    Accuracy: 10/10 ✓")
    print("    Overall: 92% ✓ PASS")
    print("\n  → Proceeding to Stage 2")
    
    demo.print_section("STAGE 2: Outline")
    demo.simulate_task("Creating detailed outline...", 0.3)
    print("\n  Output: stage-2-outline.md")
    
    print("\n  Quality Gate 2→3:")
    print("    Structure: 7/10 ⚠️")
    print("    Completeness: 6/10 ❌")
    print("    Overall: 65% ❌ FAIL")
    print("\n  → Refinement requested")
    print("  Issue: Missing 'Error Handling' section")
    
    demo.simulate_task("Refining outline with missing section...", 0.3)
    print("\n  Revised Output: stage-2-outline-v2.md")
    
    print("\n  Quality Gate 2→3 (Retry):")
    print("    Structure: 9/10 ✓")
    print("    Completeness: 9/10 ✓")
    print("    Overall: 88% ✓ PASS")
    print("\n  → Proceeding to Stage 3")
    
    demo.print_section("STAGES 3-4: Write & Review")
    demo.simulate_task("Writing complete guide...", 0.4)
    demo.simulate_task("Conducting final review...", 0.3)
    
    print("\n  All quality gates passed!")
    print("  Final output: stage-4-final.md")
    print("  Overall quality: 87%")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Sequential ensures quality at each stage before proceeding")
    return True

def demo_hub_orchestrator():
    """Demo 4: Hub Orchestrator - Multi-perspective synthesis"""
    demo = AgentDemo("hub-orchestrator", "red")
    demo.print_header("DEMO 4: HUB ORCHESTRATOR")
    
    print("\n📋 Agent: Hub Orchestrator")
    print("Use Case: Analyze topic from multiple expert perspectives, then synthesize")
    print("Pattern: Hub delegates → Spokes analyze → Hub synthesizes → Iterate if needed")
    
    demo.print_section("USER REQUEST")
    print('Task: "Analyze async/await from performance, usability, and architecture angles"')
    print("Goal: Comprehensive multi-perspective understanding")
    
    demo.print_section("HUB: Initial Delegation")
    print("\nHub assigns focus areas to specialists:")
    print("\n  Spoke 1 (Performance Expert)")
    print("    Focus: Benchmarks, optimization, overhead")
    print("    Output: spoke-1-performance.md")
    print("\n  Spoke 2 (UX Expert)")
    print("    Focus: Developer experience, API design")
    print("    Output: spoke-2-usability.md")
    print("\n  Spoke 3 (Architecture Expert)")
    print("    Focus: Design patterns, system integration")
    print("    Output: spoke-3-architecture.md")
    
    demo.simulate_task("Spokes conducting analysis...", 0.6)
    
    demo.print_section("HUB: Iteration 1 - Gap Analysis")
    print("\nReviewing all spoke outputs...")
    time.sleep(0.3)
    
    print("\n  Findings:")
    print("    ✓ Good coverage of individual perspectives")
    print("    ⚠️  Gap: Error handling not addressed by any spoke")
    print("    ⚠️  Conflict: Performance vs usability trade-offs unclear")
    
    print("\n  → Requesting targeted refinements")
    
    demo.print_section("HUB: Iteration 2 - Refinement")
    demo.simulate_task("Spokes adding error handling analysis...", 0.4)
    demo.simulate_task("Spokes clarifying trade-offs...", 0.3)
    
    print("\n  Gaps filled ✓")
    print("  Conflicts resolved ✓")
    print("  Quality sufficient ✓")
    
    demo.print_section("HUB: Final Synthesis")
    demo.simulate_task("Integrating all perspectives...", 0.4)
    
    print("\n  Synthesis Strategy:")
    print("    • Unified narrative structure")
    print("    • Cross-references between perspectives")
    print("    • Trade-offs clearly explained")
    print("    • Comprehensive understanding achieved")
    
    print("\n  Final Output: hub-final-comprehensive.md")
    print("  Quality: 91% (higher than any single spoke)")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Hub synthesis > sum of parts through iteration")
    return True

# ============================================================================
# VSM HIERARCHY AGENTS
# ============================================================================

def demo_policy_agent():
    """Demo 5: Policy Agent (System 5) - Governance"""
    demo = AgentDemo("policy-agent", "gold")
    demo.print_header("DEMO 5: POLICY AGENT (System 5)")
    
    print("\n📋 Agent: Policy Agent")
    print("VSM Level: System 5 (Highest - Governance)")
    print("Use Case: Define system-wide policies and ethical boundaries")
    print("Pattern: Rarely invoked but critical for system integrity")
    
    demo.print_section("USER REQUEST")
    print('Task: "Define policies for research system ensuring ethical, quality output"')
    
    demo.print_section("POLICY DEFINITION")
    demo.simulate_task("Analyzing system requirements...", 0.3)
    
    print("\n  Strategic Objectives:")
    print("    1. Produce high-quality, well-sourced research")
    print("    2. Maintain efficient resource utilization")
    print("    3. Ensure ethical information dissemination")
    
    print("\n  Permissible Actions (✅):")
    print("    ✅ Research from official docs, academic papers")
    print("    ✅ Generate educational content")
    print("    ✅ Execute read-only commands")
    
    print("\n  Prohibited Actions (❌):")
    print("    ❌ Access confidential data without authorization")
    print("    ❌ Generate harmful or misleading content")
    print("    ❌ Execute destructive commands")
    
    print("\n  Quality Thresholds:")
    print("    • Minimum acceptable: 80%")
    print("    • Algedonic alert: 40% (critical)")
    print("    • Auto-rejection: 60%")
    
    demo.print_section("ALGEDONIC ALERT SIMULATION")
    print("\nScenario: Agent produces output with 35% quality")
    time.sleep(0.2)
    
    print("\n  🚨 ALGEDONIC ALERT TRIGGERED!")
    print("    1. HALT all operations immediately")
    print("    2. ISOLATE problematic agent")
    print("    3. ESCALATE to human oversight")
    print("    4. ANALYZE root cause")
    print("    5. REMEDIATE before resuming")
    
    print("\n  Output: system-policy-v1.0.md")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Policy agent defines boundaries all other agents must follow")
    return True

def demo_intelligence_agent():
    """Demo 6: Intelligence Agent (System 4) - Strategic Planning"""
    demo = AgentDemo("intelligence-agent", "purple")
    demo.print_header("DEMO 6: INTELLIGENCE AGENT (System 4)")
    
    print("\n📋 Agent: Intelligence Agent")
    print("VSM Level: System 4 (Strategic Planning)")
    print("Use Case: Analyze complex tasks and create execution plans")
    print("Pattern: Context → Decomposition → Strategy → Resource Planning")
    
    demo.print_section("USER REQUEST")
    print('Task: "Create comprehensive Python async/await learning system"')
    print("Complexity: Large (tutorials, exercises, reference docs)")
    
    demo.print_section("CONTEXT ANALYSIS")
    demo.simulate_task("Scanning project environment...", 0.3)
    
    print("\n  Project Structure: Standard with docs/, src/, tests/")
    print("  Existing Artifacts: None related to async/await")
    print("  Constraints: Must target intermediate developers")
    print("  Complexity Assessment: Large, High difficulty")
    print("  Estimated Duration: 11 hours")
    print("  Token Budget: 150,000 tokens")
    
    demo.print_section("TASK DECOMPOSITION")
    print("\nBreaking into manageable subtasks:")
    print("\n  Subtask 1: Research (Critical, 2hrs)")
    print("    → Gather information on async/await")
    print("\n  Subtask 2: Outline (High, 1hr)")
    print("    → Create learning path structure")
    print("\n  Subtask 3: Tutorials (High, 3hrs)")
    print("    → Write step-by-step guides")
    print("\n  Subtask 4: Exercises (Medium, 2hrs)")
    print("    → Create practice problems")
    print("\n  Subtask 5: Reference (Medium, 2hrs)")
    print("    → Build API documentation")
    print("\n  Subtask 6: Review (High, 1hr)")
    print("    → Quality validation")
    
    demo.print_section("STRATEGY SELECTION")
    print("\n  Pattern: Hybrid (Sequential + Parallel)")
    print("\n  Rationale:")
    print("    • Phases 1-3: Sequential (dependencies)")
    print("    • Phases 4-5: Parallel (independent)")
    print("    • Phase 6: Sequential (validates all)")
    
    demo.print_section("RESOURCE PLAN")
    print("\n  Agent Assignments:")
    print("    Research → researcher")
    print("    Outline → intelligence-agent (self)")
    print("    Tutorials → writer")
    print("    Exercises → writer")
    print("    Reference → writer")
    print("    Review → critic-reviewer")
    
    print("\n  Timeline: 11 hours total")
    print("  Quality Gates: 3 checkpoints")
    
    demo.print_section("RISK MITIGATION")
    print("\n  Risk 1: Code examples may not work")
    print("    Probability: Medium")
    print("    Mitigation: Require runnable examples")
    print("    Contingency: Validation will catch issues")
    
    print("\n  Output: strategic-execution-plan.md")
    print("  Forward to: System 3 (Control Agent) for execution")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Intelligence creates detailed plans for System 3 to execute")
    return True

def demo_control_agent():
    """Demo 7: Control Agent (System 3) - Execution Management"""
    demo = AgentDemo("control-agent", "blue")
    demo.print_header("DEMO 7: CONTROL AGENT (System 3)")
    
    print("\n📋 Agent: Control Agent")
    print("VSM Level: System 3 (Execution Supervision)")
    print("Use Case: Execute strategic plans with quality enforcement")
    print("Pattern: Receive plan → Delegate → Enforce gates → Monitor → Report")
    
    demo.print_section("PLAN RECEPTION")
    print("\n  Receiving plan from System 4 (Intelligence Agent)...")
    demo.simulate_task("Validating plan completeness...", 0.2)
    
    print("\n  Plan Summary:")
    print("    Pattern: Sequential")
    print("    Subtasks: 3 (Research, Writing, Review)")
    print("    Duration: 3.5 hours")
    print("    Quality Threshold: 80%")
    
    demo.print_section("WORKER DELEGATION")
    print("\n  Subtask 1: Research")
    print("    Assigned to: researcher")
    demo.simulate_task("Delegating research task...", 0.3)
    print("    Status: COMPLETED")
    print("    Output: artifacts/async-research.md")
    
    demo.print_section("QUALITY GATE ENFORCEMENT")
    print("\n  Gate 1: Research Complete")
    demo.simulate_task("Running quality validation...", 0.3)
    
    print("\n    Criteria: 10+ concepts, 5+ sources")
    print("    Threshold: 75%")
    print("    Actual Score: 85%")
    print("    Status: ✅ PASSED")
    print("\n    → Proceeding to writing phase")
    
    print("\n  Subtask 2: Content Creation")
    print("    Assigned to: writer")
    demo.simulate_task("Delegating writing task...", 0.3)
    print("    Status: COMPLETED")
    
    print("\n  Gate 2: Content Complete (First Attempt)")
    demo.simulate_task("Running quality validation...", 0.3)
    
    print("\n    Threshold: 80%")
    print("    Actual Score: 72%")
    print("    Status: ❌ FAILED")
    print("    Issue: Missing error handling section")
    print("\n    → Requesting refinement")
    
    demo.simulate_task("Writer refining content...", 0.3)
    
    print("\n  Gate 2: Content Complete (After Refinement)")
    print("    Actual Score: 86%")
    print("    Status: ✅ PASSED")
    print("\n    → Proceeding to review")
    
    demo.print_section("EXECUTION REPORTING")
    demo.simulate_task("Generating final report...", 0.2)
    
    print("\n  Performance Metrics:")
    print("    Planned Duration: 3.5 hours")
    print("    Actual Duration: 3.67 hours (+5%)")
    print("    Quality Achieved: 86%")
    print("    Refinement Cycles: 1")
    
    print("\n  Status: ✅ SUCCESS")
    print("  Report to System 4: Execution complete")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Control enforces quality gates and manages execution")
    return True

def demo_coordination_agent():
    """Demo 8: Coordination Agent (System 2) - Conflict Prevention"""
    demo = AgentDemo("coordination-agent", "teal")
    demo.print_header("DEMO 8: COORDINATION AGENT (System 2)")
    
    print("\n📋 Agent: Coordination Agent")
    print("VSM Level: System 2 (Conflict Prevention)")
    print("Use Case: Manage parallel workers and prevent conflicts")
    print("Pattern: Monitor → Detect conflicts → Resolve → Synchronize")
    
    demo.print_section("SCENARIO: Parallel Research & Writing")
    print("\n  Active Workers:")
    print("    • researcher: Writing to artifacts/research.md")
    print("    • writer: Needs to read artifacts/research.md")
    print("    • critic: Waiting for final output")
    
    demo.print_section("ACTIVITY MONITORING")
    demo.simulate_task("Monitoring worker activities...", 0.3)
    
    print("\n  Coordination Board:")
    print("    researcher: ACTIVE (writing research.md)")
    print("    writer: BLOCKED (waiting for research.md)")
    print("    critic: IDLE")
    
    demo.print_section("CONFLICT DETECTION")
    print("\n  🔍 Potential Conflict Detected!")
    print("    Type: Resource contention")
    print("    Description: Writer attempting to read file still being written")
    print("    Severity: Medium")
    
    demo.print_section("RESOURCE MANAGEMENT")
    print("\n  File: artifacts/research.md")
    print("    Status: LOCKED (write access)")
    print("    Held by: researcher")
    print("    Queue: writer (read access pending)")
    
    demo.print_section("CONFLICT RESOLUTION")
    print("\n  Strategy: DEFER")
    print("    Action: Block writer until researcher completes")
    
    demo.simulate_task("Notifying writer of delay...", 0.2)
    print('    Message: "Writer, research.md not ready. ETA: 15 minutes"')
    
    demo.simulate_task("Researcher completes...", 0.4)
    
    demo.print_section("SYNCHRONIZATION")
    print("\n  Sync Point: Writer needs research output")
    print("    Provider: researcher")
    print("    Status: ✅ READY")
    
    demo.simulate_task("Signaling writer to proceed...", 0.2)
    print('    Message: "Writer, dependency satisfied. Proceed."')
    
    print("\n  Coordination Board (Updated):")
    print("    researcher: COMPLETE")
    print("    writer: ACTIVE")
    print("    critic: WAITING")
    
    print("\n  ✅ Conflict resolved - No resource collisions")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Coordination prevents conflicts between parallel workers")
    return True

# ============================================================================
# SPECIALIST AGENTS
# ============================================================================

def demo_researcher():
    """Demo 9: Researcher - Information Gathering Specialist"""
    demo = AgentDemo("researcher", "blue")
    demo.print_header("DEMO 9: RESEARCHER")
    
    print("\n📋 Agent: Researcher")
    print("Specialization: Information gathering and synthesis")
    print("Use Case: Comprehensive research from multiple sources")
    print("Pattern: Scope → Sources → Collect → Analyze → Report")
    
    demo.print_section("USER REQUEST")
    print('Task: "Research Python async/await - concepts, best practices, pitfalls"')
    print("Depth: Comprehensive (8+ sources)")
    
    demo.print_section("SCOPE DEFINITION")
    demo.simulate_task("Defining research questions...", 0.2)
    
    print("\n  Key Questions:")
    print("    1. What is async/await fundamentally?")
    print("    2. When should it be used vs alternatives?")
    print("    3. What are proven best practices?")
    print("    4. What are common pitfalls?")
    
    demo.print_section("SOURCE IDENTIFICATION")
    print("\n  Source Categories:")
    print("    • Official documentation (Python docs)")
    print("    • Academic papers (PEPs)")
    print("    • Tutorial sites (Real Python)")
    print("    • Production examples (GitHub)")
    
    demo.simulate_task("Gathering information from 12 sources...", 0.8)
    
    demo.print_section("ANALYSIS & SYNTHESIS")
    print("\n  Key Findings:")
    print("\n    Finding 1: Async is for I/O-bound tasks")
    print("      Evidence: PEP 492, benchmarks")
    print("      Credibility: High")
    print("      Confidence: 95%")
    
    print("\n    Finding 2: Use create_task() for concurrency")
    print("      Evidence: AsyncIO docs, tutorials")
    print("      Credibility: High")
    print("      Confidence: 90%")
    
    print("\n    Finding 3: Context managers essential")
    print("      Evidence: Production case studies")
    print("      Credibility: High")
    print("      Confidence: 85%")
    
    print("\n  Themes Identified:")
    print("    • When to use async (vs threading/multiprocessing)")
    print("    • Error handling patterns")
    print("    • Performance characteristics")
    
    demo.print_section("REPORT GENERATION")
    print("\n  Output Structure:")
    print("    ✓ Executive Summary")
    print("    ✓ 15 Key Findings (with citations)")
    print("    ✓ Detailed Analysis by Theme")
    print("    ✓ Conflicting Viewpoints")
    print("    ✓ Source Bibliography")
    
    print("\n  Output: artifacts/async-research-report.md")
    print("  Overall Confidence: 88%")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Researcher provides well-sourced, synthesized information")
    return True

def demo_writer():
    """Demo 10: Writer - Content Creation Specialist"""
    demo = AgentDemo("writer", "green")
    demo.print_header("DEMO 10: WRITER")
    
    print("\n📋 Agent: Writer")
    print("Specialization: Content synthesis and technical writing")
    print("Use Case: Transform research into structured documents")
    print("Pattern: Plan → Organize → Write → Examples → Polish")
    
    demo.print_section("USER REQUEST")
    print('Task: "Write beginner tutorial using research in artifacts/research.md"')
    print("Format: Tutorial with step-by-step examples")
    print("Audience: Intermediate Python developers")
    
    demo.print_section("CONTENT PLANNING")
    demo.simulate_task("Reviewing research findings...", 0.3)
    
    print("\n  Key Messages Identified:")
    print("    • Async enables concurrent I/O operations")
    print("    • Use for network/file/database operations")
    print("    • create_task() enables true concurrency")
    
    print("\n  Structure Chosen: Tutorial")
    print("    1. Introduction (what & why)")
    print("    2. Prerequisites")
    print("    3. Step 1: First coroutine")
    print("    4. Step 2: Multiple concurrent tasks")
    print("    5. Best practices")
    print("    6. Summary")
    
    demo.print_section("WRITING")
    demo.simulate_task("Creating introduction...", 0.3)
    demo.simulate_task("Writing step-by-step instructions...", 0.4)
    
    print("\n  Example Code Generated:")
    print("""
    ```python
    import asyncio
    
    async def fetch_data():
        \"\"\"Simple coroutine\"\"\"
        print("Starting fetch...")
        await asyncio.sleep(2)
        print("Fetch complete!")
        return {"data": "example"}
    
    # To run: asyncio.run(fetch_data())
    ```
    """)
    
    print("  ✓ Code example is runnable")
    print("  ✓ Comments explain key points")
    print("  ✓ Clear for beginners")
    
    demo.print_section("POLISH")
    demo.simulate_task("Reviewing flow and clarity...", 0.2)
    
    print("\n  Quality Check:")
    print("    ✓ Logical progression (simple → complex)")
    print("    ✓ Clear hierarchy with headers")
    print("    ✓ Scannable (bullets, code blocks)")
    print("    ✓ Consistent terminology")
    
    print("\n  Output: artifacts/async-tutorial.md")
    print("  Length: ~3,000 words")
    print("  Quality: 89%")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Writer transforms research into clear, structured content")
    return True

def demo_critic_reviewer():
    """Demo 11: Critic-Reviewer - Quality Validation Specialist"""
    demo = AgentDemo("critic-reviewer", "cyan")
    demo.print_header("DEMO 11: CRITIC-REVIEWER")
    
    print("\n📋 Agent: Critic-Reviewer")
    print("Specialization: Tool-based quality validation (CRITIC pattern)")
    print("Use Case: Objective assessment using external validation tools")
    print("Pattern: Read artifact → Run validators → Score → Generate feedback")
    
    demo.print_section("USER REQUEST")
    print('Task: "Review artifacts/async-tutorial.md and provide quality feedback"')
    print("Method: Tool-based validation (not subjective opinion)")
    
    demo.print_section("VALIDATION EXECUTION")
    demo.simulate_task("Running validation tools...", 0.5)
    
    if METRICS_AVAILABLE:
        print("\n  Using: src/validators.py")
    else:
        print("\n  Using: Built-in validation (demo mode)")
    
    demo.print_section("DIMENSIONAL ANALYSIS")
    print("\n  Structure: 85% ✅")
    print("    • Proper header hierarchy")
    print("    • Code blocks formatted correctly")
    print("    • Good section organization")
    
    print("\n  Citations: 45% ❌")
    print("    • 12 factual claims found")
    print("    • Only 3 citations provided")
    print("    • Critical performance claims lack sources")
    
    print("\n  Completeness: 75% ⚠️")
    print("    • Covers 6/8 required topics")
    print("    • Missing: 'Error Handling' section")
    print("    • Missing: 'Testing Strategies' section")
    
    print("\n  Code Quality: 95% ✅")
    print("    • All blocks have language identifiers")
    print("    • Examples appear runnable")
    print("    • Good commenting")
    
    demo.print_section("OVERALL ASSESSMENT")
    print("\n  Overall Score: 75%")
    print("  Quality Grade: C")
    print("  Status: ⚠️  NEEDS REFINEMENT")
    print("  Decision: Request targeted improvements")
    
    demo.print_section("FEEDBACK GENERATION")
    print("\n  Critical Issues:")
    print("    1. Performance claims need citations (lines 45-52)")
    print("    2. Missing 'Error Handling' section (required)")
    print("    3. Missing 'Testing Strategies' section (required)")
    
    print("\n  Refinement Instructions:")
    print("    For writer agent:")
    print("    1. Add citations for performance claims")
    print("    2. Create 'Error Handling' section with try/except examples")
    print("    3. Add 'Testing Strategies' section with pytest-asyncio")
    print("    4. Review other factual statements for citation opportunities")
    
    print("\n  Revised output should be: artifacts/async-tutorial-v2.md")
    
    demo.print_section("REFINEMENT CYCLE")
    demo.simulate_task("Writer addressing feedback...", 0.6)
    demo.simulate_task("Re-running validation...", 0.4)
    
    print("\n  Updated Scores:")
    print("    Structure: 85% ✅")
    print("    Citations: 78% ✅")
    print("    Completeness: 95% ✅")
    print("    Code Quality: 95% ✅")
    
    print("\n  Overall Score: 88%")
    print("  Status: ✅ APPROVED")
    
    print("\n✅ Demo Complete")
    print("\n💡 Key Takeaway: Critic uses objective tools for reliable quality assessment")
    return True

# ============================================================================
# MAIN RUNNER
# ============================================================================

def run_all_demos():
    """Run all agent demonstrations"""
    print("\n" + "=" * 70)
    print(" " * 15 + "COGNITION-9 AGENT DEMONSTRATIONS")
    print("=" * 70)
    print("\nThis script demonstrates all 11 agents with sample tasks")
    print("Each demo shows: inputs, processing, outputs, and quality metrics")
    print("\nEstimated time: 5-8 minutes")
    
    # Track results
    demos = [
        ("Orchestrator", demo_orchestrator),
        ("Parallel Orchestrator", demo_parallel_orchestrator),
        ("Sequential Orchestrator", demo_sequential_orchestrator),
        ("Hub Orchestrator", demo_hub_orchestrator),
        ("Policy Agent (System 5)", demo_policy_agent),
        ("Intelligence Agent (System 4)", demo_intelligence_agent),
        ("Control Agent (System 3)", demo_control_agent),
        ("Coordination Agent (System 2)", demo_coordination_agent),
        ("Researcher", demo_researcher),
        ("Writer", demo_writer),
        ("Critic-Reviewer", demo_critic_reviewer)
    ]
    
    results = []
    
    print("\n" + "=" * 70)
    print("Starting demonstrations...")
    print("=" * 70)
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            print(f"\n[{i}/11] Running {name} demo...")
            success = demo_func()
            results.append((name, success))
            time.sleep(0.5)  # Brief pause between demos
        except Exception as e:
            print(f"\n❌ Error in {name} demo: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print(" " * 25 + "DEMO SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nDemos Completed: {successful}/{total}")
    print("\nResults:")
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
    
    if successful == total:
        print("\n🎉 All agent demonstrations completed successfully!")
        print("\n📚 Next Steps:")
        print("  1. Review detailed tutorials in docs/tutorials/")
        print("  2. Try agents with real tasks in Claude Code")
        print("  3. Run stage tests: python tests/test-stage2.py")
        print("  4. Read RUNNING-TESTS.md for comprehensive guide")
    else:
        print(f"\n⚠️  {total - successful} demo(s) failed")
        print("  Check error messages above for details")
    
    print("\n" + "=" * 70)
    
    return successful == total

def run_single_demo(demo_number):
    """Run a specific demo by number"""
    demos = {
        1: ("Orchestrator", demo_orchestrator),
        2: ("Parallel Orchestrator", demo_parallel_orchestrator),
        3: ("Sequential Orchestrator", demo_sequential_orchestrator),
        4: ("Hub Orchestrator", demo_hub_orchestrator),
        5: ("Policy Agent", demo_policy_agent),
        6: ("Intelligence Agent", demo_intelligence_agent),
        7: ("Control Agent", demo_control_agent),
        8: ("Coordination Agent", demo_coordination_agent),
        9: ("Researcher", demo_researcher),
        10: ("Writer", demo_writer),
        11: ("Critic-Reviewer", demo_critic_reviewer)
    }
    
    if demo_number not in demos:
        print(f"❌ Invalid demo number: {demo_number}")
        print(f"   Valid range: 1-{len(demos)}")
        return False
    
    name, demo_func = demos[demo_number]
    print(f"\nRunning {name} demo...")
    
    try:
        success = demo_func()
        if success:
            print(f"\n✅ {name} demo completed successfully")
        return success
    except Exception as e:
        print(f"\n❌ Error in {name} demo: {e}")
        return False

def print_usage():
    """Print usage instructions"""
    print("""
Cognition-9 Agent Demonstration Script

Usage:
  python tests/test-agents-demo.py [demo_number]

Examples:
  python tests/test-agents-demo.py          # Run all demos
  python tests/test-agents-demo.py 1        # Run demo 1 only
  python tests/test-agents-demo.py 5        # Run demo 5 only

Available Demos:
  1.  Orchestrator
  2.  Parallel Orchestrator
  3.  Sequential Orchestrator
  4.  Hub Orchestrator
  5.  Policy Agent (System 5)
  6.  Intelligence Agent (System 4)
  7.  Control Agent (System 3)
  8.  Coordination Agent (System 2)
  9.  Researcher
  10. Writer
  11. Critic-Reviewer

For detailed information, see:
  - docs/tutorials/AGENT-TUTORIALS-INDEX.md
  - docs/RUNNING-TESTS.md
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
        else:
            try:
                demo_num = int(sys.argv[1])
                run_single_demo(demo_num)
            except ValueError:
                print(f"❌ Invalid argument: {sys.argv[1]}")
                print("   Use a number (1-11) or --help for usage")
    else:
        run_all_demos()
