# Hub Orchestrator - Tutorial Guide

**Agent Type**: Orchestration Pattern - Multi-Perspective Synthesis  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Red  

---

## Overview

The **Hub Orchestrator** coordinates multiple specialists providing different perspectives on the same topic, then synthesizes their insights into a cohesive whole through iterative refinement.

### What It Does

- Delegates same topic to multiple specialists with different focuses
- Collects diverse perspectives
- Identifies gaps and conflicts between perspectives
- Requests targeted refinements
- Synthesizes all viewpoints into unified analysis

### When to Use

✅ **Use hub orchestrator when**:
- Need multiple expert perspectives on same topic
- Want comprehensive multi-angle analysis
- Synthesis of diverse viewpoints required
- Gaps or conflicts need identification and resolution
- Example: Analyze topic from performance, usability, and security angles

❌ **Don't use for**:
- Independent tasks (use parallel-orchestrator)
- Linear pipelines (use sequential-orchestrator)
- Single perspective sufficient (use basic orchestrator)

---

## Usage Example

**Your Request**:
```
"Analyze Python async/await from three perspectives:
1. Performance characteristics and optimization
2. Developer experience and usability
3. Architecture patterns and design"
```

**Hub-and-Spoke Execution**:
```
Hub (Iteration 1)
├── Spoke 1: Performance Specialist
│   └── Output: artifacts/spoke-1-performance.md
├── Spoke 2: UX Specialist
│   └── Output: artifacts/spoke-2-usability.md
└── Spoke 3: Architecture Specialist
    └── Output: artifacts/spoke-3-architecture.md

Hub Synthesis
├── Reviews all three perspectives
├── Identifies: Gap in error handling across all
├── Notes: Conflict between performance vs usability
└── Requests refinement

Hub (Iteration 2)
├── Spoke 1: Add error handling performance impact
├── Spoke 2: Clarify usability trade-offs
└── Spoke 3: Update patterns for error handling

Hub Final Synthesis
└── Output: artifacts/hub-final-comprehensive-analysis.md
```

**Result**: Comprehensive analysis integrating all perspectives with conflicts resolved.

---

## Key Features

### Gap Analysis
Identifies missing information across all perspectives

### Conflict Resolution
When perspectives disagree, hub analyzes and resolves

### Iterative Refinement
Maximum 3 iterations to refine quality

### Synthesis Quality
Integrated output > sum of individual parts

---

## Tips & Best Practices

### 1. Choose Complementary Perspectives

✅ **Good**:
```
"Analyze from: technical accuracy, practical usability, business value"
```

❌ **Redundant**:
```
"Analyze from: technical A, technical B, technical C"
(Too similar, use parallel instead)
```

### 2. Allow Iteration

Hub-spoke benefits from refinement:
```
"Analyze and iterate until comprehensive (max 3 cycles)"
```

### 3. Trust Synthesis

Hub will:
- Integrate perspectives intelligently
- Resolve conflicts with evidence
- Create unified narrative

---

## Summary

**Perfect for**: Multi-perspective analysis, comprehensive topic coverage, expert synthesis, and integrating diverse viewpoints into cohesive understanding.

---

**Ready to try?**:
```
"Analyze [topic] from performance, usability, and architecture perspectives"
