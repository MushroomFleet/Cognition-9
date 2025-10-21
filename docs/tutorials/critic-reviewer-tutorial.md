# Critic-Reviewer - Tutorial Guide

**Agent Type**: Quality Validation Specialist (CRITIC Pattern)  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Cyan  

---

## Overview

The **Critic-Reviewer** uses external validation tools to provide objective, tool-based quality assessment of agent outputs, implementing the CRITIC pattern for reliable self-correction.

### What It Does

- Validates outputs using Python validation tools
- Generates objective quality scores across multiple dimensions
- Provides actionable, specific feedback for refinement
- Makes approval/refinement/rejection decisions
- Tracks quality metrics over time

### When to Use

✅ **Use critic-reviewer when**:
- Need objective quality validation
- Want tool-based (not just LLM-based) assessment
- Require specific, actionable feedback
- Implementing quality assurance workflows
- Final validation before delivery

❌ **Don't use for**:
- Simple tasks not requiring validation
- When subjective assessment preferred
- Tasks where quality metrics unclear

---

## How It Works

### Validation Process

1. **Read Output**: Loads artifact to review
2. **Run Validators**: Executes `src/validators.py`
3. **Collect Metrics**: Gathers objective scores
4. **Generate Feedback**: Creates actionable recommendations
5. **Make Decision**: APPROVE (≥80%) / REFINE (60-79%) / REJECT (<60%)

### Validation Dimensions

**Structure (0-100%)**:
- Markdown formatting
- Header hierarchy
- Code block formatting

**Citations (0-100%)**:
- Claims vs citations ratio
- Source credibility
- Attribution completeness

**Completeness (0-100%)**:
- Required topics coverage
- Content thoroughness
- Missing sections

**Code Quality (0-100%)**:
- Language identifiers present
- Non-empty code blocks
- Example validity

---

## Usage Example

**Your Request**:
```
"Review the tutorial at artifacts/async-guide.md and provide quality feedback"
```

**What Happens**:

1. **Validation Execution**:
   ```bash
   python src/validators.py --input artifacts/async-guide.md
   ```

2. **Results**:
   ```
   Structure: 85% ✓
   Citations: 45% ✗
   Completeness: 75% ⚠️
   Code Quality: 95% ✓
   
   Overall: 75% → NEEDS REFINEMENT
   ```

3. **Feedback Generated**:
   ```markdown
   # Quality Review: async-guide.md
   
   ## Critical Issues
   1. Performance claims lack citations (lines 45-52)
   2. Missing "Error Handling" section (required)
   3. Missing "Testing Strategies" section (required)
   
   ## Refinement Instructions
   1. Add citations for performance claims
   2. Create "Error Handling" section with try/except examples
   3. Add "Testing Strategies" section with pytest-asyncio
   
   Revised output: artifacts/async-guide-v2.md
   ```

**Output**: `artifacts/feedback-{id}.md` with specific improvement instructions

---

## Expected Outputs

### Quality Review Report

```markdown
# Quality Review: {Artifact Name}
Reviewer: critic-reviewer
Review Date: 2024-01-15T16:00:00Z

## Validation Results

**Overall Score**: 72% (Grade: C)
**Status**: NEEDS_REFINEMENT

## Dimensional Analysis

### Structure: 85% ✅
- Proper header hierarchy
- Code blocks properly formatted
- Good section organization

### Citations: 45% ❌
- 12 factual claims found
- Only 3 citations provided
- Critical claims lack sources

### Completeness: 75% ⚠️
- 6/8 required topics covered
- Missing: Error Handling, Testing

### Code Quality: 95% ✅
- All blocks have language identifiers
- Examples appear runnable
- Good commenting

## Critical Issues
{Specific problems that must be fixed}

## Recommended Improvements
{Actionable suggestions}

## Refinement Instructions
{Step-by-step fix guidance}
```

---

## Tips & Best Practices

### 1. Provide Requirements

For best validation:
```
"Review this guide and ensure it covers:
- Introduction
- Basic Usage
- Best Practices
- Error Handling
- Testing Strategies"
```

### 2. Use in Workflows

Integrate into quality pipelines:
```
writer → critic-reviewer → (refine if needed) → final
```

### 3. Trust the Tools

CRITIC uses objective validation:
- Not subjective opinion
- Measurable criteria
- Consistent standards

### 4. Iterate Based on Feedback

Follow refinement instructions exactly for best results

---

## Working with Validation Tools

### Running Validators Directly

```bash
# Validate a file
python src/validators.py artifacts/myfile.md

# With requirements
python src/validators.py artifacts/myfile.md \
  --requirements "Intro,Usage,Examples,Best Practices"
```

### Validation Output

```json
{
  "overall_score": 0.75,
  "quality_grade": "C",
  "passed": false,
  "dimensions": {
    "structure": {"score": 0.85, "passed": true},
    "citations": {"score": 0.45, "passed": false},
    "completeness": {"score": 0.75, "passed": false},
    "code_validity": {"score": 0.95, "passed": true}
  },
  "issues": [
    "[CITATIONS] Low citation ratio",
    "[COMPLETENESS] Required topic not found: Error Handling"
  ]
}
```

---

## Summary

The **Critic-Reviewer** provides objective, tool-based quality validation using the CRITIC pattern for reliable assessment and actionable feedback.

**Perfect for**: Quality assurance workflows, validation gates, automated review, and ensuring outputs meet measurable standards before delivery.

---

**Ready to try?**:
```
"Review artifacts/mydocument.md for quality and provide feedback"
