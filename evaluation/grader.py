"""
Grading utilities for evaluation metrics.
Computes Pass@K, compilation rates, and other metrics.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import config


@dataclass
class ProblemResult:
    problem_id: str
    title: str
    difficulty: str
    topic: str
    task_type: str
    
    attempts: int
    solved: bool
    solved_at_attempt: Optional[int]
    
    compiled: bool
    compile_error: Optional[str]
    
    tests_passed: int
    tests_total: int
    
    reasoning_score: float
    
    latency: float
    response_length: int
    
    all_attempts: List[Dict]


@dataclass
class EvaluationMetrics:
    total_problems: int
    solved_count: int
    
    pass_at_1: float
    pass_at_2: float
    pass_at_3: float
    
    compilation_rate: float
    avg_tests_passed: float
    
    avg_reasoning_score: float
    avg_latency: float
    
    by_difficulty: Dict[str, Dict]
    by_topic: Dict[str, Dict]
    by_task_type: Dict[str, Dict]


def compute_pass_at_k(results: List[ProblemResult], k: int) -> float:
    """Compute Pass@K metric."""
    if not results:
        return 0.0
    
    solved = sum(1 for r in results if r.solved_at_attempt is not None and r.solved_at_attempt <= k)
    return solved / len(results)


def compute_metrics(results: List[ProblemResult]) -> EvaluationMetrics:
    """Compute all evaluation metrics."""
    if not results:
        return EvaluationMetrics(
            total_problems=0,
            solved_count=0,
            pass_at_1=0.0,
            pass_at_2=0.0,
            pass_at_3=0.0,
            compilation_rate=0.0,
            avg_tests_passed=0.0,
            avg_reasoning_score=0.0,
            avg_latency=0.0,
            by_difficulty={},
            by_topic={},
            by_task_type={}
        )
    
    total = len(results)
    solved = sum(1 for r in results if r.solved)
    
    compiled = sum(1 for r in results if r.compiled)
    
    total_tests = sum(r.tests_total for r in results)
    passed_tests = sum(r.tests_passed for r in results)
    
    avg_tests = passed_tests / total_tests if total_tests > 0 else 0
    
    avg_reasoning = sum(r.reasoning_score for r in results) / total
    avg_latency = sum(r.latency for r in results) / total
    
    by_difficulty = _group_by(results, 'difficulty')
    by_topic = _group_by(results, 'topic')
    by_task_type = _group_by(results, 'task_type')
    
    return EvaluationMetrics(
        total_problems=total,
        solved_count=solved,
        pass_at_1=compute_pass_at_k(results, 1),
        pass_at_2=compute_pass_at_k(results, 2),
        pass_at_3=compute_pass_at_k(results, 3),
        compilation_rate=compiled / total,
        avg_tests_passed=avg_tests,
        avg_reasoning_score=avg_reasoning,
        avg_latency=avg_latency,
        by_difficulty=by_difficulty,
        by_topic=by_topic,
        by_task_type=by_task_type
    )


def _group_by(results: List[ProblemResult], key: str) -> Dict[str, Dict]:
    """Group results by a field and compute metrics."""
    groups = {}
    
    for r in results:
        value = getattr(r, key, 'unknown')
        if value not in groups:
            groups[value] = []
        groups[value].append(r)
    
    return {
        name: {
            "count": len(items),
            "pass_at_1": compute_pass_at_k(items, 1),
            "pass_at_2": compute_pass_at_k(items, 2),
            "pass_at_3": compute_pass_at_k(items, 3),
        }
        for name, items in groups.items()
    }


def save_results(results: List[ProblemResult], metrics: EvaluationMetrics,
                 raw_path: Optional[Path] = None,
                 metrics_path: Optional[Path] = None):
    """Save results and metrics to files."""
    if raw_path is None:
        raw_path = config.RESULTS_DIR / "raw_results.jsonl"
    
    if metrics_path is None:
        metrics_path = config.RESULTS_DIR / "metrics.json"
    
    with open(raw_path, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(asdict(r), ensure_ascii=False) + '\n')
    
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(metrics), f, indent=2, ensure_ascii=False)


def load_results(raw_path: Optional[Path] = None) -> List[ProblemResult]:
    """Load results from file."""
    if raw_path is None:
        raw_path = config.RESULTS_DIR / "raw_results.jsonl"
    
    results = []
    with open(raw_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            results.append(ProblemResult(**data))
    
    return results


def format_metrics_text(metrics: EvaluationMetrics, model_name: str = "Unknown") -> str:
    """Format metrics as readable text report."""
    lines = [
        "=" * 60,
        "EVALUATION REPORT",
        "=" * 60,
        f"Model: {model_name}",
        f"Date: 2026-04-09",
        f"Problems Tested: {metrics.total_problems}",
        "",
        "-" * 40,
        "OVERALL RESULTS",
        "-" * 40,
        f"Pass@1:  {metrics.pass_at_1:.1%}  (first attempt)",
        f"Pass@2:  {metrics.pass_at_2:.1%}  (within 2 attempts)",
        f"Pass@3:  {metrics.pass_at_3:.1%}  (within 3 attempts)",
        f"",
        f"Compilation Rate: {metrics.compilation_rate:.1%}",
        f"Avg Tests Passed: {metrics.avg_tests_passed:.1%}",
        f"Avg Reasoning Score: {metrics.avg_reasoning_score:.1%}",
        f"Avg Latency: {metrics.avg_latency:.1f}s",
    ]
    
    if metrics.by_difficulty:
        lines.extend(["", "-" * 40, "BY DIFFICULTY", "-" * 40])
        for diff, stats in sorted(metrics.by_difficulty.items()):
            lines.append(f"  {diff}: Pass@1={stats['pass_at_1']:.1%} ({stats['count']} problems)")
    
    if metrics.by_topic:
        lines.extend(["", "-" * 40, "BY TOPIC", "-" * 40])
        for topic, stats in sorted(metrics.by_topic.items()):
            lines.append(f"  {topic}: Pass@1={stats['pass_at_1']:.1%} ({stats['count']} problems)")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)
