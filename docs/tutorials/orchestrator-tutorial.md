# Orchestrator Agent - Tutorial Guide

**Agent Type**: Base Supervisor Pattern  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Purple  

---

## Overview

The **Orchestrator** is the foundational supervisor agent that coordinates complex multi-step workflows by delegating tasks to specialist agents, monitoring quality, and synthesizing results.

### What It Does

- Analyzes complex tasks and breaks them into subtasks
- Delegates work to appropriate specialist agents
- Reviews specialist outputs for quality
- Provides feedback and requests refinement when needed
- Synthesizes final deliverables from multiple specialist outputs

### When to Use

✅ **Use the orchestrator when you need to**:
- Coordinate multi-step workflows
- Delegate to multiple specialists
- Ensure quality control across agents
- Synthesize outputs from different sources
- Manage complex projects with multiple phases

❌ **Don't use for**:
- Simple single-step tasks
- Tasks better suited for specific specialists
- Direct research or writing (use researcher or writer instead)

---

## Installation

### Step 1: Verify Agent File Exists

The orchestrator agent is already configured at:
```
.claude/agents/orchestrator.md
```

### Step 2: Understanding the Configuration

The agent file uses YAML frontmatter for configuration:

```yaml
---
name: orchestrator
description: Main coordinator for multi-agent workflows. Analyzes tasks, delegates to specialists, and ensures quality outputs.
tools: Read, Write, List_Files
model: opus
color: purple
---
```

**Configuration explained**:
- `name`: Agent identifier used by Claude Code
- `description`: Tells Claude when to activate this agent
- `tools`: What the agent can do (read files, write files, list directories)
- `model`: Which Claude model to use (opus for best quality)
- `color`: Visual identifier in Claude Code interface

### Step 3: Verify in Claude Code

In Claude Code (v1.0.60+), the agent will automatically activate when you:
1. Describe a task matching the agent's description
2. Explicitly request the orchestrator by name
3. Ask for coordination of multi-step work

---

## Usage Examples

### Example 1: Simple Research and Write Task

**Your Request**:
```
"Research Python async/await and write a comprehensive guide"
```

**What the Orchestrator Does**:

1. **Task Analysis**:
   - Main objective: Create async/await guide
   - Subtasks: (1) Research, (2) Write guide
   - Dependencies: Writing depends on research

2. **Delegation**:
   - Delegates research to `researcher` agent
   - Waits for completion and reviews quality
   - Delegates writing to `writer` agent using research as input
   - Reviews final guide quality

3. **Quality Control**:
   - Checks research completeness (score: 93%)
   - Validates guide structure (score: 89%)
   - Both exceed 80% threshold → Approved

4. **Synthesis**:
   - Combines research and guide
   - Adds executive summary
   - Saves to `artifacts/final-output.md`

**Expected Output**:
- `artifacts/async-research.md` - Research findings
- `artifacts/async-guide.md` - Complete tutorial
- `artifacts/final-output.md` - Synthesized deliverable

### Example 2: Multi-Specialist Coordination

**Your Request**:
```
"Create a technical report analyzing Python async/await from performance, 
usability, and architecture perspectives"
```

**What the Orchestrator Does**:

1. **Decomposition**:
   - Subtask 1: Performance analysis
   - Subtask 2: Usability analysis  
   - Subtask 3: Architecture analysis
   - Subtask 4: Synthesis into unified report

2. **Parallel Delegation**:
   - Multiple researcher instances for different perspectives
   - All execute concurrently

3. **Synthesis**:
   - Integrates all perspectives
   - Resolves any conflicts
   - Creates cohesive final report

### Example 3: Quality Refinement Loop

**Your Request**:
```
"Write a Python tutorial with high quality standards"
```

**What the Orchestrator Does**:

1. **Initial Delegation**:
   - Delegates to `writer` agent
   - Writer produces initial draft

2. **Quality Review**:
   - Reviews draft (score: 72%)
   - Below 80% threshold → Needs refinement

3. **Feedback Loop**:
   - Identifies specific issues:
     - Missing error handling section
     - Insufficient code examples
     - Weak introduction
   - Provides targeted feedback to writer
   - Writer produces revision

4. **Re-Review**:
   - Reviews revision (score: 88%)
   - Exceeds threshold → Approved
   - Delivers final output

---

## Expected Outputs

### Orchestration Log

The orchestrator creates detailed logs documenting its work:

```markdown
# Orchestration Log: Python Async Guide
Timestamp: 2024-01-15T10:00:00Z
Orchestrator: orchestrator

## Task Analysis
**Original Request**: "Research and write Python async/await guide"
**Main Objective**: Create comprehensive tutorial
**Success Criteria**: Quality ≥ 80%, includes examples, proper citations

## Decomposition
1. **Research Phase**: 
   - Assigned to: researcher
   - Priority: High
   - Output: artifacts/research.md
   - Dependencies: None

2. **Writing Phase**:
   - Assigned to: writer
   - Priority: High
   - Output: artifacts/guide.md
   - Dependencies: Research phase

## Quality Review
### Research Output
- Completeness: 9/10
- Accuracy: 10/10
- Overall: 93% - APPROVED

### Guide Output
- Completeness: 9/10
- Clarity: 9/10
- Overall: 89% - APPROVED

## Final Synthesis
Output Location: artifacts/final-output.md
Quality Score: 91%
Completion Time: 2024-01-15T14:30:00Z
```

---

## Communication Protocol

### How the Orchestrator Delegates

When delegating to specialist agents, the orchestrator provides:

```markdown
Task: Research Python async/await
Output: artifacts/async-research.md
Format: Markdown with sections for:
- Core concepts
- Best practices
- Code examples
- Common pitfalls

Quality Criteria:
- Minimum 10 key concepts
- 5+ sources cited
- Code examples for each concept
- Clear organization

Success Threshold: 80%
```

