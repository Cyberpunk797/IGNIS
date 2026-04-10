"""
Run full evaluation with Pass@1, Pass@2, Pass@3 metrics.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from harness import EvaluationHarness
from grader import compute_metrics, save_results, format_metrics_text

def load_problems():
    """Load problems from dataset."""
    problems = []
    path = Path(__file__).parent.parent / "dataset" / "build" / "train_full.jsonl"
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            if data.get('task_type') == 'SFT_SOLVE':
                problems.append(data)
    
    return problems[:20]  # Test on first 20 problems

def main():
    print("=" * 60)
    print("IGNIS EVALUATION - Pass@K METRICS")
    print("=" * 60)
    
    problems = load_problems()
    print(f"Loaded {len(problems)} problems\n")
    
    harness = EvaluationHarness()
    
    print("Running evaluation with up to 3 attempts per problem...")
    print("(Self-verification loop: generate → test → repair if fail)\n")
    
    results = harness.evaluate_all(problems, max_attempts=3, verbose=True)
    
    metrics = compute_metrics(results)
    
    print("\n" + "=" * 60)
    print("RESULTS - SELF-VERIFICATION LOOP")
    print("=" * 60)
    
    print(f"""
┌─────────────────────────────────────────────────┐
│  Pass@1:  {metrics.pass_at_1:.1%}  (first attempt only)         │
│  Pass@2:  {metrics.pass_at_2:.1%}  (within 2 attempts)          │
│  Pass@3:  {metrics.pass_at_3:.1%}  (within 3 attempts)          │
└─────────────────────────────────────────────────┘
""")
    
    print(f"Compilation Rate: {metrics.compilation_rate:.1%}")
    print(f"Avg Tests Passed: {metrics.avg_tests_passed:.1%}")
    print(f"Avg Reasoning Score: {metrics.avg_reasoning_score:.1%}")
    
    save_results(results, metrics)
    print("\n[Results saved to evaluation/results/]")
    print("\nKey metrics for your GitHub README:")
    print(f"  Pass@1: {metrics.pass_at_1:.0%}")
    print(f"  Pass@2: {metrics.pass_at_2:.0%}")
    print(f"  Pass@3: {metrics.pass_at_3:.0%}")

if __name__ == "__main__":
    main()
