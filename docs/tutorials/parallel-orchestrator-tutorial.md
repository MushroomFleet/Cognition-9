# Parallel Orchestrator - Tutorial Guide

**Agent Type**: Orchestration Pattern - Concurrent Execution  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Orange  

---

## Overview

The **Parallel Orchestrator** coordinates multiple independent tasks that can execute concurrently, maximizing speed by running work simultaneously rather than sequentially.

### What It Does

- Analyzes tasks to confirm true independence (no dependencies)
- Delegates multiple tasks simultaneously to different agents
- Monitors concurrent execution progress
- Aggregates results when all tasks complete
- Handles partial failures gracefully

### When to Use

✅ **Use parallel orchestrator when**:
- Tasks are truly independent (no dependencies)
- Speed is priority (want results faster)
- Different specialists needed for different subtasks
- Research from multiple perspectives/sources
- Processing different data sets simultaneously

❌ **Don't use for**:
- Tasks with dependencies (use sequential-orchestrator)
- Tasks requiring synthesis across perspectives (use hub-orchestrator)
- Single tasks (use basic orchestrator)
- Tasks sharing resources that could conflict

---

## Installation

### Verify Agent File

Location: `.claude/agents/parallel-orchestrator.md`

Configuration:
```yaml
---
name: parallel-orchestrator
description: Orchestrates multiple independent tasks concurrently.
tools: Read, Write, List_Files
model: opus
color: orange
---
```

---

## Usage Examples

### Example 1: Multi-Source Research

**Your Request**:
```
"Research Python async/await from three independent perspectives:
1. Academic papers and PEPs
2. Tutorial and blog content
3. Production case studies and GitHub examples"
```

**What Happens**:

1. **Independence Analysis**:
   ```
   Task 1: Academic research - INDEPENDENT ✓
   Task 2: Tutorial research - INDEPENDENT ✓
   Task 3: Production research - INDEPENDENT ✓
   → All can run in parallel
   ```

2. **Parallel Delegation**:
   ```
   Time 0:00 - Task 1 delegated to researcher-A
   Time 0:00 - Task 2 delegated to researcher-B
   Time 0:00 - Task 3 delegated to researcher-C
   ```
   All three start simultaneously!

3. **Concurrent Monitoring**:
   ```
   Time 0:45 - Task 2 completes (fastest)
   Time 1:10 - Task 1 completes
   Time 1:20 - Task 3 completes (slowest)
   Total time: 1:20 (vs 3+ hours sequential)
   ```

4. **Results Aggregation**:
   - Collects all three research reports
   - Synthesizes into unified document
   - Saves to `artifacts/parallel-result.md`

**Output**:
- `artifacts/parallel-task-1.md` - Academic research
- `artifacts/parallel-task-2.md` - Tutorial research
- `artifacts/parallel-task-3.md` - Production research
- `artifacts/parallel-result.md` - Aggregated synthesis

### Example 2: Multiple Data Processing

**Your Request**:
```
"Analyze these three log files independently and provide summary for each"
```

**Parallel Execution**:
```
Agent A → logs/app.log → Summary A
Agent B → logs/db.log → Summary B
Agent C → logs/api.log → Summary C

All running concurrently
Results delivered together
```

**Time Savings**:
- Sequential: ~3 hours (1hr each)
- Parallel: ~1 hour (longest task)
- **Speedup**: 3x faster

### Example 3: Variant Generation

**Your Request**:
```
"Generate 3 different tutorial approaches for beginners:
1. Code-first approach with lots of examples
2. Concept-first approach with theory
3. Project-based approach building real app"
```

**Parallel Execution**:
- Each variant created independently
- All run simultaneously
- User can compare and choose best

---

## Expected Outputs

### Parallel Execution Log

