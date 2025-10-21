# Writer Agent - Tutorial Guide

**Agent Type**: Content Synthesis Specialist  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Green  

---

## Overview

The **Writer** is a content synthesis specialist that transforms research, requirements, and raw information into clear, well-structured written content including tutorials, guides, documentation, and reports.

### What It Does

- Synthesizes information from multiple sources into cohesive content
- Creates well-structured documents with logical organization
- Writes for specific target audiences with appropriate tone
- Generates technical documentation with code examples
- Polishes content for clarity and consistency

### When to Use

✅ **Use the writer when you need to**:
- Transform research into structured documents
- Create tutorials, guides, or reports
- Write technical documentation
- Generate content from specifications
- Polish and structure existing information

❌ **Don't use for**:
- Primary research or information gathering (use researcher)
- Task coordination (use orchestrator)
- Code validation (use critic-reviewer)
- Strategic planning (use intelligence-agent)

---

## Installation

### Step 1: Verify Agent File Exists

The writer agent is configured at:
```
.claude/agents/writer.md
```

### Step 2: Understanding the Configuration

```yaml
---
name: writer
description: Content synthesis and writing specialist. Creates well-structured documents from research and requirements.
tools: Read, Write
model: opus
color: green
---
```

**Key capabilities**:
- Reads research and requirements
- Writes structured content
- Uses Opus for highest quality output
- Specializes in technical writing

---

## Usage Examples

### Example 1: Creating a Tutorial from Research

**Your Request**:
```
"Using the research in artifacts/async-research.md, write a beginner-friendly 
tutorial about Python async/await with step-by-step examples"
```

**What the Writer Does**:

1. **Content Planning**:
   - Reviews research findings
   - Identifies key concepts for beginners
   - Plans tutorial structure (intro → basics → examples → summary)
   - Notes where code examples needed

2. **Organization**:
   - Groups related concepts
   - Orders by difficulty (simple to complex)
   - Plans transitions between sections

3. **Writing**:
   - Clear introduction explaining async/await
   - Step-by-step progression
   - Runnable code examples with comments
   - Best practices and common pitfalls

4. **Polish**:
   - Checks flow between sections
   - Verifies code examples work
   - Proofreads for clarity
   - Ensures consistent formatting

**Output**: `artifacts/async-tutorial.md`

### Example 2: Technical Documentation

**Your Request**:
```
"Write API documentation for the MetricsCollector class based on src/metrics.py"
```

**What the Writer Does**:

1. **Code Analysis**:
   - Reads source code
   - Identifies classes, methods, parameters
   - Understands functionality

2. **Documentation Structure**:
   - Class overview
   - Method descriptions
   - Parameter details
   - Usage examples
   - Return value specifications

3. **Example Generation**:
   - Creates practical usage examples
   - Shows common patterns
   - Demonstrates error handling

**Output**: Reference-style documentation with API details

### Example 3: Multi-Source Synthesis

**Your Request**:
```
"Synthesize these three research reports into one comprehensive guide"
```

**What the Writer Does**:

1. **Source Integration**:
   - Reads all three reports
   - Identifies overlapping information
   - Notes unique contributions from each

2. **Unified Structure**:
   - Creates logical organization
   - Eliminates redundancy
   - Ensures smooth flow

3. **Synthesis**:
   - Combines complementary information
   - Resolves any contradictions
   - Creates cohesive narrative

---

## Expected Outputs

### Tutorial Format

```markdown
# {Topic}: A Practical Tutorial
Author: writer
Date: 2024-01-15T14:00:00Z
Audience: {target-audience}
Type: Tutorial

{Brief description}

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Step 1: {Title}](#step-1)
4. [Step 2: {Title}](#step-2)
5. [Summary](#summary)

## Introduction
{Context and learning objectives}

## Prerequisites
- {requirement-1}
- {requirement-2}

## Step 1: {Title}
{Instruction with explanation}

**Example**:
```python
# Code example with comments
```

**Key Points**:
- {takeaway-1}
- {takeaway-2}

## Summary
{Recap and next steps}
```

### Guide Format

```markdown
# {Topic} Guide
Author: writer
Type: Guide

## Overview
{What this guide covers}

## Core Concepts
{Key ideas explained}

## Best Practices
{Recommended approaches}

## Common Patterns
{Proven solutions}

## Troubleshooting
{Common issues and fixes}
```

---

## Tips & Best Practices

### 1. Provide Clear Input

✅ **Good**:
```
"Write tutorial using artifacts/research.md, targeting intermediate developers,
tutorial style with code examples and exercises"
```

❌ **Vague**:
```
"Make a document about this"
```

### 2. Specify Audience

Be explicit about target readers:
- "Beginners new to programming"
- "Intermediate Python developers"
- "Advanced users familiar with asyncio"

The writer adjusts tone and complexity accordingly.

### 3. Define Document Type

