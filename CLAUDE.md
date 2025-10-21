# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Cognition-9** is a production-ready multi-agent orchestration system implementing a 5-level Viable System Model (VSM) cybernetic hierarchy with 13 specialized agents. The system enables sophisticated task coordination, parallel execution, quality validation, and experimental self-organizing patterns.

**Key Stats**: 13 agents, 7 Python modules, 5 test suites (18/18 passing), complete documentation

## Core Architecture

### Hierarchical Structure (VSM)

The system follows the Viable System Model with 5 cybernetic levels:

1. **System 5 (Policy)** - `policy-agent` - Governance, ethics, strategic objectives
2. **System 4 (Intelligence)** - `intelligence-agent` - Strategic planning, task decomposition
3. **System 3 (Control)** - `control-agent` - Execution management, quality enforcement
4. **System 2 (Coordination)** - `coordination-agent` - Conflict prevention, resource allocation
5. **System 1 (Operations)** - Worker agents (orchestrators, specialists)

Information flows:
- **Upward (attenuation)**: Detailed work summarized at each level
- **Downward (amplification)**: Strategic directives expanded into detailed tasks
- **Algedonic signals**: Critical issues escalate directly to System 5

### Agent Categories

**Orchestration Patterns (4 agents)**:
- `orchestrator` - Base supervisor pattern
- `parallel-orchestrator` - Concurrent independent tasks
- `sequential-orchestrator` - Dependent task pipelines
- `hub-orchestrator` - Multi-perspective synthesis with iteration

**Specialized Workers (3 agents)**:
- `researcher` - Information gathering and analysis (Read, Web_Search, Grep)
- `writer` - Content synthesis and documentation (Read, Write)
- `critic-reviewer` - Quality validation using external tools (Read, Write, Execute_Command)

**VSM Hierarchy (4 agents)**: Listed above

**Experimental (2 agents)** - Available in Stage 4:
- Adaptive Orchestrator - Self-organizing specialists
- Stigmergic Coordinator - Swarm intelligence patterns

## Testing

### Running Tests

```bash
# Test individual stages
python tests/test-orchestration.py  # Stage 1: Foundation (3 agents)
python tests/test-stage2.py         # Stage 2: Patterns + Observability (4/4 tests)
python tests/test-stage3.py         # Stage 3: VSM Hierarchy (5/5 tests)
python tests/test-stage4.py         # Stage 4: Experimental (4/4 tests)
python tests/test-stage5.py         # Stage 5: Production (4/4 tests)
```

**All 18/18 tests must pass** - The test suite validates agent communication, quality control, orchestration patterns, and infrastructure components.

### Test Verification
Tests are written in Python and use the standard library. They verify:
- Agent definition files exist and are properly formatted
- Orchestration flows work correctly
- Quality validation (CRITIC pattern) functions properly
- Metrics collection persists correctly

## Development Workflow

### Agent Communication Protocol

Agents communicate through **markdown artifacts** in the `artifacts/` directory:
- `artifacts/research-output.md` - Research findings
- `artifacts/synthesis-output.md` - Final outputs
- `artifacts/feedback.md` - Quality feedback
- Custom filenames for specific workflows

**Quality Standards**: All outputs must include reasoning, citations (where applicable), proper markdown formatting, and metadata (agent name, timestamp, confidence level).

### Quality Control (CRITIC Pattern)

External tool-based validation is critical because LLMs cannot reliably self-correct:

**Validation Dimensions** (see `src/validators.py`):
- **Structure**: Markdown formatting, header hierarchy, code block language tags
- **Citations**: Claims must have supporting citations (target ratio: 30%+)
- **Completeness**: All required topics covered (80%+ threshold)
- **Code Validity**: Code examples properly formatted and non-empty (90%+ threshold)

**Quality Thresholds**:
- Minimum acceptable: 80%
- Auto-rejection: < 60%
- Algedonic alert: < 40% (escalates to System 5)

**Refinement Loop**: If quality < 80%, feedback is generated and agents refine (max 3 cycles).

### Key Python Modules

**src/validators.py** - CRITIC pattern implementation:
- `OutputValidator` - Multi-dimensional quality assessment
- `FeedbackGenerator` - Generates actionable refinement feedback

**src/metrics.py** - Performance monitoring:
- `AgentMetrics` - Tracks individual agent performance (duration, quality, tokens, refinements)
- `OrchestratorMetrics` - Tracks orchestration patterns (total duration, agents used, average quality)
- `MetricsCollector` - Persists to JSON files in `logs/metrics/`

**src/security.py** - Authentication and authorization (JWT tokens, API keys)
**src/cost_management.py** - Token budgeting and cost tracking
**src/durable_execution.py** - Checkpointing for fault tolerance
**src/adaptive_resonance.py** - Self-organizing specialist emergence
**src/stigmergic_coordination.py** - Swarm intelligence coordination

## Common Development Tasks

### When to Use Which Agent

**Simple supervision**: Use `orchestrator` for basic task delegation
**Parallel work**: Use `parallel-orchestrator` for independent concurrent tasks (e.g., multi-source research)
**Complex pipelines**: Use `sequential-orchestrator` for dependent multi-stage workflows
**Multi-perspective synthesis**: Use `hub-orchestrator` for iterative refinement from multiple viewpoints
**Strategic planning**: Invoke `intelligence-agent` to decompose complex tasks and create execution plans
**Quality assurance**: Use `critic-reviewer` for final validation before delivery

