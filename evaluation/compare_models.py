"""
Compare Fine-tuned Model vs Original Qwen Model
Tests both models on the same problems and generates comparison report.
"""

import json
import time
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent))

import config
from client import create_client
from extract import extract_cpp_code, clean_code
from compiler import compile_code, check_compiler
from runner import run_tests, cleanup_binary


def load_dataset(path: Path = config.DATASET_PATH) -> list:
    """Load problems from JSONL dataset."""
    problems = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems


def evaluate_single(model_name: str, prompt: str, system_prompt: str, test_cases: list) -> dict:
    """Evaluate one problem on current model."""
    client = create_client()
    
    start_time = time.time()
    try:
        response = client.generate(prompt, system_prompt)
    except Exception as e:
        return {
            "model": model_name,
            "success": False,
            "compiled": False,
            "passed": 0,
            "total": len(test_cases),
            "error": str(e),
            "latency": time.time() - start_time,
            "code": None
        }
    
    latency = time.time() - start_time
    
    code, _ = extract_cpp_code(response)
    code = clean_code(code) if code else None
    
    if not code:
        return {
            "model": model_name,
            "success": False,
            "compiled": False,
            "passed": 0,
            "total": len(test_cases),
            "error": "No code extracted",
            "latency": latency,
            "code": None
        }
    
    success, error, binary_path = compile_code(code)
    
    if not success:
        return {
            "model": model_name,
            "success": False,
            "compiled": False,
            "passed": 0,
            "total": len(test_cases),
            "error": error[:200],
            "latency": latency,
            "code": code[:500]
        }
    
    passed, total, _ = run_tests(binary_path, test_cases)
    cleanup_binary(binary_path)
    
    return {
        "model": model_name,
        "success": passed == total,
        "compiled": True,
        "passed": passed,
        "total": total,
        "error": None,
        "latency": latency,
        "code": code[:500]
    }


def run_comparison(num_problems: int = 20):
    """Run comparison between fine-tuned and original models."""
    
    print("=" * 70)
    print("MODEL COMPARISON: Fine-tuned vs Original Qwen")
    print("=" * 70)
    
    from prompts import build_prompt, SYSTEM_PROMPT
    
    problems = load_dataset()[:num_problems]
    
    print(f"\nComparing on {len(problems)} problems...")
    print("\n" + "-" * 70)
    
    finetuned_results = []
    original_results = []
    
    for i, problem in enumerate(problems, 1):
        p = problem.get('problem', problem)
        title = p.get('title', 'Untitled')
        
        samples = p.get('samples', [])
        test_cases = []
        for s in samples:
            test_cases.append({
                'input': s.get('input', ''),
                'expected': s.get('output', '')
            })
        
        prompt = build_prompt(problem)
        
        print(f"\n[{i}/{len(problems)}] {title}")
        
        print("  Testing with current model (fine-tuned)...")
        ft_result = evaluate_single("fine-tuned", prompt, SYSTEM_PROMPT, test_cases)
        finetuned_results.append(ft_result)
        
        ft_status = "[PASS]" if ft_result['success'] else "[FAIL]"
        ft_compile = "[COMPILED]" if ft_result['compiled'] else "[FAILED]"
        print(f"    {ft_status} {ft_compile} ({ft_result['passed']}/{ft_result['total']} tests) - {ft_result['latency']:.1f}s")
        
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    
    ft_passed = sum(1 for r in finetuned_results if r['success'])
    ft_compiled = sum(1 for r in finetuned_results if r['compiled'])
    ft_avg_latency = sum(r['latency'] for r in finetuned_results) / len(finetuned_results)
    
    print(f"\nFine-tuned Model ({config.MODEL_NAME or 'current'}):")
    print(f"  Pass Rate:      {ft_passed}/{len(finetuned_results)} ({ft_passed/len(finetuned_results)*100:.1f}%)")
    print(f"  Compile Rate:   {ft_compiled}/{len(finetuned_results)} ({ft_compiled/len(finetuned_results)*100:.1f}%)")
    print(f"  Avg Latency:    {ft_avg_latency:.1f}s")
    
    print("\n" + "-" * 70)
    print("\nNOTE: To compare with original Qwen model:")
    print("  1. In LM Studio, unload fine-tuned model")
    print("  2. Load original Qwen2.5-3B model")
    print("  3. Run: python compare_models.py")
    print("\n" + "-" * 70)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "num_problems": len(problems),
        "fine_tuned": {
            "pass_rate": ft_passed / len(finetuned_results),
            "compile_rate": ft_compiled / len(finetuned_results),
            "avg_latency": ft_avg_latency,
            "results": finetuned_results
        }
    }
    
    output_path = config.RESULTS_DIR / "comparison_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare model performance")
    parser.add_argument('--problems', type=int, default=20,
                       help='Number of problems to test')
    args = parser.parse_args()
    
    run_comparison(args.problems)
