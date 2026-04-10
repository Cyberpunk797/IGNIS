from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Ignis Judge", version="0.1.0")


def _normalize_output(output: str) -> str:
    lines = [line.strip() for line in (output or "").strip().split("\n") if line.strip()]
    return "\n".join(lines)


def _require_api_key(x_api_key: Optional[str]) -> None:
    required = os.getenv("JUDGE_API_KEY")
    if not required:
        return
    if not x_api_key or x_api_key != required:
        raise HTTPException(status_code=401, detail="Unauthorized")


class TestCase(BaseModel):
    input: str = ""
    expected: str = ""


class RunRequest(BaseModel):
    language: str = Field(default="cpp", description="Only 'cpp' is supported right now.")
    code: str
    test_cases: list[TestCase] = Field(default_factory=list)
    timeout_s: float = 5.0
    compile_timeout_s: float = 30.0
    cpus: float = 1.0
    memory_mb: int = 512


class CompileRequest(BaseModel):
    language: str = "cpp"
    code: str
    compile_timeout_s: float = 30.0
    cpus: float = 1.0
    memory_mb: int = 512


@dataclass
class DockerResult:
    returncode: int
    stdout: str
    stderr: str


def _docker_available() -> bool:
    try:
        p = subprocess.run(
            ["docker", "version"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return p.returncode == 0
    except Exception:
        return False


def _run_docker(
    args: list[str],
    *,
    stdin: Optional[str] = None,
    timeout_s: float = 10.0,
) -> DockerResult:
    p = subprocess.run(
        ["docker"] + args,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    return DockerResult(p.returncode, p.stdout or "", p.stderr or "")


def _docker_sandbox_args(
    *,
    mount_dir: str,
    cpus: float,
    memory_mb: int,
) -> list[str]:
    # Note: Docker security flags vary by host. On Linux, these help a lot; on Windows/Mac some are no-ops.
    return [
        "run",
        "--rm",
        "--network",
        "none",
        "--cpus",
        str(max(cpus, 0.1)),
        "--memory",
        f"{max(memory_mb, 64)}m",
        "--pids-limit",
        "256",
        "--security-opt",
        "no-new-privileges",
        "--cap-drop",
        "ALL",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,nosuid,nodev,size=64m",
        "--mount",
        f"type=bind,src={mount_dir},dst=/work,rw",
        "--workdir",
        "/work",
    ]


def _compile_cpp_in_docker(
    *,
    mount_dir: str,
    compile_timeout_s: float,
    cpus: float,
    memory_mb: int,
    image: str,
) -> DockerResult:
    compile_cmd = "g++ -std=c++17 -O2 -pipe main.cpp -o main"
    return _run_docker(
        _docker_sandbox_args(mount_dir=mount_dir, cpus=cpus, memory_mb=memory_mb)
        + [
            image,
            "bash",
            "-lc",
            compile_cmd,
        ],
        timeout_s=compile_timeout_s,
    )


def _run_binary_in_docker(
    *,
    mount_dir: str,
    stdin: str,
    timeout_s: float,
    cpus: float,
    memory_mb: int,
    image: str,
) -> DockerResult:
    # Run compiled binary. `timeout` utility isn't guaranteed inside every image; enforce from host via subprocess timeout.
    return _run_docker(
        _docker_sandbox_args(mount_dir=mount_dir, cpus=cpus, memory_mb=memory_mb)
        + [
            image,
            "bash",
            "-lc",
            "./main",
        ],
        stdin=stdin,
        timeout_s=timeout_s,
    )


def _safe_mkdir_perms(path: str) -> None:
    try:
        os.chmod(path, 0o777)
    except Exception:
        pass


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "docker_available": _docker_available(),
        "language": ["cpp"],
        "sandbox": "docker",
    }


@app.post("/compile")
def compile_only(req: CompileRequest, x_api_key: Optional[str] = Header(default=None)) -> dict[str, Any]:
    _require_api_key(x_api_key)
    if req.language != "cpp":
        raise HTTPException(status_code=400, detail="Only language='cpp' is supported.")
    if not _docker_available():
        raise HTTPException(status_code=503, detail="Docker is not available on judge host.")

    image = os.getenv("JUDGE_DOCKER_IMAGE", "gcc:13")

    with tempfile.TemporaryDirectory(prefix="ignis_judge_") as tmp:
        _safe_mkdir_perms(tmp)
        src_path = os.path.join(tmp, "main.cpp")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(req.code)

        comp = _compile_cpp_in_docker(
            mount_dir=tmp,
            compile_timeout_s=req.compile_timeout_s,
            cpus=req.cpus,
            memory_mb=req.memory_mb,
            image=image,
        )

        if comp.returncode != 0:
            return {"compiled": False, "error": (comp.stderr or comp.stdout).strip()[:8000]}
        return {"compiled": True}


@app.post("/run")
def run(req: RunRequest, x_api_key: Optional[str] = Header(default=None)) -> dict[str, Any]:
    _require_api_key(x_api_key)
    if req.language != "cpp":
        raise HTTPException(status_code=400, detail="Only language='cpp' is supported.")
    if not _docker_available():
        raise HTTPException(status_code=503, detail="Docker is not available on judge host.")

    image = os.getenv("JUDGE_DOCKER_IMAGE", "gcc:13")
    timeout_s = max(0.1, float(req.timeout_s))
    compile_timeout_s = max(0.5, float(req.compile_timeout_s))

    with tempfile.TemporaryDirectory(prefix="ignis_judge_") as tmp:
        _safe_mkdir_perms(tmp)
        src_path = os.path.join(tmp, "main.cpp")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(req.code)

        comp = _compile_cpp_in_docker(
            mount_dir=tmp,
            compile_timeout_s=compile_timeout_s,
            cpus=req.cpus,
            memory_mb=req.memory_mb,
            image=image,
        )

        if comp.returncode != 0:
            return {
                "success": False,
                "compiled": False,
                "error": (comp.stderr or comp.stdout).strip()[:8000],
                "results": [],
                "passed": 0,
                "total": len(req.test_cases),
            }

        passed = 0
        results: list[dict[str, Any]] = []

        for idx, test in enumerate(req.test_cases):
            expected = _normalize_output(test.expected)
            try:
                run_res = _run_binary_in_docker(
                    mount_dir=tmp,
                    stdin=test.input or "",
                    timeout_s=timeout_s,
                    cpus=req.cpus,
                    memory_mb=req.memory_mb,
                    image=image,
                )
                actual = _normalize_output(run_res.stdout)
                runtime_ok = run_res.returncode == 0
                test_passed = runtime_ok and actual == expected
                if test_passed:
                    passed += 1

                result: dict[str, Any] = {
                    "test_id": idx + 1,
                    "input": test.input or "",
                    "expected": expected,
                    "actual": actual,
                    "passed": test_passed,
                }
                if not runtime_ok:
                    err = (run_res.stderr or "").strip()
                    result["error"] = err or f"Runtime error (exit code {run_res.returncode})"
                results.append(result)
            except subprocess.TimeoutExpired:
                results.append(
                    {
                        "test_id": idx + 1,
                        "input": test.input or "",
                        "expected": expected,
                        "actual": "",
                        "passed": False,
                        "error": "Time limit exceeded",
                    }
                )

        return {
            "success": True,
            "compiled": True,
            "results": results,
            "passed": passed,
            "total": len(req.test_cases),
        }

