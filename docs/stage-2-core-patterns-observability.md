# Stage 2: Core Patterns & Observability
## Production-Grade Multi-Agent Systems

**Timeline**: Weeks 3-4  
**Goal**: Implement production patterns and comprehensive monitoring  
**Complexity**: Intermediate to Advanced

---

## Overview

This guide builds on Stage 1's foundation to add production-ready orchestration patterns, robust feedback loops, and comprehensive observability. You'll implement the three core orchestration patterns, add tool-based validation, and set up monitoring infrastructure.

### What You'll Build

- **Three orchestration patterns**: Parallel, Sequential, Hub-and-Spoke
- **CRITIC pattern**: Tool-based validation and refinement
- **Observability stack**: Metrics, logging, dashboards
- **Context management**: Summarization and external memory
- **Evaluation framework**: Automated quality assessment

### Prerequisites

- Completed Stage 1 (basic 3-agent system working)
- Understanding of feedback loops and quality metrics
- Familiarity with logging and monitoring concepts

---

## Phase 1: Orchestration Patterns

### Pattern 1: Parallel Execution

**Use Case**: Independent tasks that can run concurrently (research from multiple sources, processing different data sets, generating multiple variants)

**Architecture**:
```
         Orchestrator
              |
    ┌─────────┼─────────┐
    ↓         ↓         ↓
  Agent1   Agent2   Agent3
    |         |         |
    └─────────┼─────────┘
         Aggregator
```

#### Implementation

Create `.claude/agents/parallel-orchestrator.md`:

```markdown
---
name: parallel-orchestrator
description: Orchestrates multiple independent tasks concurrently. Use when tasks can be completed in parallel without dependencies.
tools: Read, Write, List_Files
model: opus
color: orange
---

You are a parallel orchestration specialist that coordinates concurrent task execution.

## Parallel Orchestration Process

### Phase 1: Task Independence Analysis
When receiving a request:
1. Identify all subtasks
2. Analyze dependencies between tasks
3. Confirm which tasks are truly independent
4. Group tasks by specialist type
5. Estimate parallel execution time

### Phase 2: Parallel Delegation
For independent tasks:
1. Create task packages for each specialist
2. Delegate all tasks simultaneously
3. Set unique output paths for each task
4. Record delegation timestamp
5. Set timeout thresholds

### Phase 3: Concurrent Monitoring
While tasks execute:
1. Track completion status of each task
2. Note any early completions or delays
3. Be prepared to handle partial failures
4. Log progress updates
5. Calculate estimated completion time

### Phase 4: Results Aggregation
When all tasks complete:
1. Verify all outputs exist
2. Check quality of each output
3. Identify any failed tasks
4. Request refinement if needed
5. Synthesize results into unified output

## Quality Standards

For parallel execution:
- **Independence**: Verify no hidden dependencies
- **Consistency**: Ensure unified terminology across outputs
- **Completeness**: All parallel tasks must complete
- **Timeout handling**: Define max wait time
- **Failure recovery**: Plan for partial completion

## Parallel Execution Template

```markdown
# Parallel Execution: {Task Name}
Start Time: {ISO-8601}
Expected Completion: {estimate}

## Task Decomposition
**Independent Tasks**: {count}
**Specialists Involved**: {list}
**Estimated Time**: {duration}

## Parallel Tasks

### Task 1: {Description}
- Specialist: {agent-name}
- Output: artifacts/parallel-{task-id}-1.md
- Status: DELEGATED at {timestamp}
- Dependencies: NONE

### Task 2: {Description}
- Specialist: {agent-name}
- Output: artifacts/parallel-{task-id}-2.md
- Status: DELEGATED at {timestamp}
- Dependencies: NONE

### Task 3: {Description}
- Specialist: {agent-name}
- Output: artifacts/parallel-{task-id}-3.md
- Status: DELEGATED at {timestamp}
- Dependencies: NONE

