# Control Agent - Tutorial Guide

**Agent Type**: VSM System 3 - Execution Supervision  
**System Level**: System 3  
**Model**: Claude Opus  
**Color**: Blue  

---

## Overview

The **Control Agent** (System 3) manages execution of strategic plans from System 4, enforcing quality gates, monitoring performance, resolving issues, and reporting progress.

### What It Does

- Receives and validates strategic plans from System 4
- Delegates subtasks to worker agents per plan
- Enforces quality gates between stages
- Monitors execution metrics and progress
- Resolves issues or escalates to System 4
- Reports completion and archives results

### When to Use

✅ **Use control agent when**:
- Executing complex strategic plans
- Need strict quality enforcement
- Want comprehensive execution monitoring
- Require issue resolution and escalation
- Managing critical workflows with accountability

❌ **Don't use for**:
- Planning (use intelligence-agent)
- Simple task execution (use orchestrator)
- Policy definition (use policy-agent)

---

## Usage Example

**Your Request**:
```
"Execute this strategic plan with strict quality enforcement"
```

**What Control Agent Does**:

1. **Plan Reception**:
   - Validates plan completeness
   - Verifies agent availability
   - Initializes metrics collection
   - Creates execution log

2. **Worker Delegation** (per plan):
   ```
   Subtask 1: Research
   - Delegate to: researcher
   - Quality threshold: 85%
   - Monitor execution
   
   Quality Gate 1:
   - Check output: 92% ✓ PASS
   - Proceed to next stage
   
   Subtask 2: Writing
   - Delegate to: writer
   - Quality threshold: 85%
   
   Quality Gate 2:
   - Check output: 76% ✗ FAIL
   - Request refinement
   - Re-check: 89% ✓ PASS
   ```

3. **Performance Tracking**:
   ```
   Planned: 3.5 hours
   Actual: 3.67 hours (+5% variance)
   Quality: 89% (exceeded target 85%)
   Refinements: 1 cycle
   ```

4. **Final Report to System 4**:
   ```
   Status: SUCCESS
   Quality: 89%
   Duration: 3h 40m
   All gates passed
   ```

**Output**: Complete execution log with metrics

---

## Quality Gate Enforcement

### How Gates Work

```markdown
Gate 1→2: Research Complete
- Criteria: 10+ concepts, 5+ sources
- Threshold: 75%
- Actual: 85% → PASS ✓
- Action: Proceed to outline

Gate 2→3: Outline Complete
- Criteria: Complete structure, logical flow
- Threshold: 80%
- Actual: 68% → FAIL ✗
- Action: Request refinement
- After refinement: 84% → PASS ✓
```

### Gate Actions

- **PASS**: Proceed to next stage
- **FAIL**: Request targeted refinement
- **CRITICAL FAIL** (<40%): Escalate to System 4 for replanning

---

## Tips & Best Practices

### 1. Trust the Quality Process

Control agent will:
- Enforce all quality gates strictly
- Request refinements when needed
- Not proceed with substandard work

### 2. Monitor Execution Logs

Review `logs/executions/` to understand:
- What happened at each stage
- Why refinements requested
- Where time spent

### 3. Escalation is Normal

If plan unfeasible, control agent escalates to System 4:
- Not a failure
- Triggers replanning
- Ensures realistic execution

---

## Working in VSM Hierarchy

```
System 4 (Intelligence)
    ↓ Sends plan
System 3 (Control) ← You are here
    ↓ Manages execution
System 2 (Coordination)
    ↓ Prevents conflicts
System 1 (Workers)
    ↓ Executes tasks
```

Control agent is the executor of strategic vision.

---

## Summary

The **Control Agent** manages plan execution with strict quality enforcement and comprehensive monitoring.

**Perfect for**: Complex plan execution, quality-critical workflows, accountability requirements, and ensuring strategic plans execute correctly.

---

**Try it**:
```
"Execute this plan with quality enforcement: [strategic plan]"