```markdown
# Parallel Execution: Multi-Source Research
Start Time: 2024-01-15T10:00:00Z
Expected Completion: 2024-01-15T11:30:00Z

## Task Decomposition
**Independent Tasks**: 3
**Specialists Involved**: researcher (3 instances)
**Estimated Time**: 1.5 hours

## Parallel Tasks

### Task 1: Academic Research
- Specialist: researcher
- Output: artifacts/parallel-async-1.md
- Status: DELEGATED at 10:00:00Z
- Dependencies: NONE
- Completion: 11:10:00Z ✓

### Task 2: Tutorial Research
- Specialist: researcher
- Output: artifacts/parallel-async-2.md
- Status: DELEGATED at 10:00:00Z
- Dependencies: NONE
- Completion: 10:45:00Z ✓

### Task 3: Production Research
- Specialist: researcher
- Output: artifacts/parallel-async-3.md
- Status: DELEGATED at 10:00:00Z
- Dependencies: NONE
- Completion: 11:20:00Z ✓

## Completion Status
- Task 1: COMPLETED at 11:10:00Z
- Task 2: COMPLETED at 10:45:00Z
- Task 3: COMPLETED at 11:20:00Z

**Total Execution Time**: 1h 20m
**Success Rate**: 100% (3/3)

## Aggregated Result
**Integration Strategy**: Synthesized all three perspectives
**Output Location**: artifacts/parallel-result-async.md
```

---

## Tips & Best Practices

### 1. Verify True Independence

Before using parallel orchestrator, ensure tasks are truly independent:

✅ **Independent**:
- Research different topics
- Process different files
- Generate different variants
- Analyze separate data sets

❌ **NOT Independent**:
- Write tutorial (needs research first)
- Test code (needs code written first)
- Synthesize (needs source content first)

### 2. Group Similar Task Types

For best results:
```
"Research async/await from 3 sources" 
→ All use researcher agent (efficient)

vs

"Research X, write Y, test Z"
→ Different agents (less efficient parallelization)
```

### 3. Set Realistic Expectations

**Speed gains**: Up to N× faster (N = number of parallel tasks)
**Token costs**: ~same as sequential (all tasks still execute)
**Quality**: Same as sequential (each task gets full attention)

### 4. Handle Partial Failures

If one task fails:
```
Task 1: SUCCESS
Task 2: FAILED
Task 3: SUCCESS

Orchestrator will:
- Deliver results from successful tasks
- Report failure details
- Optionally retry failed task
```

### 5. Monitor Resource Usage

Parallel execution uses more concurrent resources:
- Multiple model instances
- Higher momentary token usage
- More memory for state tracking

---

## Troubleshooting

### Issue: Tasks Run Sequentially Anyway

**Cause**: Tasks have hidden dependencies

**Solution**: Check if tasks truly independent
```
"Research A from papers" - Independent ✓
"Research B from web" - Independent ✓
"Synthesize A and B" - DEPENDS on A & B ✗
```

Use sequential-orchestrator for dependent tasks.

### Issue: Results Inconsistent

**Cause**: Different agent instances have different context

**Solution**: Ensure each task is self-contained
```
❌ "Research using previous findings"
✅ "Research async/await error handling from official docs"
```

### Issue: Slower Than Expected

**Possible causes**:
1. Task delegation overhead
2. Longest task dominates total time
3. Resource contention

**Check**: Review completion times in log to identify bottleneck

### Issue: Aggregation Quality Low

**Cause**: Results from parallel tasks need synthesis

**Solution**: Let orchestrator know you need unified output
```
"Research from 3 sources AND synthesize into single report"
```

---

## Working with Other Agents

### Common Parallel Patterns

**Pattern 1: Multi-Researcher**
```
Parallel-Orchestrator
├── Researcher A (academic)
├── Researcher B (tutorials)
└── Researcher C (production)
```

**Pattern 2: Multi-Writer**
```
Parallel-Orchestrator
├── Writer A (tutorial version)
├── Writer B (reference version)
└── Writer C (quick-start version)
```

**Pattern 3: Mixed Specialists**
```
Parallel-Orchestrator
├── Researcher (gather info)
├── Writer (create draft)
└── Critic (review existing)
```