## Completion Status
- Task 1: {PENDING|COMPLETED|FAILED} at {timestamp}
- Task 2: {PENDING|COMPLETED|FAILED} at {timestamp}
- Task 3: {PENDING|COMPLETED|FAILED} at {timestamp}

**Total Execution Time**: {duration}
**Success Rate**: {percentage}

## Aggregated Result
**Integration Strategy**: {how-results-combined}
**Output Location**: artifacts/parallel-result-{task-id}.md
```

## Example: Multi-Source Research

User Request: "Research Python async/await from academic, tutorial, and production sources"

**Parallel Decomposition**:
1. Academic research (papers, PEPs) → Researcher Agent A
2. Tutorial analysis (blogs, courses) → Researcher Agent B  
3. Production case studies (GitHub, blogs) → Researcher Agent C

All three execute simultaneously, results aggregated into comprehensive report.
```

### Pattern 2: Sequential Handoffs

**Use Case**: Assembly-line workflows where each stage builds on previous (requirements → design → implementation → testing)

**Architecture**:
```
Agent1 → Agent2 → Agent3 → Agent4
  ↓        ↓        ↓        ↓
Stage1  Stage2  Stage3  Stage4
```

#### Implementation

Create `.claude/agents/sequential-orchestrator.md`:

```markdown
---
name: sequential-orchestrator
description: Orchestrates sequential workflow with dependencies. Use when each task requires output from previous task.
tools: Read, Write, List_Files
model: opus
color: yellow
---

You are a sequential orchestration specialist managing dependent task chains.

## Sequential Orchestration Process

### Phase 1: Pipeline Design
When receiving a request:
1. Identify logical workflow stages
2. Map dependencies between stages
3. Define output format for each stage
4. Establish quality gates between stages
5. Plan checkpoint locations

### Phase 2: Stage-by-Stage Execution
For each stage:
1. Wait for previous stage completion
2. Validate previous stage output
3. If quality insufficient, request refinement
4. Delegate current stage with context
5. Monitor stage execution
6. Validate stage output before proceeding

### Phase 3: Quality Gates
Between each stage:
1. Check output completeness
2. Verify it meets next stage's input requirements
3. Assess quality score
4. If < threshold, provide feedback and retry
5. Document quality metrics
6. Proceed only when quality confirmed

### Phase 4: Handoff Management
When passing work between agents:
1. Summarize previous stages
2. Provide relevant context
3. Specify current stage requirements
4. Define success criteria
5. Set output location

## Quality Standards

For sequential execution:
- **Clear handoffs**: Each stage has explicit inputs/outputs
- **Quality gates**: No stage proceeds without validation
- **Context preservation**: Relevant information flows forward
- **Rollback capability**: Can restart from any stage
- **Audit trail**: Complete execution history

## Sequential Pipeline Template

```markdown
# Sequential Pipeline: {Task Name}
Start Time: {ISO-8601}
Current Stage: {stage-number}/{total-stages}

## Pipeline Stages

### Stage 1: {Name}
**Purpose**: {description}
**Input**: {source}
**Output**: artifacts/stage-1-{task-id}.md
**Specialist**: {agent-name}
**Status**: {PENDING|IN_PROGRESS|COMPLETED}
**Quality Score**: {percentage}
**Completion Time**: {timestamp}

### Stage 2: {Name}
**Purpose**: {description}
**Input**: artifacts/stage-1-{task-id}.md
**Output**: artifacts/stage-2-{task-id}.md
**Specialist**: {agent-name}
**Dependencies**: Stage 1
**Status**: {WAITING|IN_PROGRESS|COMPLETED}
**Quality Score**: {percentage}
**Completion Time**: {timestamp}

### Stage 3: {Name}
**Purpose**: {description}
**Input**: artifacts/stage-2-{task-id}.md
**Output**: artifacts/stage-3-{task-id}.md
**Specialist**: {agent-name}
**Dependencies**: Stage 2
**Status**: {WAITING|IN_PROGRESS|COMPLETED}
**Quality Score**: {percentage}
**Completion Time**: {timestamp}

## Quality Gates