Choose appropriate format:
- **Tutorial**: Step-by-step learning
- **Guide**: Comprehensive reference
- **Report**: Analysis and findings
- **Reference**: Quick lookup information

### 4. Request Code Examples

When needed:
```
"Include runnable code examples for each concept"
```

Writer will:
- Ensure examples actually work
- Add explanatory comments
- Show correct and incorrect patterns

### 5. Specify Structure

If you have preferences:
```
"Organize as: Introduction → Fundamentals → Advanced Topics → Exercises"
```

---

## Troubleshooting

### Issue: Output Too Technical

**Solution**: Specify audience more clearly
```
"Write for complete beginners with no prior async experience"
```

### Issue: Missing Code Examples

**Solution**: Explicitly request them
```
"Include at least one code example per major concept"
```

### Issue: Wrong Document Type

**Solution**: Be specific about format
```
"Create a tutorial (not a reference guide) with step-by-step instructions"
```

### Issue: Content Too Brief

**Solution**: Request depth
```
"Write comprehensive guide covering all aspects in detail"
```

---

## Working with Other Agents

### With Researcher
**Common workflow**: Research → Write

```
Researcher produces: artifacts/research.md
Writer transforms into: artifacts/guide.md
```

### With Orchestrator
**Coordinated by orchestrator** in multi-phase projects:

```
Orchestrator delegates:
1. Research phase → researcher
2. Writing phase → writer
3. Review phase → critic-reviewer
```

### With Critic-Reviewer
**Quality validation workflow**:

```
Writer produces: artifacts/draft.md
Critic reviews: artifacts/feedback.md
Writer refines: artifacts/final.md
```

---

## Advanced Usage

### Multi-Document Types

Request multiple formats:
```
"Create both a quick-start tutorial AND comprehensive reference guide"
```

Writer produces:
- Tutorial for learning
- Reference for lookup

### Custom Templates

Specify exact structure:
```
"Use this structure:
1. Executive Summary
2. Technical Details
3. Implementation Guide
4. API Reference
5. Examples"
```

### Code-Heavy Documentation

For code-centric content:
```
"Write documentation with code-to-text ratio of 60:40, 
extensive commenting, and real-world examples"
```

---

## Document Type Details

### Tutorial
**Best for**: Teaching concepts through practice  
**Structure**: Intro → Steps → Examples → Exercises → Summary  
**Tone**: Instructional, encouraging  
**Code**: Lots of runnable examples

### Guide
**Best for**: Comprehensive topic coverage  
**Structure**: Overview → Concepts → Practices → Patterns → Troubleshooting  
**Tone**: Authoritative, thorough  
**Code**: Examples showing best practices

### Reference
**Best for**: Quick information lookup  
**Structure**: Alphabetical or topical grouping  
**Tone**: Concise, factual  
**Code**: Short usage snippets

### Report
**Best for**: Presenting findings and analysis  
**Structure**: Summary → Methodology → Findings → Analysis → Recommendations  
**Tone**: Professional, objective  
**Code**: Supporting evidence where relevant

---

## Quality Self-Check

The writer evaluates its own output across:

### Clarity
- One idea per paragraph
- Active voice preferred
- Concrete examples provided
- Technical terms defined

### Structure
- Logical progression
- Clear hierarchy (headings)
- Scannable format (bullets, code blocks)
- Smooth transitions

### Completeness
- All required topics covered
- Nothing important omitted
- Examples for key concepts

### Accuracy
- Technical correctness verified
- Code examples tested
- Facts checked against sources

---

## Performance Expectations

**For Tutorial Creation**:
- Duration: 1-2 hours
- Quality: 85-95%
- Token Usage: 15,000-30,000
- Refinement: 0-1 cycles typically

**For Technical Documentation**:
- Duration: 1-3 hours depending on complexity
- Quality: 90-95% (higher standards)
- Token Usage: 20,000-40,000
- Refinement: 1-2 cycles for accuracy

---

## Next Steps

After mastering the writer:

1. **Combine with Research**: Learn [researcher-tutorial.md](./researcher-tutorial.md)
2. **Add Validation**: Try [critic-reviewer-tutorial.md](./critic-reviewer-tutorial.md)
3. **Orchestrate Workflows**: Use [orchestrator-tutorial.md](./orchestrator-tutorial.md)
4. **Sequential Pipelines**: Explore [sequential-orchestrator-tutorial.md](./sequential-orchestrator-tutorial.md)

---

## Summary

The **Writer** agent transforms research and requirements into polished, well-structured content.

**Strengths**:
- Clear, audience-appropriate writing
- Logical organization and flow
- Technical accuracy with code examples
- Multiple document format support
- Quality polish and consistency

**Perfect for**: Content creation, technical documentation, tutorials, guides, and synthesis of information into readable formats.

---

**Ready to try?** Start with:
```
"Write a beginner-friendly tutorial about [topic] with examples"
```

The writer will handle the rest!
