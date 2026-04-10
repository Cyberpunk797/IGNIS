import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl  # noqa: E402


def score_entry(entry: dict) -> tuple[float, list[str]]:
    notes: list[str] = []
    score = 0.40
    response = entry["response"]
    problem = entry["problem"]

    if len(problem.get("tags", [])) >= 2:
        score += 0.05
    else:
        notes.append("problem has fewer than 2 tags")

    if problem.get("samples"):
        score += 0.05
    else:
        notes.append("missing samples")

    task_type = entry["task_type"]
    if task_type in {"SFT_SOLVE", "PLAN_ONLY"}:
        if response.get("invariant_or_correctness"):
            score += 0.10
        else:
            notes.append("missing invariant_or_correctness")
        if response.get("edge_cases"):
            score += 0.05
        else:
            notes.append("missing edge_cases")
        complexity = response.get("complexity", {})
        if complexity.get("time") and complexity.get("memory"):
            score += 0.10
        else:
            notes.append("missing complexity details")

    if task_type == "SFT_SOLVE":
        if len(response.get("algorithm_steps", [])) >= 3:
            score += 0.05
        else:
            notes.append("short algorithm_steps")
        code = response.get("final_code", "")
        if "ios::sync_with_stdio(false);" in code and "cin.tie(nullptr);" in code:
            score += 0.10
        else:
            notes.append("missing fast I/O in final_code")
        if len(response.get("explanation", "")) >= 120:
            score += 0.05
        else:
            notes.append("short explanation")

    if task_type == "REPAIR":
        if response.get("diagnosis") and len(response["diagnosis"]) >= 2:
            score += 0.10
        else:
            notes.append("thin diagnosis")
        if response.get("bug_type"):
            score += 0.05
        else:
            notes.append("missing bug_type")

    if task_type == "OPTIMIZE":
        slow = response.get("slow_code", {})
        if slow.get("complexity"):
            score += 0.05
        else:
            notes.append("missing slow complexity")
        if response.get("why_too_slow") and response.get("optimization_idea"):
            score += 0.10
        else:
            notes.append("weak optimization diagnosis")

    return min(score, 1.0), notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute heuristic quality scores.")
    parser.add_argument("input_path", help="JSONL input file")
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()

    report = []
    for entry in read_jsonl(args.input_path):
        score, notes = score_entry(entry)
        report.append({
            "id": entry["id"],
            "task_type": entry["task_type"],
            "declared_quality_score": entry["quality_score"],
            "heuristic_quality_score": round(score, 4),
            "notes": notes,
        })

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
