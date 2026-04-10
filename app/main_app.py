"""
IGNIS - Self-Verifying Competitive Programming AI
Main application with AI-powered problem solving and self-verification.
"""

import sys
from pathlib import Path

# Add evaluation module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'evaluation'))

from flask import Flask, render_template, request, jsonify, session
import json
import subprocess
import tempfile
import os
import uuid
import time
import urllib.request
import urllib.error

# Import from evaluation module
from client import create_client
from extract import extract_cpp_code, clean_code
from compiler import compile_code, check_compiler
from runner import run_tests, cleanup_binary
from prompts import build_prompt, build_verification_prompt, SYSTEM_PROMPT
import config

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

TEMP_DIR = Path(tempfile.gettempdir()) / "cp_ai"
TEMP_DIR.mkdir(exist_ok=True)

JUDGE_URL = os.getenv("IGNIS_JUDGE_URL") or os.getenv("JUDGE_URL")
JUDGE_API_KEY = os.getenv("IGNIS_JUDGE_API_KEY") or os.getenv("JUDGE_API_KEY")


def normalize_output(output: str) -> str:
    lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
    return '\n'.join(lines)


def _judge_post(path: str, payload: dict, timeout: float = 10.0) -> dict:
    if not JUDGE_URL:
        raise RuntimeError("Judge URL not configured")

    base = JUDGE_URL.rstrip("/")
    url = f"{base}{path}"
    data = json.dumps(payload).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if JUDGE_API_KEY:
        headers["X-Api-Key"] = JUDGE_API_KEY

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body) if body else {}


def _judge_get(path: str, timeout: float = 5.0) -> dict:
    if not JUDGE_URL:
        raise RuntimeError("Judge URL not configured")

    base = JUDGE_URL.rstrip("/")
    url = f"{base}{path}"

    headers = {}
    if JUDGE_API_KEY:
        headers["X-Api-Key"] = JUDGE_API_KEY

    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body) if body else {}


def solve_with_ai(problem: dict, max_attempts: int = 3) -> dict:
    """Solve problem using AI with self-verification."""
    p = problem.get('problem', problem)
    
    prompt = build_prompt(problem)
    client = create_client()
    
    code = None
    reasoning = ""
    
    for attempt in range(1, max_attempts + 1):
        print(f"  AI Attempt {attempt}/{max_attempts}")
        
        if attempt == 1:
            response = client.generate(prompt, SYSTEM_PROMPT, max_tokens=2000)
        else:
            if code:
                verification_prompt = build_verification_prompt(p, code)
                response = client.generate(verification_prompt, SYSTEM_PROMPT, max_tokens=2500)
            else:
                response = client.generate(prompt, SYSTEM_PROMPT, max_tokens=2000)
        
        code, reasoning = extract_cpp_code(response)
        code = clean_code(code) if code else None
        
        if not code:
            continue
        
        success, error, binary_path = compile_code(code)
        
        if not success:
            continue
        
        samples = p.get('samples', [])
        test_cases = [
            {'input': s.get('input', ''), 'expected': s.get('output', '')}
            for s in samples
        ]
        
        passed, total, _ = run_tests(binary_path, test_cases)
        cleanup_binary(binary_path)
        
        if passed == total:
            return {
                "success": True,
                "code": code,
                "reasoning": reasoning,
                "attempts": attempt,
                "tests_passed": passed,
                "tests_total": total
            }
    
    return {
        "success": False,
        "code": code,
        "reasoning": reasoning,
        "attempts": max_attempts,
        "tests_passed": 0,
        "tests_total": len(p.get('samples', []))
    }


