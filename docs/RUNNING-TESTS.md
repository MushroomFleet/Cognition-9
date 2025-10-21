# Running Tests - Cognition-9

Complete guide to testing and demonstrating the Cognition-9 multi-agent system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Test Categories](#test-categories)
4. [Running Agent Demonstrations](#running-agent-demonstrations)
5. [Running Stage Tests](#running-stage-tests)
6. [Understanding Results](#understanding-results)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## Quick Start

**Run all agent demonstrations:**
```bash
python tests/test-agents-demo.py
```

**Run a specific agent demo:**
```bash
python tests/test-agents-demo.py 5  # Run Policy Agent demo
```

**Run stage tests:**
```bash
python tests/test-stage2.py  # Core patterns & observability
python tests/test-stage3.py  # Cybernetic architecture
```

---

## Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Claude Code** (optional, for live agent testing)
   - Version 1.0.60 or higher
   - See installation instructions in README.md

### Required Python Packages

Install dependencies:
```bash
pip install -r requirements.txt
```

Core packages:
- `dataclasses` (built-in for Python 3.7+)
- No external dependencies for demos

### Verify Setup

Check that all components are in place:
```bash
python tests/test-orchestration.py
```

This will verify:
- ✓ Directory structure
- ✓ Agent definitions
- ✓ Configuration files
- ✓ Source modules

---

## Test Categories

### 1. Agent Demonstrations (`test-agents-demo.py`)

**Purpose**: Demonstrate what each agent does with simulated tasks

**What it shows**:
- Agent capabilities and use cases
- Expected inputs and outputs
- Quality validation processes
- Typical workflows

**When to use**: Learning about agents, onboarding new users

### 2. Orchestration Tests (`test-orchestration.py`)

**Purpose**: Basic multi-agent coordination

**What it tests**:
- Task decomposition
- Delegation patterns
- Quality review processes
- Final synthesis

**When to use**: Verifying basic setup

### 3. Stage Tests (`test-stage2.py`, `test-stage3.py`, etc.)

**Purpose**: Validate implementation milestones

**What they test**:
- Stage 2: CRITIC pattern, metrics, orchestration patterns
- Stage 3: Cybernetic architecture (VSM hierarchy)
- Stage 4: Novel architectures (adaptive, stigmergic)
- Stage 5: Production deployment features

**When to use**: Validating implementation progress

---

## Running Agent Demonstrations

### All Demos (Recommended First Run)

```bash
python tests/test-agents-demo.py
```

**Output**: Complete walkthrough of all 11 agents  
**Duration**: 5-8 minutes  
**What you'll see**:
- Agent descriptions and use cases
- Simulated task execution
- Quality scoring
- Key takeaways

### Individual Agent Demos

Run specific demos by number:

```bash
# Orchestration Agents
python tests/test-agents-demo.py 1   # Basic Orchestrator
python tests/test-agents-demo.py 2   # Parallel Orchestrator
python tests/test-agents-demo.py 3   # Sequential Orchestrator
python tests/test-agents-demo.py 4   # Hub Orchestrator

# VSM Hierarchy
python tests/test-agents-demo.py 5   # Policy Agent (System 5)
python tests/test-agents-demo.py 6   # Intelligence Agent (System 4)
python tests/test-agents-demo.py 7   # Control Agent (System 3)
python tests/test-agents-demo.py 8   # Coordination Agent (System 2)

# Specialists
python tests/test-agents-demo.py 9   # Researcher
python tests/test-agents-demo.py 10  # Writer
python tests/test-agents-demo.py 11  # Critic-Reviewer
```

### Getting Help

```bash
python tests/test-agents-demo.py --help
```

---

## Running Stage Tests

### Stage 2: Core Patterns & Observability

```bash
python tests/test-stage2.py
```

**Tests**:
1. ✓ CRITIC pattern validators
2. ✓ Metrics collection system
3. ✓ Agent configuration (4 agents)
4. ✓ Source modules present

**Expected Output**:
```
Stage 2 Implementation: COMPLETE
✓ Three orchestration patterns
✓ CRITIC pattern for validation
✓ Metrics collection and reporting
✓ Quality assessment framework
```

### Stage 3: Cybernetic Architecture

```bash
python tests/test-stage3.py
```

**Tests**:
1. ✓ VSM hierarchy agents (4 agents)
2. ✓ Homeostasis mechanisms
3. ✓ Durable execution
4. ✓ Security features

### Stage 4: Novel Architectures

```bash
python tests/test-stage4.py
```

**Tests**:
1. ✓ Adaptive Resonance Theory
2. ✓ Stigmergic coordination
3. ✓ Self-organizing behaviors
4. ✓ Emergent patterns

### Stage 5: Production Deployment

```bash
python tests/test-stage5.py
```

**Tests**:
1. ✓ Cost management
2. ✓ Skill library
3. ✓ Production readiness
4. ✓ Integration points

---

## Understanding Results

### Demo Output Format

Each demo follows this structure:

```
======================================================================
DEMO [N]: [AGENT NAME]
======================================================================

📋 Agent: [Name]
Use Case: [Description]
Pattern: [Workflow pattern]

----------------------------------------------------------------------
USER REQUEST
----------------------------------------------------------------------
Task: "[Sample request]"
Expected Output: [Description]

----------------------------------------------------------------------
[PROCESSING STEPS]
----------------------------------------------------------------------
→ [Step description]
  ✓ Completed (simulated)

Quality Score: [XX]% ✅ PASS / ❌ FAIL

✅ Demo Complete

💡 Key Takeaway: [Important insight]
```

### Quality Scores

**Understanding percentages**:
- **90-100%**: Excellent - Exceeds expectations
- **80-89%**: Good - Meets all requirements
- **70-79%**: Acceptable - Minor refinement needed
- **60-69%**: Needs refinement - Missing key elements
- **Below 60%**: Requires major revision

**Quality thresholds in system**:
- Minimum acceptable: 80%
- Algedonic alert: 40% (critical failure)
- Auto-rejection: 60%

### Test Result Interpretation

**✅ All tests passed**: System fully functional
```
Tests Passed: 4/4
✅ validators
✅ metrics
✅ agents
✅ modules
```

**⚠️ Some tests failed**: Review error messages
```
Tests Passed: 3/4
✅ validators
❌ metrics - Import error
✅ agents
✅ modules
```

---

## Troubleshooting

### Common Issues

#### Issue: Import errors

**Symptom**:
```
ImportError: No module named 'src.validators'
```

**Solution**:
```bash
# Ensure you're in project root
cd /path/to/Cognition-9

# Verify src/ directory exists
ls src/

# Run tests from project root
python tests/test-agents-demo.py
```

#### Issue: Agent files not found

**Symptom**:
```
✗ .claude/agents/orchestrator.md
```

**Solution**:
```bash
# Verify agent files exist
ls -la .claude/agents/

# Should see 11 .md files
```

#### Issue: Claude Code not recognizing agents

**Symptom**: Agents don't activate in Claude Code

**Solution**:
1. Ensure Claude Code version 1.0.60+
2. Verify agent files in `.claude/agents/`
3. Check YAML frontmatter is valid
4. Try describing task more explicitly:
   ```
   "Research topic X and write a guide"  # ✓ Activates orchestrator
   vs
   "Tell me about X"  # ✗ Too simple
   ```

#### Issue: Slow execution

**Symptom**: Demos taking longer than expected

**Explanation**: Demos include `time.sleep()` for visualization  
**Normal**: 5-8 minutes for all 11 demos  
**Solution**: This is intentional for demonstration clarity

#### Issue: Missing dependencies

**Symptom**:
```
ModuleNotFoundError: No module named 'dataclasses'
```

**Solution**:
```bash
# Upgrade Python (dataclasses built-in 3.7+)
python --version

# Or install for Python 3.6
pip install dataclasses
```

### Debug Mode

Run demos with Python's verbose output:
```bash
python -v tests/test-agents-demo.py
```

Check specific module:
```bash
python -c "import src.validators; print('✓ Validators OK')"
python -c "import src.metrics; print('✓ Metrics OK')"
```

---

## Advanced Usage

### Creating Custom Test Scenarios

1. **Copy demo template**:
```python
def demo_custom_workflow():
    demo = AgentDemo("my-workflow", "blue")
    demo.print_header("CUSTOM WORKFLOW TEST")
    
    # Your test logic here
    demo.simulate_task("Running custom task...", 0.5)
    demo.show_quality(85, 80)
    
    return True
```

2. **Add to demo list**:
```python
demos = [
    # ... existing demos ...
    ("Custom Workflow", demo_custom_workflow),
]
```

### Automating Test Runs

**Create test script** (`run-tests.sh`):
```bash
#!/bin/bash
echo "Running Cognition-9 Tests..."

echo "1. Agent Demos..."
python tests/test-agents-demo.py

echo "2. Stage 2 Tests..."
python tests/test-stage2.py

echo "3. Stage 3 Tests..."
python tests/test-stage3.py

echo "All tests complete!"
```

**Run**:
```bash
chmod +x run-tests.sh
./run-tests.sh
```

### CI/CD Integration

**GitHub Actions example** (`.github/workflows/test.yml`):
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - run: pip install -r requirements.txt
      - run: python tests/test-agents-demo.py
      - run: python tests/test-stage2.py
```

### Benchmarking Performance

Track execution times:
```bash
time python tests/test-agents-demo.py
```

Expected results:
- Demo script: 5-8 minutes
- Stage 2 tests: 1-2 minutes
- Individual demos: 30-60 seconds

---

## Test Coverage Matrix

| Component | Demo | Stage 2 | Stage 3 | Stage 4 | Stage 5 |
|-----------|------|---------|---------|---------|---------|
| Orchestrator | ✅ | ✅ | - | - | - |
| Parallel | ✅ | ✅ | - | - | - |
| Sequential | ✅ | ✅ | - | - | - |
| Hub | ✅ | ✅ | - | - | - |
| Policy (S5) | ✅ | - | ✅ | - | - |
| Intelligence (S4) | ✅ | - | ✅ | - | - |
| Control (S3) | ✅ | - | ✅ | - | - |
| Coordination (S2) | ✅ | - | ✅ | - | - |
| Researcher | ✅ | ✅ | - | - | - |
| Writer | ✅ | ✅ | - | - | - |
| Critic | ✅ | ✅ | - | - | - |
| Validators | - | ✅ | - | - | - |
| Metrics | - | ✅ | - | - | ✅ |
| Homeostasis | - | - | ✅ | - | - |
| Adaptive | - | - | - | ✅ | - |
| Stigmergic | - | - | - | ✅ | - |
| Cost Mgmt | - | - | - | - | ✅ |

---

## Additional Resources

### Documentation
- **Agent Details**: See `docs/tutorials/[agent-name]-tutorial.md`
- **System Overview**: Read `docs/SYSTEM-OVERVIEW.md`
- **Stage Guides**: Check `docs/stage-*.md` files

### Tutorials
All agents have detailed tutorials in `docs/tutorials/`:
- `AGENT-TUTORIALS-INDEX.md` - Complete index
- `orchestrator-tutorial.md` - Orchestrator guide
- `researcher-tutorial.md` - Researcher guide
- (...11 tutorials total)

### Getting Help

1. **Check tutorials**: `docs/tutorials/AGENT-TUTORIALS-INDEX.md`
2. **Run demos**: `python tests/test-agents-demo.py`
3. **Review examples**: Study demo output for patterns
4. **Read agent files**: `.claude/agents/*.md` are self-documenting

---

## Next Steps

After running tests:

1. **✅ Demos work?** → Try agents in Claude Code with real tasks
2. **✅ Stage 2 passed?** → Continue to Stage 3 tests
3. **✅ All stages passed?** → System ready for production
4. **❌ Issues?** → Check Troubleshooting section

**Ready to use agents?** See README.md for usage guide.

---

## Summary

**Quick commands**:
```bash
# All agent demos
python tests/test-agents-demo.py

# Specific demo
python tests/test-agents-demo.py [1-11]

# Stage tests
python tests/test-stage2.py
python tests/test-stage3.py

# Help
python tests/test-agents-demo.py --help
```

**Expected outcomes**:
- All demos show agent capabilities
- All stage tests pass
- Ready to use with Claude Code
- System validated and functional

**For more information**: See `docs/tutorials/AGENT-TUTORIALS-INDEX.md`

---

*Last updated: 2025-10-21*
