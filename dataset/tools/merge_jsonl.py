import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl, write_jsonl  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge multiple JSONL files into one.")
    parser.add_argument("output_path", help="Output JSONL path")
    parser.add_argument("input_paths", nargs="+", help="Input JSONL paths")
    args = parser.parse_args()

    merged = []
    seen_ids: set[str] = set()
    for input_path in args.input_paths:
        for row in read_jsonl(input_path):
            row_id = row["id"]
            if row_id in seen_ids:
                raise ValueError(f"Duplicate id across inputs: {row_id}")
            seen_ids.add(row_id)
            merged.append(row)

    write_jsonl(args.output_path, merged)
    print(f"Wrote {len(merged)} entries to {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
