"""
Evaluation harness - orchestrates the full evaluation pipeline.
"""

import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

import config
from client import create_client, LMStudioClient
from extract import extract_cpp_code, clean_code
from compiler import compile_code, check_compiler
from runner import run_tests, cleanup_binary, TestResult
from prompts import build_prompt, SYSTEM_PROMPT
from reasoning import check_reasoning_quality, ReasoningQuality
from grader import ProblemResult


@dataclass
class AttemptResult:
    attempt_number: int
    success: bool
    compiled: bool
    tests_passed: int
    tests_total: int
    response: str
    code: Optional[str]
    compile_error: Optional[str]
    reasoning: str
    latency: float
    test_results: List[TestResult] = field(default_factory=list)


class EvaluationHarness:
    def __init__(self, client: Optional[LMStudioClient] = None):
        self.client = client or create_client()
        self.compiler_available, self.compiler_version = check_compiler()
        
    def evaluate_problem(self, problem: Dict, max_attempts: int = config.MAX_ATTEMPTS) -> ProblemResult:
        """
        Evaluate a single problem against the model.
        
        Returns ProblemResult with all attempts and final metrics.
        """
        p = problem.get('problem', problem)
        problem_id = problem.get('id', p.get('problem_id', 'unknown'))
        title = p.get('title', 'Untitled')
        difficulty = problem.get('bucket', 'unknown')
        topic = p.get('tags', ['unknown'])[0] if p.get('tags') else 'unknown'
        task_type = problem.get('task_type', 'SFT_SOLVE')
        
        samples = p.get('samples', [])
        test_cases = []
        for s in samples:
            test_cases.append({
                'input': s.get('input', ''),
                'expected': s.get('output', '')
            })
        
        prompt = build_prompt(problem)
        
        attempts: List[AttemptResult] = []
        solved = False
        solved_at = None
        all_code = []
        all_reasoning = []
        
        for attempt in range(1, max_attempts + 1):
            start_time = time.time()
            
            try:
                response = self.client.generate(prompt, SYSTEM_PROMPT)
            except Exception as e:
                print(f"  [Attempt {attempt}] Error: {e}")
                attempts.append(AttemptResult(
                    attempt_number=attempt,
                    success=False,
                    compiled=False,
                    tests_passed=0,
                    tests_total=len(test_cases),
                    response="",
                    code=None,
                    compile_error=str(e),
                    reasoning="",
                    latency=0
                ))
                continue
            
            latency = time.time() - start_time
            
            code, reasoning = extract_cpp_code(response)
            code = clean_code(code) if code else None
            all_code.append(code)
            all_reasoning.append(reasoning)
            
            if not code:
                print(f"  [Attempt {attempt}] No code extracted")
                attempts.append(AttemptResult(
                    attempt_number=attempt,
                    success=False,
                    compiled=False,
                    tests_passed=0,
                    tests_total=len(test_cases),
                    response=response,
                    code=None,
                    compile_error="No code in response",
                    reasoning=reasoning,
                    latency=latency
                ))
                continue
            
            success, error, binary_path = compile_code(code)
            
            if not success:
                print(f"  [Attempt {attempt}] Compilation failed")
                attempts.append(AttemptResult(
                    attempt_number=attempt,
                    success=False,
                    compiled=False,
                    tests_passed=0,
                    tests_total=len(test_cases),
                    response=response,
                    code=code,
                    compile_error=error,
                    reasoning=reasoning,
                    latency=latency
                ))
                continue
            
            passed, total, test_results = run_tests(binary_path, test_cases)
            cleanup_binary(binary_path)
            
            success = passed == total
            print(f"  [Attempt {attempt}] Tests: {passed}/{total}")
            
            attempts.append(AttemptResult(
                attempt_number=attempt,
                success=success,
                compiled=True,
                tests_passed=passed,
                tests_total=total,
                response=response,
                code=code,
                compile_error=None,
                reasoning=reasoning,
                latency=latency,
                test_results=test_results
            ))
            
            if success:
                solved = True
                solved_at = attempt
                break
        
        best_attempt = attempts[-1] if attempts else None
        reasoning_quality = check_reasoning_quality(
            best_attempt.reasoning if best_attempt else "",
            bool(best_attempt.code if best_attempt else None)
        )
        
        return ProblemResult(
            problem_id=problem_id,
            title=title,
            difficulty=difficulty,
            topic=topic,
            task_type=task_type,
            attempts=len(attempts),
            solved=solved,
            solved_at_attempt=solved_at,
            compiled=best_attempt.compiled if best_attempt else False,
            compile_error=best_attempt.compile_error if best_attempt else None,
            tests_passed=best_attempt.tests_passed if best_attempt else 0,
            tests_total=best_attempt.tests_total if best_attempt else len(test_cases),
            reasoning_score=reasoning_quality.score,
            latency=sum(a.latency for a in attempts),
            response_length=len(best_attempt.response) if best_attempt else 0,
            all_attempts=[
                {
                    "attempt": a.attempt_number,
                    "success": a.success,
                    "compiled": a.compiled,
                    "tests_passed": a.tests_passed,
                    "latency": a.latency,
                }
                for a in attempts
            ]
        )
    
    def evaluate_all(self, problems: List[Dict], 
                    max_attempts: int = config.MAX_ATTEMPTS,
                    verbose: bool = True) -> List[ProblemResult]:
        """Evaluate all problems."""
        results = []
        total = len(problems)
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"EVALUATION STARTED")
            print(f"{'='*60}")
            print(f"Problems: {total}")
            print(f"Max attempts per problem: {max_attempts}")
            print(f"Compiler: {self.compiler_version}")
            print(f"{'='*60}\n")
        
        for i, problem in enumerate(problems, 1):
            p = problem.get('problem', problem)
            title = p.get('title', 'Untitled')
            
            if verbose:
                print(f"[{i}/{total}] {title}...", end=" ", flush=True)
            
            result = self.evaluate_problem(problem, max_attempts)
            results.append(result)
            
            if verbose:
                status = "[PASS]" if result.solved else "[FAIL]"
                print(f"{status} ({result.tests_passed}/{result.tests_total} tests)")
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"EVALUATION COMPLETE")
            print(f"{'='*60}\n")
        
        return results