### What the Orchestrator Expects Back

```markdown
# Research Report: Python Async/Await
Researcher: researcher
Date: 2024-01-15T11:30:00Z
Confidence: 92%

[Research content...]

## Metadata
- Sources Consulted: 12
- Key Concepts: 15
- Code Examples: 8
- Quality Self-Assessment: 92%
```

---

## Quality Standards

The orchestrator enforces these quality criteria:

### Completeness (Score 0-10)
- All requirements addressed
- No missing sections
- Comprehensive coverage

### Accuracy (Score 0-10)
- Information is correct
- Sources are credible
- Claims are well-supported

### Clarity (Score 0-10)
- Clear, well-structured writing
- Logical flow
- Proper formatting

### Overall Threshold
- **Minimum acceptable**: 80% (8.0/10 average)
- **Target quality**: 85%+
- **Excellent quality**: 90%+

---

## Tips & Best Practices

### 1. Provide Clear, Detailed Requests

❌ **Vague**:
```
"Make something about Python"
```

✅ **Clear**:
```
"Research Python async/await best practices and write a beginner-friendly 
tutorial with runnable code examples and common pitfall explanations"
```

### 2. Let the Orchestrator Decide How

The orchestrator will:
- Analyze your request
- Decompose into optimal subtasks
- Select appropriate specialists
- Determine execution order

You don't need to specify which agents to use.

### 3. Trust the Quality Process

The orchestrator will:
- Validate all outputs
- Request refinements if needed
- Iterate until quality threshold met
- Deliver only high-quality results

### 4. Check the Artifacts

All intermediate and final outputs saved to `artifacts/`:
- Review to understand what happened
- Use for debugging if needed
- Reference for future work

### 5. Provide Feedback

If the final output doesn't meet your needs:
- Be specific about what's missing or wrong
- The orchestrator will coordinate refinements
- Can iterate multiple times if needed

---

## Troubleshooting

### Issue: Orchestrator Not Activating

**Symptoms**: Request goes to default Claude instead of orchestrator

**Solutions**:
1. Ensure Claude Code v1.0.60+ is installed
2. Verify `.claude/agents/orchestrator.md` exists
3. Make request more clearly multi-step:
   - "Research X and write Y" (triggers orchestration)
   - vs "Tell me about X" (single-step query)

### Issue: Quality Too Low

**Symptoms**: Orchestrator reports quality below threshold

**Solutions**:
1. Check what specific dimensions failed
2. Review orchestrator's feedback
3. Specialist may need more context or better requirements
4. Consider if task is too vague or ambitious

### Issue: Taking Too Long

**Symptoms**: Orchestration seems slow

**Causes**:
- Multiple refinement cycles (quality iterations)
- Complex multi-specialist coordination
- Thorough quality checking

**This is normal**: Multi-agent systems trade speed for quality

---

## Working with Other Agents

The orchestrator commonly works with:

### Researcher Agent
- For information gathering phases
- Tutorial: [researcher-tutorial.md](./researcher-tutorial.md)

### Writer Agent
- For content creation phases
- Tutorial: [writer-tutorial.md](./writer-tutorial.md)

### Critic-Reviewer Agent
- For final quality validation
- Tutorial: [critic-reviewer-tutorial.md](./critic-reviewer-tutorial.md)

### Intelligence Agent (Advanced)
- For complex strategic planning
- Tutorial: [intelligence-agent-tutorial.md](./intelligence-agent-tutorial.md)

---

## Advanced Usage

### Custom Quality Thresholds

You can specify quality requirements:
```
"Research topic X and write guide with minimum 90% quality"
```

The orchestrator will:
- Set quality threshold to 90%
- Iterate until achieved
- May take longer but ensures excellence

### Specify Output Formats

Be explicit about what you want:
```
"Create tutorial-style guide with:
- Step-by-step instructions
- Runnable code examples
- Exercises for practice
- Troubleshooting section"
```

### Multi-Phase Projects

For complex projects:
```
"Phase 1: Research async/await
Phase 2: Create outline
Phase 3: Write tutorial
Phase 4: Add exercises
Phase 5: Technical review"
```

The orchestrator will manage all phases sequentially with quality gates.

---

## Next Steps

After mastering the orchestrator:

1. **Learn Specialists**: Explore [researcher](./researcher-tutorial.md) and [writer](./writer-tutorial.md)
2. **Try Patterns**: Experiment with [parallel-orchestrator](./parallel-orchestrator-tutorial.md)
3. **Advanced Control**: Study [intelligence-agent](./intelligence-agent-tutorial.md)
4. **Quality Systems**: Master [critic-reviewer](./critic-reviewer-tutorial.md)

---

## Performance Expectations

### Typical Metrics

**For Research + Write Task**:
- Duration: 2-4 hours (vs 1-2 hours single agent)
- Quality: 85-95% (vs 70-85% single agent)
- Token Usage: ~15x overhead for coordination
- Success Rate: 90%+

**Why Use Despite Overhead?**:
- Higher quality outputs
- Better specialist utilization
- Quality assurance built-in
- Scalable to complex projects

---

## Summary

The **Orchestrator** is your primary coordination agent for multi-step workflows. It:

✅ Analyzes tasks and creates execution plans  
✅ Delegates to appropriate specialists  
✅ Enforces quality standards  
✅ Manages refinement cycles  
✅ Delivers integrated results  

**Perfect for**: Complex projects requiring coordination, quality control, and specialist expertise.

---

**Ready to try?** Start with a simple request like:
```
"Research topic X and create a guide about it"
```

And watch the orchestrator coordinate the entire workflow!