def chat_with_ai(problem: dict, messages: list[dict]) -> dict:
    """Continue a chat-style conversation with the AI solver."""
    p = problem.get('problem', problem)
    client = create_client()

    system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "You are in interactive solver chat mode.\n"
        "Answer the user's latest question about the current competitive programming problem.\n"
        "Be concise but useful.\n"
        "If you provide code, wrap it in a ```cpp block.\n"
    )

    context_lines = [
        f"Problem: {p.get('title', 'Untitled')}",
        "",
        p.get('statement', ''),
        "",
        f"Input: {p.get('input_spec', 'Not specified')}",
        f"Output: {p.get('output_spec', 'Not specified')}",
        f"Constraints: {p.get('constraints', 'Not specified')}",
    ]

    samples = p.get('samples', [])
    if samples:
        context_lines.append("")
        context_lines.append("Samples:")
        for sample in samples[:3]:
            context_lines.append(f"Input: {sample.get('input', '').strip()}")
            context_lines.append(f"Output: {sample.get('output', '').strip()}")

    conversation_lines = ["", "Conversation so far:"]
    for message in messages[-12:]:
        role = message.get("role", "user")
        content = message.get("content", "").strip()
        if content:
            conversation_lines.append(f"{role.upper()}: {content}")

    prompt = "\n".join(context_lines + conversation_lines + ["", "Respond to the latest USER message."])

    response = client.generate(prompt, system_prompt, max_tokens=1800)
    code, _ = extract_cpp_code(response)
    code = clean_code(code) if code else None

    return {
        "reply": response,
        "code": code,
    }


def compile_and_run(code: str, test_cases: list) -> dict:
    """Compile code and run against test cases."""
    if JUDGE_URL:
        try:
            judge_result = _judge_post(
                "/run",
                {
                    "language": "cpp",
                    "code": code,
                    "test_cases": [
                        {"input": t.get("input", ""), "expected": t.get("expected", "")}
                        for t in test_cases
                    ],
                    "timeout_s": 5.0,
                    "compile_timeout_s": 30.0,
                },
                timeout=40.0,
            )
            return judge_result
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                error_body = ""
            return {
                "success": False,
                "compiled": False,
                "error": f"Judge error: HTTP {e.code} {error_body}".strip(),
                "results": [],
                "passed": 0,
                "total": len(test_cases),
            }
        except Exception as e:
            return {
                "success": False,
                "compiled": False,
                "error": f"Judge error: {e}",
                "results": [],
                "passed": 0,
                "total": len(test_cases),
            }

    result = compile_code(code)
    
    if not result[0]:
        return {
            "compiled": False,
            "error": result[1],
            "results": [],
            "passed": 0,
            "total": len(test_cases)
        }
    
    binary_path = result[2]
    results = []
    passed = 0
    
    for i, test in enumerate(test_cases):
        input_data = test.get('input', '')
        expected = normalize_output(test.get('expected', ''))
        
        try:
            proc_result = subprocess.run(
                [str(binary_path)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            actual = normalize_output(proc_result.stdout)
            runtime_ok = proc_result.returncode == 0
            test_passed = runtime_ok and actual == expected
            
            if test_passed:
                passed += 1
            
            test_result = {
                "test_id": i + 1,
                "input": input_data,
                "expected": expected,
                "actual": actual,
                "passed": test_passed
            }

            if not runtime_ok:
                stderr = proc_result.stderr.strip()
                test_result["error"] = stderr or f"Runtime error (exit code {proc_result.returncode})"

            results.append(test_result)
        except subprocess.TimeoutExpired:
            results.append({
                "test_id": i + 1,
                "input": input_data,
                "expected": expected,
                "actual": "",
                "passed": False,
                "error": "Time limit exceeded"
            })
        except Exception as e:
            results.append({
                "test_id": i + 1,
                "input": input_data,
                "expected": expected,
                "actual": "",
                "passed": False,
                "error": str(e)
            })
    
    try:
        os.remove(binary_path)
    except:
        pass
    
    return {
        "compiled": True,
        "results": results,
        "passed": passed,
        "total": len(test_cases)
    }


def load_problems_from_dataset():
    """Load problems from the dataset."""
    problems = []
    dataset_path = Path(__file__).parent.parent / "dataset" / "build" / "train_full.jsonl"
    
    if dataset_path.exists():
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    p = data.get('problem', {})
                    
                    difficulty = "Easy"
                    rating = p.get('difficulty_rating', 1200)
                    if rating >= 1600:
                        difficulty = "Hard"
                    elif rating >= 1300:
                        difficulty = "Medium"
                    
                    tags = p.get('tags', [])
                    if isinstance(tags, str):
                        tags = [tags]
                    
                    samples = p.get('samples', [])
                    examples = []
                    for s in samples[:3]:
                        examples.append({
                            'input': s.get('input', '').strip(),
                            'output': s.get('output', '').strip()
                        })
                    
                    problem = {
                        "id": p.get('problem_id', data.get('id', 'unknown')),
                        "title": p.get('title', 'Untitled'),
                        "difficulty": difficulty,
                        "tags": tags,
                        "statement": p.get('statement', ''),
                        "input_format": p.get('input_spec', ''),
                        "output_format": p.get('output_spec', ''),
                        "constraints": p.get('constraints', ''),
                        "examples": examples,
                        "task_type": data.get('task_type', 'SFT_SOLVE'),
                        "rating": rating
                    }
                    problems.append(problem)
                except json.JSONDecodeError:
                    continue
    
    return problems


PROBLEMS = load_problems_from_dataset()


@app.route('/')
def index():
    """Main page."""
    return render_template('main.html', problems=PROBLEMS)


@app.route('/api/problems')
def get_problems():
    """Get list of problems."""
    return jsonify(PROBLEMS)


@app.route('/api/compile', methods=['POST'])
def api_compile():
    """Compile user code."""
    data = request.json
    code = data.get('code', '')
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})

    if JUDGE_URL:
        try:
            judge_result = _judge_post(
                "/compile",
                {
                    "language": "cpp",
                    "code": code,
                    "compile_timeout_s": 30.0,
                },
                timeout=35.0,
            )
            if judge_result.get("compiled"):
                return jsonify({"success": True, "message": "Compiled successfully!"})
            return jsonify({"success": False, "error": judge_result.get("error", "Compilation failed")})
        except Exception as e:
            return jsonify({"success": False, "error": f"Judge error: {e}"})

    result = compile_code(code)

    if result[0]:
        try:
            os.remove(result[2])
        except:
            pass
        return jsonify({"success": True, "message": "Compiled successfully!"})
    else:
        return jsonify({"success": False, "error": result[1]})


