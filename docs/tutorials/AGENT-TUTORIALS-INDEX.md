# Agent Tutorials - Complete Index

This document provides quick-start guidance for all 13 agents. For detailed tutorials, see individual tutorial files.

---

## Quick Reference: All 13 Agents

### 📋 Detailed Tutorials Available

1. **[Orchestrator](./orchestrator-tutorial.md)** ✅ - Complete tutorial
2. **[Researcher](./researcher-tutorial.md)** ✅ - Complete tutorial
3. **[Writer](./writer-tutorial.md)** - See agent file: `.claude/agents/writer.md`

---

## Remaining Agent Quick Starts

For agents 4-13, the agent files in `.claude/agents/` contain complete specifications. Here's how to use each:

### VSM Hierarchy Agents

#### 4. Policy Agent (System 5)
**File**: `.claude/agents/policy-agent.md`  
**Use for**: Governance, ethical boundaries, policy compliance  
**Key feature**: Algedonic alerts for critical deviations  
**Example**: "Check if this task complies with system policies"

#### 5. Intelligence Agent (System 4)
**File**: `.claude/agents/intelligence-agent.md`  
**Use for**: Strategic planning, task decomposition, resource planning  
**Key feature**: Creates detailed execution plans  
**Example**: "Analyze this complex task and create an execution plan"

#### 6. Control Agent (System 3)
**File**: `.claude/agents/control-agent.md`  
**Use for**: Execution management, quality enforcement, performance monitoring  
**Key feature**: Enforces quality gates between stages  
**Example**: "Execute this plan and enforce all quality gates"

#### 7. Coordination Agent (System 2)
**File**: `.claude/agents/coordination-agent.md`  
**Use for**: Conflict prevention, resource allocation, deduplication  
**Key feature**: Prevents redundant work across agents  
**Example**: "Coordinate these parallel tasks and prevent conflicts"

---

### Orchestration Pattern Agents

#### 8. Parallel Orchestrator
**File**: `.claude/agents/parallel-orchestrator.md`  
**Use for**: Independent concurrent tasks  
**Key feature**: Executes multiple tasks simultaneously  
**Example**: "Research this topic from 3 different perspectives in parallel"

#### 9. Sequential Orchestrator
**File**: `.claude/agents/sequential-orchestrator.md`  
**Use for**: Dependent pipeline workflows  
**Key feature**: Quality gates between each stage  
**Example**: "Create a guide through: research → outline → write → review"

#### 10. Hub Orchestrator
**File**: `.claude/agents/hub-orchestrator.md`  
**Use for**: Multi-perspective synthesis  
**Key feature**: Iterative refinement with gap analysis  
**Example**: "Analyze from performance, usability, and architecture perspectives"

---

### Specialized Worker Agents

#### 11. Writer
**File**: `.claude/agents/writer.md`  
**Use for**: Content synthesis, technical documentation  
**Key feature**: Multiple document types (tutorial, guide, reference, report)  
**Example**: "Write a tutorial from this research with code examples"

#### 12. Critic-Reviewer
**File**: `.claude/agents/critic-reviewer.md`  
**Use for**: Tool-based quality validation (CRITIC pattern)  
**Key feature**: Objective validation with external tools  
**Example**: "Validate this document's quality using validation tools"

---

### Experimental Agents

#### 13. Adaptive Orchestrator
**File**: `.claude/agents/adaptive-orchestrator.md`  
**Use for**: Self-organizing specialist emergence  
**Key feature**: Dynamically creates specialists based on task patterns  
**Example**: "Handle these diverse tasks and learn optimal specializations"  
**Module**: `src/adaptive_resonance.py`

#### 14. Stigmergic Coordinator  
**File**: `.claude/agents/stigmergic-coordinator.md`  
**Use for**: Swarm intelligence coordination  
**Key feature**: Agents coordinate through shared signals  
**Example**: "Coordinate these agents using stigmergic signals"  
**Module**: `src/stigmergic_coordination.py`

---

