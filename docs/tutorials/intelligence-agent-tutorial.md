# Intelligence Agent - Tutorial Guide

**Agent Type**: VSM System 4 - Strategic Planning  
**System Level**: System 4  
**Model**: Claude Opus  
**Color**: Purple  

---

## Overview

The **Intelligence Agent** (System 4) performs strategic planning by analyzing complex tasks, decomposing them into subtasks, selecting optimal execution strategies, and creating detailed execution plans.

### What It Does

- Scans project environment and analyzes context
- Decomposes complex tasks into manageable subtasks
- Selects optimal orchestration pattern (parallel/sequential/hub-spoke)
- Plans resource allocation and budgets
- Creates detailed strategic execution plans for System 3

### When to Use

✅ **Use intelligence agent when**:
- Facing complex, multi-faceted tasks requiring planning
- Need strategic decomposition before execution
- Want optimal pattern selection
- Require resource estimation and budgeting
- Building execution roadmaps

❌ **Don't use for**:
- Simple tasks (use basic orchestrator)
- Tasks already well-decomposed
- Immediate execution without planning phase

---

## Usage Example

**Your Request**:
```
"Analyze this complex task and create a strategic execution plan:
Create comprehensive Python async/await learning system including
research, tutorials, exercises, and reference documentation"
```

**What Intelligence Agent Does**:

1. **Context Analysis**:
   - Scans project structure
   - Reviews existing artifacts
   - Identifies constraints and requirements
   - Assesses complexity (Large, High difficulty)

2. **Task Decomposition**:
   ```
   Subtask 1: Research (Critical, 2hrs)
   Subtask 2: Create outline (High, 1hr)
   Subtask 3: Write tutorials (High, 3hrs)
   Subtask 4: Create exercises (Medium, 2hrs)
   Subtask 5: Build reference docs (Medium, 2hrs)
   Subtask 6: Review & validate (High, 1hr)
   ```

3. **Strategy Selection**:
   ```
   Pattern: Sequential with parallel sub-phases
   
   Rationale:
   - Phases 1-3 must be sequential (dependencies)
   - Phases 4-5 can run in parallel (independent)
   - Phase 6 validates everything (sequential)
   ```

4. **Resource Planning**:
   ```
   Agent Assignments:
   - Research: researcher
   - Outline: intelligence-agent (self)
   - Tutorials: writer
   - Exercises: writer
   - Reference: writer
   - Review: critic-reviewer
   
   Timeline: 11 hours total
   Token Budget: 150,000 tokens
   ```

5. **Risk Mitigation**:
   ```
   Risk: Code examples may not work
   - Probability: Medium
   - Mitigation: Require runnable examples
   - Contingency: Validation will catch, fix in review
   ```

**Output**: Detailed strategic plan forwarded to System 3 (control-agent) for execution

---

## Strategic Plan Output

```markdown
# Strategic Execution Plan
Task: Python async/await learning system
Planner: intelligence-agent
Date: 2024-01-15T10:00:00Z

## Context Analysis
- Scope: Large (multi-component system)
- Difficulty: High
- Estimated Duration: 11 hours
- Token Budget: 150,000

## Task Decomposition
{6 subtasks with dependencies, priorities, estimates}

## Strategy Selection
Pattern: Hybrid (Sequential with parallel sub-phases)

## Resource Plan
{Agent assignments, timeline, budget}

## Quality Gates
{Where and how to validate}

## Risk Mitigation
{3-5 identified risks with contingencies}

## Plan Approval
Recommended: YES
Policy Compliant: YES
Forward to: System 3 (Control Agent)
```

---

## Tips & Best Practices

### 1. Provide Full Context

Help intelligence agent plan optimally:
```
"Task: Create tutorial
Constraints: Must complete in 8 hours, target beginners
Requirements: Runnable examples, exercises, 90% quality"
```

### 2. Review Plans Before Execution

Intelligence agent creates plan, you can review before execution starts

### 3. Trust the Decomposition

Agent applies experience and best practices to break down complex tasks

### 4. Use for Complex Tasks

Simple tasks don't need full strategic planning - just use orchestrator

---

## Working in VSM Hierarchy

```
System 5 (Policy)
    ↓ Sets boundaries
System 4 (Intelligence) ← You are here
    ↓ Creates plan
System 3 (Control)
    ↓ Executes plan
System 2 (Coordination)
    ↓ Prevents conflicts
System 1 (Workers)
    ↓ Does work
```

Intelligence agent operates between policy (what's allowed) and execution (what gets done).

---

## Summary

The **Intelligence Agent** provides strategic planning and task decomposition for complex multi-agent workflows.

**Perfect for**: Complex project planning, resource allocation, strategy selection, and creating execution roadmaps for System 3 to execute.

---

**Try it**:
```
"Create strategic plan for: [complex multi-phase task]"