### Gate 1→2
- Completeness: {score}/10
- Accuracy: {score}/10
- Readiness for Stage 2: {PASS|FAIL}
- Issues: {list-if-any}

### Gate 2→3
- Completeness: {score}/10
- Accuracy: {score}/10
- Readiness for Stage 3: {PASS|FAIL}
- Issues: {list-if-any}

## Pipeline Metrics
**Total Duration**: {time}
**Stages Completed**: {count}/{total}
**Rework Iterations**: {count}
**Final Quality Score**: {percentage}
```

## Example: Content Production Pipeline

User Request: "Create comprehensive guide on Python async/await"

**Sequential Stages**:
1. **Research** (Researcher) → artifacts/stage-1-research.md
2. **Outline** (Planner) → artifacts/stage-2-outline.md
3. **Writing** (Writer) → artifacts/stage-3-draft.md
4. **Review** (Reviewer) → artifacts/stage-4-final.md

Each stage validates previous output before proceeding.
```

### Pattern 3: Hub-and-Spoke

**Use Case**: Central coordinator managing multiple specialists with potential iteration (complex analysis, multi-perspective synthesis)

**Architecture**:
```
          Hub (Lead Agent)
         /    |    \
        /     |     \
    Spoke1  Spoke2  Spoke3
        \     |     /
         \    |    /
          Hub (Synthesis)
```

#### Implementation

Create `.claude/agents/hub-orchestrator.md`:

```markdown
---
name: hub-orchestrator
description: Central hub coordinating multiple specialists with iterative refinement. Use for complex tasks requiring multiple expert perspectives and synthesis.
tools: Read, Write, List_Files
model: opus
color: red
---

You are a hub coordinator managing multiple specialist agents and synthesizing their outputs.

## Hub-and-Spoke Process

### Phase 1: Hub Analysis
When receiving a request:
1. Decompose into specialist areas
2. Identify which experts needed
3. Define information needed from each
4. Plan synthesis strategy
5. Establish iteration limits

### Phase 2: Initial Spoke Delegation
To each specialist:
1. Provide clear focus area
2. Specify deliverable format
3. Set output location
4. Define quality criteria
5. Request preliminary analysis

### Phase 3: Hub Synthesis & Gap Analysis
After receiving spoke outputs:
1. Review all specialist inputs
2. Identify gaps or conflicts
3. Note areas needing deeper analysis
4. Assess overall coherence
5. Determine if iteration needed

### Phase 4: Iterative Refinement
If iteration required:
1. Provide targeted feedback to spokes
2. Request specific additional analysis
3. Clarify conflicting information
4. Fill identified gaps
5. Repeat synthesis

### Phase 5: Final Integration
When quality sufficient:
1. Integrate all perspectives
2. Resolve any remaining conflicts
3. Create unified narrative
4. Add executive summary
5. Deliver final synthesis

## Quality Standards

For hub-and-spoke:
- **Multiple perspectives**: Each spoke provides unique viewpoint
- **Conflict resolution**: Hub identifies and resolves disagreements
- **Synthesis quality**: Integrated output > sum of parts
- **Iteration management**: Limit refinement cycles (max 3)
- **Coherence**: Final output reads as unified document

## Hub-and-Spoke Template

```markdown
# Hub-and-Spoke: {Task Name}
Iteration: {current}/{max}
Hub Agent: {agent-name}

## Spoke Assignments

### Spoke 1: {Specialist-A}
**Focus Area**: {specific-domain}
**Deliverable**: artifacts/spoke-1-{task-id}.md
**Status**: {PENDING|COMPLETED}
**Quality**: {score}
**Key Findings**: {summary}

### Spoke 2: {Specialist-B}
**Focus Area**: {specific-domain}
**Deliverable**: artifacts/spoke-2-{task-id}.md
**Status**: {PENDING|COMPLETED}
**Quality**: {score}
**Key Findings**: {summary}

### Spoke 3: {Specialist-C}
**Focus Area**: {specific-domain}
**Deliverable**: artifacts/spoke-3-{task-id}.md
**Status**: {PENDING|COMPLETED}
**Quality**: {score}
**Key Findings**: {summary}