### Orchestration Patterns

**Pattern 1: Parallel Execution**
- Use when: Independent tasks, speed priority
- Example: "Research topic X from academic, tutorial, and production sources"
- Result: 3x faster than sequential (tasks run simultaneously)

**Pattern 2: Sequential Pipeline**
- Use when: Dependent tasks, each stage needs previous output
- Example: Research → Write → Review
- Features: Quality gates between stages, audit trail

**Pattern 3: Hub-and-Spoke**
- Use when: Multiple perspectives needed, synthesis required
- Features: Central coordinator, iterative refinement, conflict resolution

### Typical Execution Flow

```
User → intelligence-agent (Strategic Planning)
       ↓
intelligence-agent → control-agent (Execution Management)
       ↓
control-agent → coordination-agent (Prevent Conflicts)
       ↓
coordination-agent → Worker Agents (orchestrator → specialists)
       ↓
Worker Agents → Output artifacts
       ↓
critic-reviewer → Validate quality
       ↓
If quality < 80% → Refinement loop
If quality >= 80% → Deliver to user
```

## Performance Characteristics

**Multi-Agent vs Single Agent**:
- Quality: +15-25% improvement (85-95% vs 70-85%)
- Speed: 0.5-0.7x faster with parallelization
- Token usage: ~15x overhead for coordination
- Success rate: 90%+ on parallelizable tasks

**Good for**:
- Parallelizable research/analysis
- Multiple specialized domains
- High-value complex work
- Context exceeding 200k tokens

**Avoid when**:
- Shared context needed throughout
- Primarily writing/synthesis
- Low-value routine tasks
- Simple sequential work

## File Structure

```
.claude/agents/        # 13 agent definition files (.md with YAML frontmatter)
├── orchestrator.md, parallel-orchestrator.md, sequential-orchestrator.md, hub-orchestrator.md
├── researcher.md, writer.md, critic-reviewer.md
├── policy-agent.md, intelligence-agent.md, control-agent.md, coordination-agent.md
└── [experimental agents in Stage 4]

src/                   # 7 Python modules (standard library, no dependencies for core)
├── validators.py      # CRITIC pattern validation
├── metrics.py         # Performance tracking
├── security.py        # Auth (requires PyJWT>=2.8.0)
├── cost_management.py # Token budgeting
├── durable_execution.py # Checkpointing
├── adaptive_resonance.py # Self-organizing
└── stigmergic_coordination.py # Swarm intelligence

tests/                 # 5 test suites, 18 tests total
├── test-orchestration.py  # Stage 1 validation
├── test-stage2.py         # Patterns + observability
├── test-stage3.py         # VSM hierarchy
├── test-stage4.py         # Experimental features
└── test-stage5.py         # Production features

docs/                  # Implementation guides + tutorials
├── stage-1-foundation-setup.md
├── stage-2-core-patterns-observability.md
├── stage-3-cybernetic-architecture.md
├── stage-4-novel-architectures.md
├── stage-5-production-deployment.md
├── SYSTEM-OVERVIEW.md
└── tutorials/         # 13 agent-specific tutorials

artifacts/             # Agent output files (markdown)
logs/metrics/          # Performance data (JSON)
data/                  # Persistent state (budgets, specialists, executions, stigmergy signals)
```

## Dependencies

**Core**: Python 3.7+ standard library only (no pip installs required for basic functionality)

**Optional** (for Stage 5 production features):
```bash
pip install -r requirements.txt
# PyJWT>=2.8.0 - JWT token functionality in security.py
# Flask>=3.0.0, flask-cors>=4.0.0 - REST API (optional)
```

## Cybernetic Principles

### Requisite Variety (Ashby's Law)
Each VSM level has complexity matching its responsibilities. Orchestrator variety must match system variety.

### Feedback Loops
- **Negative feedback**: Quality gates, refinement requests
- **Positive feedback**: Skill library, pattern reinforcement (Stage 4)
- **Homeostasis**: Self-regulating quality thresholds

### Algedonic Signals
Rapid escalation for critical deviations:
- Quality < 40%: Immediate halt and escalation
- Ethical violations: Alert System 5 (policy-agent)
- Resource exhaustion: Trigger intervention

## Important Implementation Details

### Agent Definitions
All agents are defined in `.claude/agents/*.md` with YAML frontmatter specifying:
- `name` - Agent identifier
- `color` - UI color coding
- `model` - Claude model (opus/sonnet)
- `tools` - Available tool set
- `description` - Purpose and capabilities

### Context Engineering
Critical for success:
- Extremely detailed task descriptions
- Clear boundaries between agent responsibilities
- Explicit output formats
- Tool guidance and source prioritization

### Metrics Collection
`MetricsCollector` persists to JSON automatically:
- Agent metrics: `logs/metrics/agent_{name}_{timestamp}.json`
- Orchestrator metrics: `logs/metrics/orchestrator_{id}.json`

Use for performance analysis, optimization, and debugging.

## References

- **Main Documentation**: README.md, docs/SYSTEM-OVERVIEW.md
- **Agent Coordination**: AGENTS.md (project-level protocols)
- **Tutorial Index**: docs/tutorials/AGENT-TUTORIALS-INDEX.md
- **Stage Guides**: docs/stage-*.md for implementation details
- **VSM Theory**: Stafford Beer's Viable System Model
- **Cybernetics**: W. Ross Ashby's Law of Requisite Variety
