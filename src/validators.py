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