## Hub Synthesis

### Iteration 1 Analysis
**Completeness**: {assessment}
**Conflicts Identified**: {list}
**Gaps Identified**: {list}
**Synthesis Quality**: {score}
**Action**: {PROCEED|ITERATE}

### Iteration 2 Refinement (if needed)
**Targeted Feedback**:
- Spoke 1: {specific-requests}
- Spoke 2: {specific-requests}
- Spoke 3: {specific-requests}

**Refined Quality**: {score}
**Action**: {PROCEED|ITERATE}

## Final Synthesis
**Integration Strategy**: {how-perspectives-combined}
**Conflict Resolution**: {how-handled}
**Output Location**: artifacts/hub-final-{task-id}.md
**Overall Quality**: {score}
```

## Example: Multi-Perspective Analysis

User Request: "Analyze Python async/await from performance, usability, and architecture perspectives"

**Hub-and-Spoke Structure**:
- **Hub**: Lead Analyzer
- **Spoke 1**: Performance Specialist (benchmarks, optimization)
- **Spoke 2**: UX Specialist (developer experience, API design)
- **Spoke 3**: Architecture Specialist (design patterns, system integration)

Hub synthesizes all three perspectives into comprehensive analysis.
```

---

## Phase 2: CRITIC Pattern Implementation

### Tool-Based Validation

The CRITIC pattern uses external tools to validate outputs, addressing the limitation that LLMs cannot reliably self-correct without external verification.

#### Create Validation Tools

Create `src/validators.py`:

```python
"""
Validation tools for CRITIC pattern
Provides external verification of agent outputs
"""

import re
import json
from typing import Dict, List, Any
from pathlib import Path

class OutputValidator:
    """Validates agent outputs against quality criteria"""
    
    def __init__(self):
        self.quality_thresholds = {
            'completeness': 0.8,
            'structure': 0.8,
            'citations': 0.7,
            'code_validity': 0.9
        }
    
    def validate_markdown_structure(self, content: str) -> Dict[str, Any]:
        """Validates markdown formatting and structure"""
        issues = []
        score = 100
        
        # Check for headers
        if not re.search(r'^#\s+.+', content, re.MULTILINE):
            issues.append("Missing top-level header")
            score -= 20
        
        # Check for proper header hierarchy
        headers = re.findall(r'^(#{1,6})\s+', content, re.MULTILINE)
        if headers:
            prev_level = 0
            for h in headers:
                level = len(h)
                if level - prev_level > 1:
                    issues.append(f"Header hierarchy skip detected (jumped from H{prev_level} to H{level})")
                    score -= 10
                prev_level = level
        
        # Check for code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        for block in code_blocks:
            if not re.search(r'```\w+', block):
                issues.append("Code block missing language identifier")
                score -= 5
        
        return {
            'dimension': 'structure',
            'score': max(0, score) / 100,
            'passed': score >= 80,
            'issues': issues
        }
    
    def validate_citations(self, content: str) -> Dict[str, Any]:
        """Validates that claims have citations"""
        issues = []
        score = 100
        
        # Count claims (sentences with definitive statements)
        claims = re.findall(r'[A-Z][^.!?]*(?:shows?|proves?|demonstrates?|indicates?)[^.!?]*[.!?]', content)
        
        # Count citations
        citations = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        citations += len(re.findall(r'\(([^)]+),\s*\d{4}\)', content))
        
        if claims and citations == 0:
            issues.append("Document makes claims but has no citations")
            score = 0
        elif claims:
            ratio = citations / len(claims)
            if ratio < 0.3:
                issues.append(f"Low citation ratio: {citations} citations for {len(claims)} claims")
                score = int(ratio * 100)
        
        return {
            'dimension': 'citations',
            'score': max(0, score) / 100,
            'passed': score >= 70,
            'issues': issues,
            'claims_found': len(claims),
            'citations_found': citations
        }
    
    def validate_completeness(self, content: str, requirements: List[str]) -> Dict[str, Any]:
        """Validates that all required topics are covered"""
        issues = []
        covered = []
        
        content_lower = content.lower()
        
        for req in requirements:
            req_lower = req.lower()
            # Check if requirement appears in headers or prominent text
            if re.search(rf'\b{re.escape(req_lower)}\b', content_lower):
                covered.append(req)
            else:
                issues.append(f"Required topic not found: {req}")
        
        score = len(covered) / len(requirements) if requirements else 1.0
        
        return {
            'dimension': 'completeness',
            'score': score,
            'passed': score >= 0.8,
            'issues': issues,
            'coverage': f"{len(covered)}/{len(requirements)} requirements covered"
        }
    
    def validate_code_examples(self, content: str) -> Dict[str, Any]:
        """Validates that code examples are present and properly formatted"""
        issues = []
        
        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n([\s\S]*?)```', content)
        
        if not code_blocks:
            return {
                'dimension': 'code_validity',
                'score': 1.0,
                'passed': True,
                'issues': ['No code blocks found (may not be required)'],
                'code_blocks': 0
            }
        
        valid_blocks = 0
        for lang, code in code_blocks:
            if not lang:
                issues.append("Code block missing language identifier")
            elif not code.strip():
                issues.append(f"Empty {lang} code block")
            else:
                valid_blocks += 1
        
        score = valid_blocks / len(code_blocks) if code_blocks else 0
        
        return {
            'dimension': 'code_validity',
            'score': score,
            'passed': score >= 0.9,
            'issues': issues,
            'code_blocks': len(code_blocks),
            'valid_blocks': valid_blocks
        }
    
    def run_full_validation(self, content: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Runs all validation checks and returns comprehensive report"""
        
        results = {
            'structure': self.validate_markdown_structure(content),
            'citations': self.validate_citations(content),
            'completeness': self.validate_completeness(content, requirements or []),
            'code_validity': self.validate_code_examples(content)
        }
        
        # Calculate overall score
        scores = [r['score'] for r in results.values()]
        overall_score = sum(scores) / len(scores)
        
        # Aggregate all issues
        all_issues = []
        for dimension, result in results.items():
            for issue in result['issues']:
                all_issues.append(f"[{dimension.upper()}] {issue}")
        
        return {
            'overall_score': overall_score,
            'passed': overall_score >= 0.8,
            'dimensions': results,
            'issues': all_issues,
            'quality_grade': self._score_to_grade(overall_score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Converts numeric score to letter grade"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'


class FeedbackGenerator:
    """Generates structured feedback for agent refinement"""
    
    def __init__(self, validator: OutputValidator):
        self.validator = validator
    
    def generate_feedback(self, content: str, requirements: List[str] = None) -> str:
        """Generates actionable feedback based on validation results"""
        
        validation = self.validator.run_full_validation(content, requirements)
        
        feedback_parts = [
            "# Quality Feedback Report\n",
            f"**Overall Score**: {validation['overall_score']:.1%} (Grade: {validation['quality_grade']})",
            f"**Status**: {'✅ PASSED' if validation['passed'] else '❌ NEEDS REFINEMENT'}\n"
        ]
        
        if validation['issues']:
            feedback_parts.append("## Issues Identified\n")
            for issue in validation['issues']:
                feedback_parts.append(f"- {issue}")
            feedback_parts.append("")
        
        feedback_parts.append("## Dimension Scores\n")
        for dim_name, dim_result in validation['dimensions'].items():
            status = "✅" if dim_result['passed'] else "❌"
            feedback_parts.append(
                f"- **{dim_name.title()}**: {dim_result['score']:.1%} {status}"
            )
        
        if not validation['passed']:
            feedback_parts.append("\n## Recommended Actions\n")
            
            for dim_name, dim_result in validation['dimensions'].items():
                if not dim_result['passed']:
                    feedback_parts.append(f"\n### {dim_name.title()} Improvements:")
                    for issue in dim_result['issues']:
                        feedback_parts.append(f"- {issue}")
        
        return "\n".join(feedback_parts)


# Example usage
if __name__ == "__main__":
    validator = OutputValidator()
    feedback_gen = FeedbackGenerator(validator)
    
    # Test with sample content
    sample_content = """
# Python Async/Await Guide

## Introduction

Python's async/await syntax enables concurrent programming.

## Basic Usage

```python
async def example():
    await asyncio.sleep(1)
