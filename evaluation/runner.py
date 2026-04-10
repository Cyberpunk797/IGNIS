"""
Run compiled C++ binary against test cases.
Handles execution, input/output comparison, and timeouts.
"""

import subprocess
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import config


class TestResult:
    def __init__(self, test_id: int, passed: bool, 
                 expected: str, actual: str,
                 error: Optional[str] = None,
                 timeout: bool = False,
                 execution_time: float = 0.0):
        self.test_id = test_id
        self.passed = passed
        self.expected = expected
        self.actual = actual
        self.error = error
        self.timeout = timeout
        self.execution_time = execution_time
    
    def to_dict(self) -> dict:
        return {
            "test_id": self.test_id,
            "passed": self.passed,
            "expected": self.expected,
            "actual": self.actual,
            "error": self.error,
            "timeout": self.timeout,
            "execution_time": self.execution_time
        }


def normalize_output(output: str) -> str:
    """Normalize output for comparison."""
    lines = output.strip().split('\n')
    normalized = []
    for line in lines:
        line = line.strip()
        if line:
            normalized.append(line)
    return '\n'.join(normalized)


def run_single_test(binary_path: Path, input_data: str, 
                    timeout: int = 5) -> Tuple[str, str, bool, float, Optional[str]]:
    """
    Run a single test case.
    
    Returns:
        Tuple of (output, error, timeout, exec_time, error_msg)
    """
    import time
    
    try:
        start_time = time.time()
        
        result = subprocess.run(
            [str(binary_path)],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode != 0:
            return "", f"Runtime error: {result.stderr}", True, execution_time, result.stderr
        
        return result.stdout, "", False, execution_time, None
        
    except subprocess.TimeoutExpired:
        return "", "", True, timeout, "Execution timed out"
    except Exception as e:
        return "", "", True, 0, str(e)


def run_tests(binary_path: Path, test_cases: List[Dict],
              timeout: int = 5) -> Tuple[int, int, List[TestResult]]:
    """
    Run all test cases against compiled binary.
    
    Args:
        binary_path: Path to compiled executable
        test_cases: List of dicts with 'input' and 'expected' keys
        
    Returns:
        Tuple of (passed_count, total_count, list_of_results)
    """
    results = []
    passed = 0
    
    for i, test in enumerate(test_cases):
        input_data = test.get('input', '')
        expected = normalize_output(test.get('expected', ''))
        
        actual, error, timed_out, exec_time, error_msg = run_single_test(
            binary_path, input_data, timeout
        )
        
        actual_normalized = normalize_output(actual)
        test_passed = actual_normalized == expected and not timed_out
        
        if test_passed:
            passed += 1
        
        result = TestResult(
            test_id=i + 1,
            passed=test_passed,
            expected=expected,
            actual=actual_normalized,
            error=error_msg or error,
            timeout=timed_out
        )
        results.append(result)
    
    return passed, len(test_cases), results


def cleanup_binary(binary_path: Path):
    """Remove compiled binary."""
    try:
        if os.path.exists(binary_path):
            os.remove(binary_path)
    except:
        pass
