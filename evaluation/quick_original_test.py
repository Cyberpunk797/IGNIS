"""
Quick comparison script - tests original Qwen on 10 problems
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from client import create_client
from extract import extract_cpp_code, clean_code
from compiler import compile_code
from runner import run_tests, cleanup_binary
from prompts import build_prompt, SYSTEM_PROMPT
import config


def quick_test(num_problems=10):
    client = create_client()
    
    with open(config.DATASET_PATH, 'r', encoding='utf-8') as f:
        problems = [json.loads(line) for line in f][:num_problems]
    
    print("Testing Original Qwen Model: qwen2.5-coder-7b-instruct")
    print("=" * 60)
    
    results = []
    
    for i, p in enumerate(problems, 1):
        prob = p.get('problem', p)
        title = prob.get('title', 'Untitled')
        
        samples = prob.get('samples', [])
        test_cases = [{'input': s.get('input', ''), 'expected': s.get('output', '')} for s in samples]
        
        prompt = build_prompt(p)
        
        print(f"\n[{i}] {title}...", end=' ', flush=True)
        
        start = time.time()
        try:
            response = client.generate(prompt, SYSTEM_PROMPT, max_tokens=1500)
        except Exception as e:
            print(f"ERROR: {str(e)[:80]}")
            continue
        
        latency = time.time() - start
        
        code, _ = extract_cpp_code(response)
        code = clean_code(code) if code else None
        
        if not code:
            print(f"NO CODE ({latency:.1f}s)")
            continue
        
        success, err, binary = compile_code(code)
        if not success:
            print(f"COMPILE ERROR ({latency:.1f}s)")
            continue
        
        passed, total, _ = run_tests(binary, test_cases)
        cleanup_binary(binary)
        
        status = "PASS" if passed == total else "FAIL"
        print(f"{status} ({passed}/{total} tests, {latency:.1f}s)")
        
        results.append({'title': title, 'passed': passed, 'total': total, 'latency': latency})
    
    print("\n" + "=" * 60)
    print("ORIGINAL QWEN RESULTS:")
    if results:
        passed = sum(1 for r in results if r['passed'] == r['total'])
        print(f"Pass Rate: {passed}/{len(results)} ({passed/len(results)*100:.0f}%)")
        print(f"Avg Latency: {sum(r['latency'] for r in results)/len(results):.1f}s")
    
    return results


if __name__ == "__main__":
    quick_test(10)
