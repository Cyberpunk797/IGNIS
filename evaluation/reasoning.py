"""
Reasoning quality checker.
Evaluates the quality of reasoning in model responses.
"""

import re
from typing import Dict, List


class ReasoningQuality:
    def __init__(self):
        self.has_core_idea: bool = False
        self.has_algorithm_steps: bool = False
        self.has_data_structures: bool = False
        self.has_invariant: bool = False
        self.has_edge_cases: bool = False
        self.has_complexity: bool = False
        self.has_code: bool = False
        self.score: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            "has_core_idea": self.has_core_idea,
            "has_algorithm_steps": self.has_algorithm_steps,
            "has_data_structures": self.has_data_structures,
            "has_invariant": self.has_invariant,
            "has_edge_cases": self.has_edge_cases,
            "has_complexity": self.has_complexity,
            "has_code": self.has_code,
            "score": self.score
        }


def check_reasoning_quality(text: str, has_code: bool = False) -> ReasoningQuality:
    """
    Check reasoning quality of model response.
    
    Args:
        text: The text response from the model
        has_code: Whether code was extracted
        
    Returns:
        ReasoningQuality object with scores
    """
    quality = ReasoningQuality()
    text_lower = text.lower()
    
    core_idea_patterns = [
        r'core\s*idea',
        r'key\s*observation',
        r'main\s*insight',
        r'fundamental',
        r'key\s*point'
    ]
    quality.has_core_idea = any(re.search(p, text_lower) for p in core_idea_patterns)
    
    step_patterns = [
        r'step\s*\d',
        r'\d+\.\s*[a-z]',
        r'first\s*,?\s*second',
        r'algorithm\s*step',
        r'procedure'
    ]
    quality.has_algorithm_steps = any(re.search(p, text_lower) for p in step_patterns)
    
    ds_patterns = [
        r'vector',
        r'array',
        r'stack',
        r'queue',
        r'deque',
        r'map',
        r'set',
        r'heap',
        r'tree',
        r'graph',
        r'list'
    ]
    quality.has_data_structures = any(re.search(p, text_lower) for p in ds_patterns)
    
    invariant_patterns = [
        r'invariant',
        r'correctness',
        r'prove',
        r'why\s*it\s*work',
        r'maintain'
    ]
    quality.has_invariant = any(re.search(p, text_lower) for p in invariant_patterns)
    
    edge_patterns = [
        r'edge\s*case',
        r'corner\s*case',
        r'boundary',
        r'empty',
        r'single',
        r'zero'
    ]
    quality.has_edge_cases = any(re.search(p, text_lower) for p in edge_patterns)
    
    complexity_patterns = [
        r'o\([^)]+\)',
        r'time\s*complexity',
        r'space\s*complexity',
        r'big\s*o',
        r'\d+\s*\*\s*log'
    ]
    quality.has_complexity = any(re.search(p, text_lower) for p in complexity_patterns)
    
    quality.has_code = has_code
    
    score = (
        (1.5 if quality.has_core_idea else 0) +
        (1.5 if quality.has_algorithm_steps else 0) +
        (1.0 if quality.has_data_structures else 0) +
        (1.5 if quality.has_invariant else 0) +
        (1.0 if quality.has_edge_cases else 0) +
        (1.5 if quality.has_complexity else 0) +
        (2.0 if quality.has_code else 0)
    )
    max_score = 10.0
    quality.score = min(score / max_score, 1.0)
    
    return quality


def format_reasoning_report(quality: ReasoningQuality) -> str:
    """Format reasoning quality as readable text."""
    lines = ["Reasoning Quality Report:", "=" * 30]
    
    items = [
        ("Core Idea", quality.has_core_idea),
        ("Algorithm Steps", quality.has_algorithm_steps),
        ("Data Structures", quality.has_data_structures),
        ("Correctness/Invariant", quality.has_invariant),
        ("Edge Cases", quality.has_edge_cases),
        ("Complexity", quality.has_complexity),
        ("Code Provided", quality.has_code),
    ]
    
    for name, present in items:
        status = "[OK]" if present else "[MISSING]"
        lines.append(f"  {status} {name}")
    
    lines.append(f"\nOverall Score: {quality.score:.1%}")
    
    return "\n".join(lines)