@app.route('/api/run', methods=['POST'])
def api_run():
    """Run user code against test cases."""
    data = request.json
    code = data.get('code', '')
    test_cases = data.get('test_cases', [])
    
    code = code.strip()
    
    if not code:
        return jsonify({
            "success": False, 
            "error": "No code provided. Please write your C++ solution.",
            "compiled": False,
            "results": [],
            "passed": 0,
            "total": len(test_cases) if test_cases else 0
        })
    
    if not test_cases:
        return jsonify({"success": False, "error": "No test cases"})
    
    result = compile_and_run(code, test_cases)
    return jsonify(result)


@app.route('/api/ask-ai', methods=['POST'])
def api_ask_ai():
    """Get AI solution with self-verification."""
    data = request.json
    problem = data.get('problem', {})
    
    print(f"Asking AI for: {problem.get('title', 'Unknown')}")
    
    result = solve_with_ai(problem)
    
    return jsonify(result)


@app.route('/api/chat-ai', methods=['POST'])
def api_chat_ai():
    """Chat with AI about the selected problem."""
    data = request.json or {}
    problem = data.get('problem', {})
    messages = data.get('messages', [])

    if not problem:
        return jsonify({"success": False, "error": "No problem provided"})

    if not messages:
        return jsonify({"success": False, "error": "No messages provided"})

    try:
        result = chat_with_ai(problem, messages)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/health')
def api_health():
    """Check system health."""
    compiler_ok, compiler_version = check_compiler()
    
    try:
        client = create_client()
        ai_status = client.is_connected()
        ai_model = client.get_model_name()
    except:
        ai_status = False
        ai_model = None

    judge_status = None
    if JUDGE_URL:
        try:
            judge_health = _judge_get("/health", timeout=3.0)
            judge_status = {
                "configured": True,
                "reachable": True,
                "docker_available": bool(judge_health.get("docker_available")),
            }
        except Exception:
            judge_status = {"configured": True, "reachable": False}
    
    return jsonify({
        "compiler": {
            "available": compiler_ok,
            "version": compiler_version if compiler_ok else None
        },
        "ai": {
            "connected": ai_status,
            "model": ai_model
        },
        "judge": judge_status,
    })


if __name__ == '__main__':
    print("=" * 60)
    print("AxLu-ZeSi CP - AI Coding Assistant")
    print("=" * 60)
    print("Starting server at http://localhost:5000")
    print("Open browser to start coding!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
