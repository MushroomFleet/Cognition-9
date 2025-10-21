# Researcher Agent - Tutorial Guide

**Agent Type**: Information Gathering Specialist  
**System Level**: Operations (System 1)  
**Model**: Claude Opus  
**Color**: Blue  

---

## Overview

The **Researcher** is a specialized agent for comprehensive information gathering, analysis, and synthesis from multiple sources.

### What It Does

- Gathers information from multiple authoritative sources
- Evaluates source credibility and relevance
- Identifies patterns and trends across sources
- Synthesizes findings into structured research reports
- Provides confidence levels and citations

### When to Use

✅ **Use the researcher when you need to**:
- Gather information from multiple sources
- Conduct literature reviews
- Compare different approaches or technologies
- Synthesize findings from diverse sources
- Provide well-cited, credible research

❌ **Don't use for**:
- Content creation or writing (use writer instead)
- Simple fact-checking (too heavyweight)
- Tasks not requiring source synthesis

---

## Installation

### Agent File Location
```
.claude/agents/researcher.md
```

### Configuration
```yaml
---
name: researcher
description: Research specialist for gathering and analyzing information. Use for comprehensive information gathering tasks.
tools: Read, Web_Search, Grep
model: opus
color: blue
---
```

**Key capabilities**:
- `Web_Search`: Can search the internet for information
- `Grep`: Can search through files and code
- `Read`: Can read existing documents

---

## Usage Examples

### Example 1: Technology Research

**Request**:
```
"Research Python async/await - find best practices, common pitfalls, 
and performance characteristics"
```

**What Happens**:

1. **Scope Definition**:
   - Key questions: What is async/await? Best practices? Common pitfalls?
   - Sources needed: Official docs, tutorials, production case studies

2. **Information Collection**:
   - Searches Python documentation
   - Reviews tutorial sites (Real Python, etc.)
   - Examines production examples on GitHub
   - Collects 10-15 sources

3. **Analysis & Synthesis**:
   - Groups findings by theme
   - Identifies consensus vs conflicting info
   - Assesses confidence in each finding

4. **Report Generation**:
   ```markdown
   # Research Report: Python Async/Await
   
   ## Executive Summary
   [Key findings in 2-3 paragraphs]
   
   ## Key Findings
   1. Async is for I/O-bound tasks (Confidence: 95%)
   2. Use create_task() for concurrency (Confidence: 90%)
   [...]
   
   ## Detailed Analysis
   [In-depth discussion with citations]
   
   ## Source Bibliography
   [All sources listed]
   ```

**Output**: `artifacts/async-research.md`

### Example 2: Comparative Analysis

**Request**:
```
"Research and compare asyncio vs threading vs multiprocessing in Python"
```

**Output Structure**:
- Overview of each approach
- Use cases for each
- Performance characteristics
- Pros and cons comparison
- Recommendation matrix
- Cited sources

---

## Research Depth Levels

The researcher adapts depth based on task:

### Preliminary (1-3 sources)
- Quick fact-checking
- Basic concept definition
- Initial feasibility assessment

### Moderate (4-7 sources)
- Standard information gathering
- Multiple perspectives
- Comparing approaches

### Comprehensive (8+ sources)
- Deep domain analysis
- Academic literature review
- Production best practices
- Conflicting information resolution

**Specify depth in your request**:
```
"Do comprehensive research on topic X" → 8+ sources
"Quick research on topic Y" → 1-3 sources
```

---

## Output Format

Standard research report structure:

```markdown
# Research Report: {Topic}
Researcher: researcher
Date: {ISO-8601}
Confidence: {percentage}

## Executive Summary
[2-3 paragraphs]

## Research Scope
**Questions Addressed**: [list]
**Sources Consulted**: {count}
**Research Depth**: {preliminary|moderate|comprehensive}

## Key Findings

### Finding 1: {Title}
**Summary**: [1-2 sentences]
**Evidence**: [details]
**Source**: [citation]
**Credibility**: {High|Medium|Low}
**Confidence**: {percentage}

## Detailed Analysis
[Themed sections with integrated sources]

## Conflicting Viewpoints
[Where sources disagree + analysis]

## Recommendations
- For immediate use: [actionable items]
- For further research: [gaps identified]

## Source Bibliography
[Complete citations]
```

---

## Tips & Best Practices

### 1. Be Specific About What You Need

✅ **Good**:
```
"Research Python async/await focusing on:
- When to use vs threading
- Common mistakes beginners make
- Performance benchmarks
- Best practices from production use"
```

❌ **Vague**:
```
"Research async stuff"
```

### 2. Specify Depth if Non-Standard

```
"Do quick preliminary research" → 1-3 sources
"Comprehensive deep-dive research" → 8+ sources
```

### 3. Indicate Source Preferences

```
"Research prioritizing:
- Official documentation
- Academic papers
- Production case studies"
```

### 4. Check Citations

Research reports include citations - verify sources if critical.

### 5. Note Confidence Levels

Researcher provides confidence for each finding:
- 90-100%: High confidence
- 70-89%: Moderate confidence  
- <70%: Low confidence (needs more research)

---

## Troubleshooting

### Issue: Sources Not Credible

**Solution**: Specify source types in request
```
"Research using only official docs and academic papers"
```

### Issue: Not Comprehensive Enough

**Solution**: Request deeper research
```
"Do comprehensive research with 10+ sources"
```

### Issue: Missing Key Topics

**Solution**: List specific requirements
```
"Research must cover: [topic 1], [topic 2], [topic 3]"
```

---

## Working with Other Agents

### Typical Workflow Combinations

**Research → Write**:
```
orchestrator receives: "Research X and write guide"
→ researcher gathers information
→ writer creates guide from research
```

**Research → Validate**:
```
parallel-orchestrator: "Research from multiple perspectives"
→ multiple researcher instances
→ critic-reviewer validates synthesis
```

---

## Related Tutorials

- **[Orchestrator](./orchestrator-tutorial.md)** - Coordinates research tasks
- **[Writer](./writer-tutorial.md)** - Uses research for content creation
- **[Parallel Orchestrator](./parallel-orchestrator-tutorial.md)** - Multi-source research

---

## Next Steps

1. Try a simple research task
2. Experiment with different depth levels
3. Practice with comparative research
4. Combine with writer for full workflows

---

**Ready to research?** Try:
```
"Research [your topic] with comprehensive analysis"
