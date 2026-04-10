"""
Self-Verification Loop
Model checks its own output and tries to fix errors.
"""

import json
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, List, Dict

sys.path.insert(0, str(Path(__file__).parent))

import config
from client import create_client
from extract import extract_cpp_code, clean_code
from compiler import compile_code, check_compiler
from runner import run_tests, cleanup_binary
from prompts import build_prompt, build_verification_prompt, SYSTEM_PROMPT


class SelfVerificationLoop:
    def __init__(self, max_attempts: int = 3):
        self.client = create_client()
        self.max_attempts = max_attempts
    
    def verify_and_fix(self, problem: Dict, test_cases: List[Dict]) -> Tuple[bool, str, int]:
        """
        Attempt to solve problem with self-verification.
        
        Returns:
            Tuple of (success, final_code, attempts_used)
        """
        p = problem.get('problem', problem)
        prompt = build_prompt(problem)
        
        code = None
        attempts = 0
        
        for attempt in range(1, self.max_attempts + 1):
            attempts = attempt
            print(f"  [Verification Attempt {attempt}/{self.max_attempts}]")
            
            if attempt == 1:
                response = self.client.generate(prompt, SYSTEM_PROMPT, max_tokens=1500)
            else:
                code_str = code if code else ""
                verification_prompt = build_verification_prompt(p, code_str)
                response = self.client.generate(
                    verification_prompt, 
                    SYSTEM_PROMPT, 
                    max_tokens=2000
                )
            
            code, _ = extract_cpp_code(response)
            code = clean_code(code) if code else None
            
            if not code:
                print(f"    No code extracted, retrying...")
                continue
            
            success, error, binary_path = compile_code(code)
            
            if not success:
                print(f"    Compilation failed: {error[:100]}...")
                continue
            
            passed, total, _ = run_tests(binary_path, test_cases)
            cleanup_binary(binary_path)
            
            if passed == total:
                print(f"    All tests passed! ({passed}/{total})")
                return True, code, attempts
            else:
                print(f"    Tests failed: {passed}/{total}, attempting fix...")
        
        return False, code if code else "", attempts


def run_self_verification(num_problems: int = 10, max_attempts: int = 3):
    """Run self-verification on multiple problems."""
    
    print("=" * 70)
    print("SELF-VERIFICATION EVALUATION")
    print("=" * 70)
    print(f"Problems: {num_problems}")
    print(f"Max attempts per problem: {max_attempts}")
    print("=" * 70 + "\n")
    
    with open(config.DATASET_PATH, 'r', encoding='utf-8') as f:
        problems = [json.loads(line) for line in f][:num_problems]
    
    verifier = SelfVerificationLoop(max_attempts=max_attempts)
    
    results = []
    
    for i, problem in enumerate(problems, 1):
        p = problem.get('problem', problem)
        title = p.get('title', 'Untitled')
        
        samples = p.get('samples', [])
        test_cases = [
            {'input': s.get('input', ''), 'expected': s.get('output', '')} 
            for s in samples
        ]
        
        print(f"[{i}/{len(problems)}] {title}...")
        
        success, code, attempts = verifier.verify_and_fix(problem, test_cases)
        
        status = "[PASS]" if success else "[FAIL]"
        print(f"  Result: {status} (used {attempts} attempts)\n")
        
        results.append({
            'title': title,
            'success': success,
            'attempts': attempts
        })
    
    passed = sum(1 for r in results if r['success'])
    
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Pass Rate: {passed}/{len(results)} ({passed/len(results)*100:.0f}%)")
    print(f"Average attempts: {sum(r['attempts'] for r in results)/len(results):.1f}")
    print("=" * 70)
    
    return results


def compare_with_baseline(num_problems: int = 10):
    """Compare self-verification vs single attempt."""
    
    print("\n" + "=" * 70)
    print("BASELINE COMPARISON")
    print("=" * 70)
    
    with open(config.DATASET_PATH, 'r', encoding='utf-8') as f:
        problems = [json.loads(line) for line in f][:num_problems]
    
    print("\n[1] Testing single attempt (no verification)...")
    baseline_results = []
    
    for i, problem in enumerate(problems, 1):
        p = problem.get('problem', problem)
        title = p.get('title', 'Untitled')
        
        samples = p.get('samples', [])
        test_cases = [
            {'input': s.get('input', ''), 'expected': s.get('output', '')} 
            for s in samples
        ]
        
        print(f"  [{i}/{len(problems)}] {title}...", end=' ')
        
        prompt = build_prompt(problem)
        client = create_client()
        
        try:
            response = client.generate(prompt, SYSTEM_PROMPT, max_tokens=1500)
            code, _ = extract_cpp_code(response)
            code = clean_code(code) if code else None
            
            if not code:
                print("NO CODE")
                baseline_results.append(False)
                continue
            
            success, error, binary_path = compile_code(code)
            
            if not success:
                print("COMPILE ERROR")
                baseline_results.append(False)
                continue
            
            passed, total, _ = run_tests(binary_path, test_cases)
            cleanup_binary(binary_path)
            
            status = "PASS" if passed == total else "FAIL"
            print(status)
            baseline_results.append(passed == total)
            
        except Exception as e:
            print(f"ERROR: {str(e)[:50]}")
            baseline_results.append(False)
    
    baseline_passed = sum(baseline_results)
    
    print(f"\nBaseline (single attempt): {baseline_passed}/{len(problems)} ({baseline_passed/len(problems)*100:.0f}%)")
    
    print("\n[2] Testing with self-verification...")
    sv_results = run_self_verification(num_problems, max_attempts=3)
    
    sv_passed = sum(1 for r in sv_results if r['success'])
    
    print(f"\nSelf-verification: {sv_passed}/{len(sv_results)} ({sv_passed/len(sv_results)*100:.0f}%)")
    
    improvement = sv_passed - baseline_passed
    print(f"\nImprovement: +{improvement} problems ({'+' if improvement >= 0 else ''}{improvement/len(problems)*100:.0f}%)")
    
    return baseline_results, sv_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Self-verification evaluation")
    parser.add_argument('--problems', type=int, default=10, help='Number of problems')
    parser.add_argument('--max-attempts', type=int, default=3, help='Max verification attempts')
    parser.add_argument('--compare', action='store_true', help='Compare with baseline')
    
    args = parser.parse_args()
    
    if args.compare:
        compare_with_baseline(args.problems)
    else:
        run_self_verification(args.problems, args.max_attempts)
