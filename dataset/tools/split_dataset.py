import argparse
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl, write_jsonl  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Split unified dataset by problem_id.")
    parser.add_argument("input_path", help="Merged JSONL input")
    parser.add_argument("train_output", help="Train JSONL output")
    parser.add_argument("valid_output", help="Validation JSONL output")
    parser.add_argument("--valid-ratio", type=float, default=0.1, help="Validation ratio by problem group")
    parser.add_argument("--seed", type=int, default=17, help="Random seed")
    args = parser.parse_args()

    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in read_jsonl(args.input_path):
        grouped[entry["problem"]["problem_id"]].append(entry)

    problem_ids = sorted(grouped)
    rng = random.Random(args.seed)
    rng.shuffle(problem_ids)

    valid_count = max(1, int(round(len(problem_ids) * args.valid_ratio)))
    valid_ids = set(problem_ids[:valid_count])

    train_rows = []
    valid_rows = []
    for problem_id, rows in grouped.items():
        if problem_id in valid_ids:
            valid_rows.extend(rows)
        else:
            train_rows.extend(rows)

    train_rows.sort(key=lambda row: row["id"])
    valid_rows.sort(key=lambda row: row["id"])

    write_jsonl(args.train_output, train_rows)
    write_jsonl(args.valid_output, valid_rows)

    print(f"Train entries: {len(train_rows)}")
    print(f"Validation entries: {len(valid_rows)}")
    print(f"Validation problem groups: {len(valid_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
