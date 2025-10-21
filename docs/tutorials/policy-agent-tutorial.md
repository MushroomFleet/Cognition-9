# Policy Agent - Tutorial Guide

**Agent Type**: VSM System 5 - Governance & Policy  
**System Level**: System 5 (Highest)  
**Model**: Claude Opus  
**Color**: Gold  

---

## Overview

The **Policy Agent** (System 5 in the Viable System Model) defines governance, ethical boundaries, and strategic objectives for the entire multi-agent system. It's rarely invoked but critical for system integrity.

### What It Does

- Defines permissible vs prohibited actions for all agents
- Establishes ethical guidelines and boundaries
- Sets strategic objectives and organizational goals
- Monitors policy compliance across the system
- Responds to algedonic (critical) alerts

### When to Use

✅ **Use policy agent when**:
- Setting up new multi-agent systems (define policies)
- Reviewing system governance and ethics
- Investigating policy violations
- Responding to critical algedonic alerts
- Updating strategic objectives

❌ **Don't use for**:
- Day-to-day task execution
- Tactical decisions (use intelligence-agent)
- Operational work (use worker agents)

---

## Key Concepts

### Algedonic Alerts

**Algedonic** = Pain/pleasure signals for rapid escalation

Critical situations triggering immediate policy review:
- Quality score < 40% (system failure)
- Ethical boundary violation
- Security breach attempt
- Agent producing harmful content
- Resource exhaustion or infinite loops

**Response Protocol**:
1. HALT all operations
2. ISOLATE problematic agent/task
3. ESCALATE to human oversight
4. ANALYZE root cause
5. REMEDIATE and update policies

### Policy Framework

**Three Categories**:

1. **Permissible Actions** (What agents MAY do)
2. **Prohibited Actions** (What agents MUST NOT do)
3. **Ethical Guidelines** (How agents SHOULD operate)

---

## Usage Example

**Your Request**:
```
"Review and update system policies for this multi-agent research system"
```

**What the Policy Agent Does**:

1. **Policy Definition**:
   ```markdown
   ## Strategic Objectives
   1. Produce high-quality, well-sourced research
   2. Maintain efficient resource utilization
   3. Ensure ethical information dissemination
   
   ## Permissible Actions
   ✅ Research from approved sources
   ✅ Generate educational content
   ✅ Execute read-only commands
   
   ## Prohibited Actions
   ❌ Access confidential data without authorization
   ❌ Generate harmful or misleading content
   ❌ Execute destructive commands
   
   ## Quality Thresholds
   - Minimum acceptable: 80%
   - Algedonic alert: 40%
   - Auto-rejection: 60%
   ```

2. **Compliance Monitoring**:
   - Defines audit trail requirements
   - Sets review frequencies
   - Establishes escalation procedures

**Output**: `artifacts/system-policy-v{version}.md`

---

## Tips & Best Practices

### 1. Set Clear Boundaries

Be explicit about what's allowed:
```
✅ "Agents may research from: official docs, academic papers, established blogs"
❌ "Agents should research appropriate sources" (too vague)
```

### 2. Define Measurable Thresholds

```
"Quality minimum: 80%"
"Alert if: Quality < 40%"
"Auto-reject if: Quality < 60%"
```

### 3. Update Policies as System Evolves

Policies should adapt:
- Monthly reviews recommended
- After significant incidents
- When adding new capabilities

### 4. Document Rationale

Explain WHY policies exist:
```
"No destructive commands: Prevents accidental data loss"
"Citation requirements: Ensures truthfulness and accountability"
```

---

## Summary

The **Policy Agent** defines system-wide governance, ethics, and strategic direction. It's the constitutional authority for the entire multi-agent system.

**Perfect for**: System governance, ethical boundaries, strategic objectives, compliance monitoring, and responding to critical system events.

---

**Typical Usage**:
```
"Define policies for this research system ensuring ethical, high-quality output"
```

Then policies guide all other agents automatically.
