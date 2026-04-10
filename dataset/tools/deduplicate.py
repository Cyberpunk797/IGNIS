import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.jsonl import read_jsonl, write_jsonl  # noqa: E402


SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    return SPACE_RE.sub(" ", text.strip().lower())


def signature(entry: dict) -> str:
    payload = {
        "problem_id": entry["problem"]["problem_id"],
        "title": normalize_text(entry["problem"]["title"]),
        "statement": normalize_text(entry["problem"]["statement"]),
        "task_type": entry["task_type"],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplicate JSONL entries by normalized problem signature.")
    parser.add_argument("input_path", help="Input JSONL path")
    parser.add_argument("output_path", help="Deduplicated output path")
    args = parser.parse_args()

    deduped = []
    seen: set[str] = set()
    removed = 0
    for entry in read_jsonl(args.input_path):
        sig = signature(entry)
        if sig in seen:
            removed += 1
            continue
        seen.add(sig)
        deduped.append(entry)

    write_jsonl(args.output_path, deduped)
    print(f"Removed {removed} duplicates. Wrote {len(deduped)} entries to {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