### Integration with Other Orchestrators

**Parallel inside Sequential**:
```
Sequential-Orchestrator
├── Stage 1: Research (parallel from 3 sources)
├── Stage 2: Synthesize
└── Stage 3: Write
```

**Sequential inside Parallel**:
```
Parallel-Orchestrator
├── Pipeline A: Research→Write
├── Pipeline B: Research→Write
└── Pipeline C: Research→Write
```

---

## Advanced Usage

### Dynamic Task Count

Don't hardcode number of parallel tasks:
```
"Research from as many relevant perspectives as needed"
```

Orchestrator determines optimal task count.

### Priority Handling

Specify if some tasks more important:
```
"Research from academic papers (CRITICAL) and blogs (nice-to-have)"
```

### Timeout Management

For time-sensitive work:
```
"Research these 5 topics in parallel, max 30 minutes each"
```

Orchestrator enforces timeouts.

---

## Performance Expectations

### Time Savings

**3 Independent Tasks**:
- Sequential: 3 × 1hr = 3 hours
- Parallel: max(1hr, 1hr, 1hr) = 1 hour
- **Speedup**: 3× faster

**Variable Duration Tasks**:
- Sequential: 0.5hr + 2hr + 1hr = 3.5 hours
- Parallel: max(0.5hr, 2hr, 1hr) = 2 hours
- **Speedup**: 1.75× faster (limited by longest task)

### Resource Usage

- **Token Usage**: ~same as sequential (all work still done)
- **Concurrent Load**: Higher (multiple agents active)
- **Memory**: More state tracking overhead

---

## Comparison with Other Patterns

### vs Sequential Orchestrator

**Parallel**:
- ✅ Faster for independent tasks
- ✅ Maximizes parallelism
- ❌ Requires true independence
- ❌ More complex aggregation

**Sequential**:
- ✅ Handles dependencies naturally
- ✅ Simpler state management
- ❌ Slower (tasks run one-by-one)
- ❌ Can't leverage concurrency

### vs Hub Orchestrator

**Parallel**:
- Focus: Speed through concurrency
- Best for: Independent information gathering
- Synthesis: Simple aggregation

**Hub**:
- Focus: Multi-perspective synthesis
- Best for: Complementary viewpoints
- Synthesis: Deep integration with iteration

---

## Real-World Use Cases

### Use Case 1: Competitive Analysis
```
"Research these 5 competitor products in parallel:
- Product A features
- Product B pricing
- Product C user reviews
- Product D technical specs
- Product E market position"
```

### Use Case 2: Multi-Language Documentation
```
"Generate this tutorial in 3 languages simultaneously:
- English version
- Spanish version
- French version"
```

### Use Case 3: A/B/C Testing
```
"Create 3 different homepage designs in parallel:
- Minimalist design
- Feature-rich design
- Visual/artistic design"
```

---

## Next Steps

1. **Try Basic Parallel**: Start with 2-3 independent tasks
2. **Learn Sequential**: For dependent tasks, see [sequential-orchestrator-tutorial.md](./sequential-orchestrator-tutorial.md)
3. **Explore Hub Pattern**: For synthesis, see [hub-orchestrator-tutorial.md](./hub-orchestrator-tutorial.md)
4. **Master VSM**: Advanced planning with [intelligence-agent-tutorial.md](./intelligence-agent-tutorial.md)

---

## Summary

The **Parallel Orchestrator** enables concurrent execution of independent tasks for maximum speed.

**Key Benefits**:
- N× speedup for N independent tasks
- Efficient resource utilization
- Graceful handling of partial failures
- Automatic result aggregation

**Perfect for**: Multi-source research, variant generation, independent data processing, and any workflow where tasks don't depend on each other.

---

**Ready to try?** Start with:
```
"Research [topic] from academic, tutorial, and production perspectives in parallel"
```

And experience the power of concurrent execution!
