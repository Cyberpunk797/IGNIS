"""
Main evaluation runner.
Usage: python run.py [--problems N] [--max-attempts K] [--subset TYPE]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from client import check_connection
from harness import EvaluationHarness
from grader import compute_metrics, save_results, format_metrics_text, load_results
from compiler import check_compiler


def load_dataset(path: Path = config.DATASET_PATH) -> list:
    """Load problems from JSONL dataset."""
    problems = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems


def filter_problems(problems: list, task_type: str = None,
                   difficulty: str = None, limit: int = None) -> list:
    """Filter problems by criteria."""
    filtered = problems
    
    if task_type:
        filtered = [p for p in filtered if p.get('task_type') == task_type]
    
    if difficulty:
        filtered = [
            problem for problem in filtered
            if problem.get('bucket', problem.get('problem', {}).get('bucket')) == difficulty
        ]
    
    if limit:
        filtered = filtered[:limit]
    
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Run evaluation on CP dataset")
    parser.add_argument('--problems', type=int, default=None,
                       help='Number of problems to test (default: all)')
    parser.add_argument('--max-attempts', type=int, default=config.MAX_ATTEMPTS,
                       help=f'Max attempts per problem (default: {config.MAX_ATTEMPTS})')
    parser.add_argument('--task-type', type=str, default=None,
                       choices=['SFT_SOLVE', 'PLAN_ONLY', 'REPAIR', 'OPTIMIZE'],
                       help='Filter by task type')
    parser.add_argument('--difficulty', type=str, default=None,
                       choices=['fast', 'medium', 'high'],
                       help='Filter by difficulty bucket')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from previous results')
    parser.add_argument('--model-name', type=str, default='aizu_qwen_coder_v1.gguf',
                       help='Model name for report')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("AXLU-ZESI-CP EVALUATION")
    print("=" * 60 + "\n")
    
    print("[1/4] Checking connections...")
    
    compiler_ok, compiler_version = check_compiler()
    if compiler_ok:
        print(f"  [OK] g++: {compiler_version}")
    else:
        print(f"  [FAIL] g++ not found: {compiler_version}")
        print("  Please install MinGW/g++ to compile C++ code")
    
    lm_status = check_connection()
    if lm_status['status'] == 'connected':
        print(f"  [OK] LM Studio: {lm_status['model']}")
    else:
        print(f"  [FAIL] LM Studio: {lm_status.get('error', 'Not connected')}")
        print("  Please start LM Studio server and load your model")
        sys.exit(1)
    
    print("\n[2/4] Loading dataset...")
    all_problems = load_dataset()
    print(f"  Loaded {len(all_problems)} problems")
    
    problems = filter_problems(
        all_problems,
        task_type=args.task_type,
        difficulty=args.difficulty,
        limit=args.problems
    )
    print(f"  Testing {len(problems)} problems")
    
    print(f"\n[3/4] Running evaluation (max {args.max_attempts} attempts each)...")
    
    harness = EvaluationHarness()
    results = harness.evaluate_all(problems, max_attempts=args.max_attempts)
    
    print("[4/4] Computing metrics...")
    metrics = compute_metrics(results)
    
    report = format_metrics_text(metrics, args.model_name)
    print("\n" + report)
    
    save_results(results, metrics)
    print(f"\nResults saved to: {config.RESULTS_DIR}")
    
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
