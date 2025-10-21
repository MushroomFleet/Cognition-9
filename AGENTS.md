# AGENTS.md - Project Agent Configuration

## Project Overview
Multi-agent orchestration system for coordinated task execution using Claude Code's native custom agent capabilities.

## Agent Coordination Model
This project uses a supervisor pattern with the following agents:
- **Orchestrator**: Coordinates work between specialists
- **Researcher**: Gathers and analyzes information
- **Writer**: Synthesizes findings into structured output

## Handoff Protocol
Agents communicate through markdown artifacts stored in `artifacts/`:
- `artifacts/research-output.md`: Research findings
- `artifacts/synthesis-output.md`: Final synthesized output
- `artifacts/feedback.md`: Quality feedback and corrections

## Quality Standards
All agent outputs must:
- Include clear reasoning for decisions
- Cite sources where applicable
- Follow markdown formatting conventions
- Include metadata (agent name, timestamp, confidence level)

## Execution Flow
1. User provides task to Orchestrator
2. Orchestrator analyzes and decomposes task
3. Orchestrator delegates to appropriate specialist(s)
4. Specialists complete work and save to artifacts
5. Orchestrator reviews outputs for quality
6. If quality threshold not met, request refinement
7. Deliver final synthesized result

## Development Commands
- Test individual agent: `# Test researcher agent with sample task`
- Run full workflow: `# Execute complete orchestration`
- View logs: `cat logs/execution-{timestamp}.log`