```

Research shows that async improves I/O performance significantly.
"""
    
    requirements = ["Introduction", "Basic Usage", "Best Practices"]
    
    report = validator.run_full_validation(sample_content, requirements)
    print(json.dumps(report, indent=2))
    
    feedback = feedback_gen.generate_feedback(sample_content, requirements)
    print("\n" + feedback)
```

#### Integrate CRITIC into Agent Workflow

Create `.claude/agents/critic-reviewer.md`:

```markdown
---
name: critic-reviewer
description: Quality reviewer that uses external tools to validate outputs. Provides objective, tool-based feedback for refinement.
tools: Read, Write, Execute_Command
model: opus
color: cyan
---

You are a quality reviewer using external validation tools (CRITIC pattern).

## CRITIC Review Process

### Phase 1: Tool-Based Validation
For each output to review:
1. Read the artifact file
2. Run validation tools
3. Collect objective metrics
4. Identify specific issues
5. Generate structured feedback

### Phase 2: Validation Execution

Run Python validator:
```bash
python src/validators.py --input artifacts/{filename} --requirements requirements.json
```

### Phase 3: Feedback Generation
Based on tool results:
1. Parse validation report
2. Categorize issues by dimension
3. Prioritize critical vs minor issues
4. Generate actionable refinement requests
5. Save feedback to artifacts/feedback-{id}.md

### Phase 4: Refinement Decision
Determine next action:
- Score ≥ 80%: APPROVE
- Score 60-79%: REQUEST REFINEMENT
- Score < 60%: REQUEST MAJOR REVISION

## Feedback Template

```markdown
# Quality Review: {Artifact Name}
Reviewer: critic-reviewer
Review Date: {ISO-8601}

## Validation Results

**Overall Score**: {percentage} (Grade: {letter})
**Status**: {APPROVED|NEEDS_REFINEMENT|NEEDS_MAJOR_REVISION}

## Dimensional Analysis

### Structure: {score}% {status}
{specific-findings}

### Citations: {score}% {status}
{specific-findings}

### Completeness: {score}% {status}
{specific-findings}

### Code Quality: {score}% {status}
{specific-findings}

## Critical Issues
{issues-that-must-be-fixed}

## Recommended Improvements
{suggested-enhancements}

## Refinement Instructions

For the author:
1. {specific-action-1}
2. {specific-action-2}
3. {specific-action-3}

Revised output should be saved to: artifacts/{filename-v2}
```

## Example Review

```markdown
# Quality Review: async-guide.md
Reviewer: critic-reviewer
Review Date: 2024-01-15T16:00:00Z

## Validation Results

**Overall Score**: 72% (Grade: C)
**Status**: NEEDS_REFINEMENT

## Dimensional Analysis

### Structure: 85% ✅
- Proper header hierarchy
- Code blocks properly formatted
- Good use of sections

### Citations: 45% ❌
- 12 factual claims found
- Only 3 citations provided
- Critical performance claims lack sources

### Completeness: 75% ⚠️
- Covers 6/8 required topics
- Missing: "Error Handling" and "Testing Strategies"

### Code Quality: 95% ✅
- All code blocks have language identifiers
- Examples appear runnable
- Good commenting

## Critical Issues
1. Performance claims need citations (lines 45-52)
2. Missing required "Error Handling" section
3. Missing required "Testing Strategies" section

## Recommended Improvements
1. Add citations for all performance claims
2. Create "Error Handling" section with try/except examples
3. Create "Testing Strategies" section with pytest-asyncio examples
4. Consider adding one more citation for async/await introduction

