"""
LeetCode-Style C++ Compiler Interface
Web app for compiling and running C++ code against test cases.
"""

from flask import Flask, render_template, request, jsonify, session
import json
import subprocess
import tempfile
import os
import uuid
from pathlib import Path
import time

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

TEMP_DIR = Path(tempfile.gettempdir()) / "cp_compiler"
TEMP_DIR.mkdir(exist_ok=True)

COMPILER = "g++"
COMPILE_FLAGS = ["-std=c++17", "-O2", "-pipe"]

LANGUAGE_CONFIG = {
    "cpp": {
        "compiler": "g++",
        "extension": ".cpp",
        "flags": ["-std=c++17", "-O2", "-pipe"]
    },
    "python": {
        "compiler": "python",
        "extension": ".py",
        "flags": []
    }
}


class CompileResult:
    def __init__(self, success: bool, output: str = "", error: str = "", time: float = 0.0):
        self.success = success
        self.output = output
        self.error = error
        self.time = time


class RunResult:
    def __init__(self, success: bool, output: str = "", error: str = "", 
                 passed: int = 0, total: int = 0, time: float = 0.0):
        self.success = success
        self.output = output
        self.error = error
        self.passed = passed
        self.total = total
        self.time = time


def compile_code(code: str, language: str = "cpp") -> CompileResult:
    """Compile code and return result."""
    start = time.time()
    
    config = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG["cpp"])
    
    fd, src_path = tempfile.mkstemp(suffix=config["extension"])
    try:
        os.write(fd, code.encode('utf-8'))
        os.close(fd)
        
        fd, out_path = tempfile.mkstemp(suffix='.exe')
        os.close(fd)
        
        cmd = [config["compiler"]] + config["flags"] + [
            "-o", out_path, src_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        elapsed = time.time() - start
        
        if result.returncode == 0:
            return CompileResult(True, out_path, "", elapsed)
        else:
            return CompileResult(False, "", result.stderr, elapsed)
            
    except subprocess.TimeoutExpired:
        return CompileResult(False, "", "Compilation timed out", time.time() - start)
    except Exception as e:
        return CompileResult(False, "", str(e), time.time() - start)
    finally:
        if os.path.exists(src_path):
            try:
                os.remove(src_path)
            except:
                pass


def run_code(binary_path: str, input_data: str, timeout: int = 5) -> RunResult:
    """Run compiled binary with input and return result."""
    start = time.time()
    
    try:
        result = subprocess.run(
            [binary_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        elapsed = time.time() - start
        
        if result.returncode != 0:
            return RunResult(False, "", f"Runtime error: {result.stderr}", 0, 1, elapsed)
        
        return RunResult(True, result.stdout.strip(), "", 1, 1, elapsed)
        
    except subprocess.TimeoutExpired:
        return RunResult(False, "", "Time limit exceeded", 0, 1, time.time() - start)
    except Exception as e:
        return RunResult(False, "", str(e), 0, 1, time.time() - start)


def normalize_output(output: str) -> str:
    """Normalize output for comparison."""
    lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
    return '\n'.join(lines)


def run_all_tests(code: str, test_cases: list, language: str = "cpp") -> dict:
    """Run code against all test cases."""
    results = []
    passed = 0
    
    compile_result = compile_code(code, language)
    
    if not compile_result.success:
        return {
            "compiled": False,
            "compile_error": compile_result.error,
            "compile_time": compile_result.time,
            "results": [],
            "passed": 0,
            "total": len(test_cases)
        }
    
    binary_path = compile_result.output
    total_time = compile_result.time
    
    for i, test in enumerate(test_cases):
        input_data = test.get("input", "")
        expected = normalize_output(test.get("expected", ""))
        
        run_result = run_code(binary_path, input_data)
        total_time += run_result.time
        
        actual = normalize_output(run_result.output)
        test_passed = actual == expected
        
        if test_passed:
            passed += 1
        
        results.append({
            "test_id": i + 1,
            "input": input_data,
            "expected": expected,
            "actual": actual,
            "passed": test_passed,
            "time": run_result.time,
            "error": run_result.error if not test_passed else None
        })
    
    if os.path.exists(binary_path):
        try:
            os.remove(binary_path)
        except:
            pass
    
    return {
        "compiled": True,
        "compile_time": compile_result.time,
        "results": results,
        "passed": passed,
        "total": len(test_cases),
        "total_time": total_time
    }


@app.route('/')
def index():
    """Main page with code editor."""
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile():
    """Compile code and return result."""
    data = request.json
    
    code = data.get('code', '')
    language = data.get('language', 'cpp')
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    result = compile_code(code, language)
    
    if result.success:
        return jsonify({
            "success": True,
            "message": "Compilation successful",
            "time": f"{result.time:.3f}s"
        })
    else:
        return jsonify({
            "success": False,
            "error": result.error,
            "time": f"{result.time:.3f}s"
        })


@app.route('/run', methods=['POST'])
def run():
    """Run code against test cases."""
    data = request.json
    
    code = data.get('code', '')
    test_cases = data.get('test_cases', [])
    language = data.get('language', 'cpp')
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    if not test_cases:
        return jsonify({"success": False, "error": "No test cases provided"})
    
    result = run_all_tests(code, test_cases, language)
    
    return jsonify({
        "success": True,
        "compiled": result["compiled"],
        "compile_error": result.get("compile_error"),
        "passed": result["passed"],
        "total": result["total"],
        "results": result["results"],
        "time": f"{result['total_time']:.3f}s"
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        result = subprocess.run(["g++", "--version"], capture_output=True, timeout=5)
        compiler_available = result.returncode == 0
        compiler_version = result.stdout.split('\n')[0] if compiler_available else "Not found"
    except:
        compiler_available = False
        compiler_version = "Not found"
    
    return jsonify({
        "status": "healthy",
        "compiler": {
            "available": compiler_available,
            "version": compiler_version
        }
    })


if __name__ == '__main__':
    print("=" * 50)
    print("CP COMPILER - LeetCode Style")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