## General Usage Pattern for All Agents

### 1. Activation

Agents activate when you:
- **Describe a matching task**: Claude Code reads the agent's description
- **Request by name**: "Use the researcher agent to..."
- **Implicit match**: Task characteristics match agent specialty

### 2. Agent File Structure

All agent files follow this structure:
```markdown
---
YAML frontmatter (configuration)
---

Agent description and role

## Core Responsibilities
[What the agent does]

## Working Process
[How the agent operates]

## Quality Standards
[What the agent ensures]

## Templates/Examples
[Output formats and examples]
```

### 3. Finding Agent Details

To learn about any agent:
1. Open `.claude/agents/{agent-name}.md`
2. Read the frontmatter for basic config
3. Review "Core Responsibilities" section
4. Check "Working Process" for methodology
5. See templates for expected outputs

---

## Creating Custom Tutorials

Want to create a detailed tutorial for a specific agent?

### Template Structure

```markdown
# {Agent Name} - Tutorial Guide

## Overview
- What it does
- When to use
- Key features

## Installation
- File location
- Configuration explained
- Verification steps

## Usage Examples
- Example 1: Basic usage
- Example 2: Advanced usage
- Example 3: Edge cases

## Expected Outputs
- Output format
- Quality standards
- File locations

## Tips & Best Practices
- Do's and don'ts
- Common patterns
- Pro tips

## Troubleshooting
- Common issues
- Solutions
- Debugging tips

## Related Agents
- Links to related tutorials
- Workflow combinations

## Next Steps
- What to try next
```

---

## Quick Start for Any Agent

### Step 1: Read Agent File
```bash
# View agent configuration and instructions
cat .claude/agents/{agent-name}.md
```

### Step 2: Test Agent
Request a task matching the agent's description.

### Step 3: Review Output
Check `artifacts/` for generated outputs.

### Step 4: Iterate
Provide feedback and refine.

---

## Agent Categories Summary

### Control & Governance (VSM Hierarchy)
- **Policy**: Defines rules and boundaries
- **Intelligence**: Plans strategy
- **Control**: Manages execution
- **Coordination**: Prevents conflicts

### Orchestration (Workflow Patterns)
- **Orchestrator**: Base supervisor
- **Parallel**: Concurrent execution
- **Sequential**: Pipeline workflows
- **Hub**: Multi-perspective synthesis

### Workers (Task Execution)
- **Researcher**: Information gathering
- **Writer**: Content creation
- **Critic-Reviewer**: Quality validation

### Experimental (R&D)
- **Adaptive**: Self-organizing
- **Stigmergic**: Swarm intelligence

---

## Learning Progression

### Beginners
Start with these 3:
1. Orchestrator - Basic coordination
2. Researcher - Information gathering
3. Writer - Content creation

### Intermediate
Add these 4:
4. Parallel-Orchestrator - Concurrent work
5. Sequential-Orchestrator - Pipelines
6. Hub-Orchestrator - Multi-perspective
7. Critic-Reviewer - Quality validation

### Advanced
Explore VSM hierarchy:
8. Intelligence-Agent - Strategic planning
9. Control-Agent - Execution management
10. Coordination-Agent - Conflict prevention
11. Policy-Agent - Governance

### Expert/Research
Try experimental:
12. Adaptive-Orchestrator - Self-organizing
13. Stigmergic-Coordinator - Swarm intelligence

---

## Need More Help?

- **Agent Files**: See `.claude/agents/` directory
- **System Overview**: Read `docs/SYSTEM-OVERVIEW.md`
- **Stage Guides**: Check `docs/stage-*.md` files
- **Main Index**: Return to `INDEX.md`

---

## Contributing Tutorials

Want to contribute a detailed tutorial for an agent?

1. Use the template structure above
2. Include practical examples
3. Add troubleshooting section
4. Link to related agents
5. Submit via pull request

---

**Remember**: All agent definitions in `.claude/agents/` are self-documenting with complete specifications, working processes, and examples!