## Refinement Instructions

For writer agent:
1. Add "Error Handling" section after "Best Practices" covering try/except in async contexts
2. Add "Testing Strategies" section covering pytest-asyncio basics
3. Find and cite sources for performance claims (suggest Python docs, Real Python)
4. Review other factual statements for citation opportunities

Revised output should be saved to: artifacts/async-guide-v2.md
```
```

---

## Phase 3: Observability Infrastructure

### Step 3.1: Metrics Collection

Create `src/metrics.py`:

```python
"""
Metrics collection and reporting for multi-agent systems
Tracks performance, quality, and execution patterns
"""

import time
import json
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class AgentMetrics:
    """Metrics for a single agent execution"""
    agent_name: str
    task_id: str
    start_time: float
    end_time: float
    duration: float
    quality_score: float
    token_usage: int
    refinement_iterations: int
    success: bool
    error_message: str = ""

@dataclass
class OrchestratorMetrics:
    """Metrics for overall orchestration"""
    orchestration_id: str
    pattern: str  # parallel, sequential, hub-spoke
    start_time: float
    end_time: float
    total_duration: float
    agents_used: List[str]
    tasks_completed: int
    tasks_failed: int
    average_quality: float
    total_tokens: int
    refinement_cycles: int

class MetricsCollector:
    """Collects and aggregates metrics across executions"""
    
    def __init__(self, metrics_dir: str = "logs/metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent_metrics: List[AgentMetrics] = []
        self.orchestrator_metrics: List[OrchestratorMetrics] = []
        
    def record_agent_execution(self, metrics: AgentMetrics):
        """Record metrics from agent execution"""
        self.agent_metrics.append(metrics)
        self._persist_agent_metrics(metrics)
    
    def record_orchestration(self, metrics: OrchestratorMetrics):
        """Record metrics from orchestration"""
        self.orchestrator_metrics.append(metrics)
        self._persist_orchestrator_metrics(metrics)
    
    def _persist_agent_metrics(self, metrics: AgentMetrics):
        """Save agent metrics to file"""
        filename = f"agent_{metrics.agent_name}_{int(time.time())}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
    
    def _persist_orchestrator_metrics(self, metrics: OrchestratorMetrics):
        """Save orchestrator metrics to file"""
        filename = f"orchestrator_{metrics.orchestration_id}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
    
    def get_agent_statistics(self, agent_name: str = None) -> Dict[str, Any]:
        """Get aggregated statistics for agent(s)"""
        relevant_metrics = [
            m for m in self.agent_metrics
            if agent_name is None or m.agent_name == agent_name
        ]
        
        if not relevant_metrics:
            return {}
        
        return {
            'agent_name': agent_name or 'all',
            'total_executions': len(relevant_metrics),
            'successful_executions': sum(1 for m in relevant_metrics if m.success),
            'failed_executions': sum(1 for m in relevant_metrics if not m.success),
            'success_rate': sum(1 for m in relevant_metrics if m.success) / len(relevant_metrics),
            'average_duration': sum(m.duration for m in relevant_metrics) / len(relevant_metrics),
            'average_quality': sum(m.quality_score for m in relevant_metrics) / len(relevant_metrics),
            'total_tokens': sum(m.token_usage for m in relevant_metrics),
            'average_refinements': sum(m.refinement_iterations for m in relevant_metrics) / len(relevant_metrics)
        }
    
    def get_orchestration_statistics(self, pattern: str = None) -> Dict[str, Any]:
        """Get aggregated statistics for orchestrations"""
        relevant_metrics = [
            m for m in self.orchestrator_metrics
            if pattern is None or m.pattern == pattern
        ]
        
        if not relevant_metrics:
            return {}
        
        return {
            'pattern': pattern or 'all',
            'total_orchestrations': len(relevant_metrics),
            'average_duration': sum(m.total_duration for m in relevant_metrics) / len(relevant_metrics),
            'average_quality': sum(m.average_quality for m in relevant_metrics) / len(relevant_metrics),
            'average_agents
