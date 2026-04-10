import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl  # noqa: E402
from libs.taxonomy import BUCKETS, QUALITY_TIERS, TASK_TYPES  # noqa: E402


COMMON_PROBLEM_FIELDS = {
    "problem_id",
    "title",
    "statement",
    "input_spec",
    "output_spec",
    "constraints",
    "samples",
    "tags",
    "difficulty_rating",
    "bucket",
}


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _validate_problem(problem: dict, errors: list[str]) -> None:
    missing = sorted(COMMON_PROBLEM_FIELDS - set(problem))
    if missing:
        errors.append(f"problem missing fields: {missing}")
        return
    _require(problem["bucket"] in BUCKETS, f"invalid bucket: {problem['bucket']}", errors)
    _require(isinstance(problem["difficulty_rating"], int), "difficulty_rating must be int", errors)
    _require(isinstance(problem["samples"], list) and len(problem["samples"]) >= 1, "samples must be non-empty", errors)
    _require(isinstance(problem["tags"], list) and len(problem["tags"]) >= 1, "tags must be non-empty", errors)


def _validate_common(entry: dict, errors: list[str]) -> None:
    required = {
        "id",
        "task_type",
        "language",
        "cpp_standard",
        "problem",
        "response",
        "quality_tier",
        "quality_score",
        "verification_reserved",
        "created_at",
    }
    missing = sorted(required - set(entry))
    if missing:
        errors.append(f"missing top-level fields: {missing}")
        return

    _require(entry["task_type"] in TASK_TYPES, f"invalid task_type: {entry['task_type']}", errors)
    _require(entry["language"] == "cpp", "language must be cpp", errors)
    _require(entry["cpp_standard"] == "c++17", "cpp_standard must be c++17", errors)
    _require(entry["quality_tier"] in QUALITY_TIERS, f"invalid quality_tier: {entry['quality_tier']}", errors)
    _require(isinstance(entry["quality_score"], (int, float)), "quality_score must be numeric", errors)
    _require(0.0 <= float(entry["quality_score"]) <= 1.0, "quality_score must be between 0 and 1", errors)
    _require(isinstance(entry["verification_reserved"], dict), "verification_reserved must be object", errors)
    _validate_problem(entry["problem"], errors)


def _validate_code_has_fast_io(code: str, field_name: str, errors: list[str]) -> None:
    _require("ios::sync_with_stdio(false);" in code, f"{field_name} missing ios::sync_with_stdio(false);", errors)
    _require("cin.tie(nullptr);" in code, f"{field_name} missing cin.tie(nullptr);", errors)


def _validate_by_task(entry: dict, errors: list[str]) -> None:
    response = entry.get("response", {})
    task_type = entry.get("task_type")
    if task_type == "SFT_SOLVE":
        required = {
            "core_idea",
            "algorithm_steps",
            "data_structures",
            "invariant_or_correctness",
            "edge_cases",
            "complexity",
            "explanation",
            "final_code",
        }
        missing = sorted(required - set(response))
        _require(not missing, f"SFT_SOLVE response missing: {missing}", errors)
        if "final_code" in response:
            _validate_code_has_fast_io(response["final_code"], "final_code", errors)
    elif task_type == "PLAN_ONLY":
        required = {
            "core_idea",
            "algorithm_steps",
            "data_structures",
            "invariant_or_correctness",
            "edge_cases",
            "complexity",
        }
        missing = sorted(required - set(response))
        _require(not missing, f"PLAN_ONLY response missing: {missing}", errors)
    elif task_type == "REPAIR":
        required = {
            "buggy_code",
            "bug_type",
            "failure_description",
            "diagnosis",
            "fix_explanation",
            "fixed_code",
        }
        missing = sorted(required - set(response))
        _require(not missing, f"REPAIR response missing: {missing}", errors)
        if "fixed_code" in response:
            _validate_code_has_fast_io(response["fixed_code"], "fixed_code", errors)
    elif task_type == "OPTIMIZE":
        required = {
            "slow_code",
            "why_too_slow",
            "optimization_idea",
            "new_complexity",
            "optimized_code",
        }
        missing = sorted(required - set(response))
        _require(not missing, f"OPTIMIZE response missing: {missing}", errors)
        if "optimized_code" in response:
            _validate_code_has_fast_io(response["optimized_code"], "optimized_code", errors)


def validate_file(path: Path) -> int:
    failures = 0
    seen_ids: set[str] = set()
    for line_number, entry in enumerate(read_jsonl(path), start=1):
        errors: list[str] = []
        _validate_common(entry, errors)
        _validate_by_task(entry, errors)
        entry_id = entry.get("id")
        if entry_id in seen_ids:
            errors.append(f"duplicate id in file: {entry_id}")
        seen_ids.add(entry_id)
        if errors:
            failures += 1
            print(f"{path}:{line_number}")
            for error in errors:
                print(f"  - {error}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate unified dataset JSONL files.")
    parser.add_argument("paths", nargs="+", help="JSONL files to validate")
    args = parser.parse_args()

    total_failures = 0
    for raw_path in args.paths:
        total_failures += validate_file(Path(raw_path))

    if total_failures:
        print(f"Validation finished with {total_failures} failing entries.")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
