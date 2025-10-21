# Sequential Orchestrator - Tutorial Guide

**Agent Type**: Orchestration Pattern - Pipeline Workflow  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Yellow  

---

## Overview

The **Sequential Orchestrator** manages dependent task chains where each stage builds on the previous stage's output, like an assembly line with quality gates between stages.

### What It Does

- Designs execution pipelines with clear stage dependencies
- Enforces quality gates between each stage
- Validates outputs before proceeding to next stage
- Manages smooth handoffs between agents
- Maintains context through the pipeline

### When to Use

✅ **Use sequential orchestrator when**:
- Tasks have dependencies (Stage 2 needs Stage 1's output)
- Quality gates needed between phases
- Assembly-line workflow appropriate
- Context must flow from stage to stage
- Examples: Research → Outline → Write → Review

❌ **Don't use for**:
- Independent tasks (use parallel-orchestrator)
- Multi-perspective synthesis (use hub-orchestrator)
- Simple two-step workflows (use basic orchestrator)

---

## Usage Examples

### Example 1: Content Production Pipeline

**Your Request**:
```
"Create comprehensive Python async/await guide through:
1. Research phase
2. Outline phase
3. Writing phase
4. Review phase"
```

**Sequential Execution**:
```
Stage 1: Research
  ├── Input: User requirements
  ├── Agent: researcher
  ├── Output: artifacts/stage-1-research.md
  ├── Quality Gate: 85% ✓ PASS
  └── Proceeds to Stage 2

Stage 2: Outline
  ├── Input: artifacts/stage-1-research.md
  ├── Agent: planner
  ├── Output: artifacts/stage-2-outline.md
  ├── Quality Gate: 80% ✓ PASS
  └── Proceeds to Stage 3

Stage 3: Writing
  ├── Input: artifacts/stage-2-outline.md
  ├── Agent: writer
  ├── Output: artifacts/stage-3-draft.md
  ├── Quality Gate: 75% ✗ FAIL
  └── Refinement requested

Stage 3 (Revised): Writing
  ├── Input: artifacts/stage-2-outline.md + feedback
  ├── Agent: writer
  ├── Output: artifacts/stage-3-draft-v2.md
  ├── Quality Gate: 88% ✓ PASS
  └── Proceeds to Stage 4

Stage 4: Review
  ├── Input: artifacts/stage-3-draft-v2.md
  ├── Agent: critic-reviewer
  ├── Output: artifacts/stage-4-final.md
  └── Complete ✓
```

**Total Time**: 4 hours (with one refinement cycle)

### Example 2: Software Development Pipeline

**Your Request**:
```
"Build feature X through: requirements → design → implementation → testing"
```

**Pipeline Stages**:
1. Requirements gathering
2. Design specification
3. Code implementation
4. Test validation

Each stage validates before next proceeds.

---

## Quality Gates

### What They Do

Quality gates enforce standards between stages:

```markdown
### Gate 1→2: Research Complete
- Completeness: 9/10 ✓
- Accuracy: 10/10 ✓
- Organization: 8/10 ✓
- Overall: 90% → PASS
- Action: Proceed to outline

### Gate 2→3: Outline Complete
- Structure: 7/10 ⚠️
- Completeness: 6/10 ✗
- Overall: 65% → FAIL
- Action: Request revision
- Issues: Missing "Error Handling" and "Testing" sections
```

### Threshold Management

- **Default**: 80% to pass
- **Can customize**: "Use 90% threshold for high-quality output"
- **Fail action**: Request targeted refinement

---

## Tips & Best Practices

### 1. Plan Your Pipeline

Be explicit about stages:
```
"Create through these stages:
1. Research best practices
2. Create detailed outline
3. Write full content
4. Technical review and validation"
```

### 2. Specify Stage Inputs/Outputs

Clear handoffs:
```
"Stage 1 should produce research with 10+ findings
Stage 2 should use research to create structured outline
Stage 3 should use outline to write complete guide"
```

### 3. Set Quality Expectations

```
"Each stage must achieve 85% quality before proceeding"
```

### 4. Allow for Refinement

Expect 1-2 refinement cycles:
- Not a failure, it's quality assurance
- Targeted refinements are efficient
- Final quality is worth it

### 5. Maintain Context

Ensure each stage has what it needs:
```
"When writing (Stage 3), provide research findings AND outline structure"
```

---

## Troubleshooting

### Issue: Stage Stuck in Quality Gate

**Cause**: Output doesn't meet threshold

**Solution**: Review feedback and refine
- Check specific quality dimensions that failed
- Provide more context or requirements
- May need to lower threshold if too strict

### Issue: Pipeline Too Slow

**Cause**: Each stage sequential + refinements

**Solutions**:
- Reduce number of stages
- Accept lower quality thresholds
- Use parallel-orchestrator for independent parts

### Issue: Context Lost Between Stages

**Cause**: Handoff doesn't preserve important information

**Solution**: Explicitly specify what to preserve
```
"Stage 2 should retain all research citations for Stage 3"
```

---

## Working with Other Agents

### Common Pipeline Patterns

**Research → Write → Review**:
```
researcher → writer → critic-reviewer
```

**Plan → Execute → Validate**:
```
intelligence-agent → control-agent → critic-reviewer
```

**Nested Patterns**:
```
Sequential Pipeline
├── Stage 1: Parallel research from 3 sources
├── Stage 2: Synthesize research
├── Stage 3: Write guide
└── Stage 4: Review
```

---

## Performance Expectations

**For 4-Stage Pipeline**:
- Duration: 3-5 hours (includes quality gates)
- Quality: 85-95% (enforced at each stage)
- Token Usage: Moderate (refinement adds overhead)
- Refinement Cycles: 1-3 across all stages

**Compared to Parallel**:
- Slower (sequential not concurrent)
- Higher quality (gates catch issues early)
- Better for dependent workflows

---

## Next Steps

1. **Try Simple Pipeline**: Research → Write
2. **Learn Parallel**: See [parallel-orchestrator-tutorial.md](./parallel-orchestrator-tutorial.md)
3. **Explore Hub**: Try [hub-orchestrator-tutorial.md](./hub-orchestrator-tutorial.md)
4. **Advanced Control**: Study [control-agent-tutorial.md](./control-agent-tutorial.md)

---

## Summary

The **Sequential Orchestrator** manages dependent task chains with quality gates ensuring excellence at each stage.

**Perfect for**: Assembly-line workflows, content production pipelines, software development cycles, and any work where later stages depend on earlier stages.

---

**Ready to try?** Start with:
```
"Create guide through: research → outline → write → review"
```

Experience quality-gated pipeline execution!
