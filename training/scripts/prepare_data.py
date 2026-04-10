import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl, write_jsonl  # noqa: E402


def render_problem(problem: dict) -> str:
    sample_text = "\n".join(
        [
            f"Sample {index + 1} Input:\n{sample['input']}\nSample {index + 1} Output:\n{sample['output']}"
            for index, sample in enumerate(problem["samples"])
        ]
    )
    return (
        f"Title: {problem['title']}\n"
        f"Statement:\n{problem['statement']}\n\n"
        f"Input:\n{problem['input_spec']}\n\n"
        f"Output:\n{problem['output_spec']}\n\n"
        f"Constraints:\n{problem['constraints']}\n\n"
        f"{sample_text}\n"
    )


def render_instruction(entry: dict) -> str:
    prefix = (
        "You are solving a competitive programming task in C++17. "
        "Reason explicitly about algorithm choice, correctness, edge cases, and complexity."
    )
    return f"{prefix}\n\nTask Type: {entry['task_type']}\n\n{render_problem(entry['problem'])}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert unified JSONL into instruction/completion JSONL.")
    parser.add_argument("input_path", help="Unified JSONL input")
    parser.add_argument("output_path", help="Prepared JSONL output")
    args = parser.parse_args()

    rows = []
    for entry in read_jsonl(args.input_path):
        rows.append({
            "id": entry["id"],
            "task_type": entry["task_type"],
            "instruction": render_instruction(entry),
            "completion": json.dumps(entry["response"], ensure_ascii=False),
        })

    write_jsonl(args.output_path, rows)
    print(f"Wrote {len(rows)} prepared rows to {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
