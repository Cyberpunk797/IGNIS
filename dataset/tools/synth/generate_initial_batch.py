from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SYNTH_DIR = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SYNTH_DIR) not in sys.path:
    sys.path.insert(0, str(SYNTH_DIR))

from libs.jsonl import write_jsonl  # noqa: E402
import seed_common  # noqa: E402
import problem_defs_1  # noqa: F401,E402
import problem_defs_2  # noqa: F401,E402
import problem_defs_3  # noqa: F401,E402
import extra_bank  # noqa: F401,E402
import batch_sft_1  # noqa: F401,E402
import batch_sft_2  # noqa: F401,E402
import batch_sft_3  # noqa: F401,E402
import batch_sft_4  # noqa: F401,E402
import batch_plan_only  # noqa: F401,E402
import batch_repair_1  # noqa: F401,E402
import batch_repair_2  # noqa: F401,E402
import batch_optimize_1  # noqa: F401,E402
import batch_optimize_2  # noqa: F401,E402


def main() -> int:
    raw_dir = ROOT / "dataset" / "raw"
    build_dir = ROOT / "dataset" / "build"
    raw_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    write_jsonl(raw_dir / "problem_bank_100.jsonl", seed_common.PROBLEM_BANK_100)
    write_jsonl(raw_dir / "batch_001_sft_solve.jsonl", seed_common.SFT_ENTRIES)
    write_jsonl(raw_dir / "batch_001_plan_only.jsonl", seed_common.PLAN_ONLY_ENTRIES)
    write_jsonl(raw_dir / "batch_001_repair.jsonl", seed_common.REPAIR_ENTRIES)
    write_jsonl(raw_dir / "batch_001_optimize.jsonl", seed_common.OPTIMIZE_ENTRIES)

    merged = (
        seed_common.SFT_ENTRIES
        + seed_common.PLAN_ONLY_ENTRIES
        + seed_common.REPAIR_ENTRIES
        + seed_common.OPTIMIZE_ENTRIES
    )
    write_jsonl(build_dir / "train_batch_001.jsonl", merged)
    write_jsonl(build_dir / "train_full.jsonl", merged)

    print(f"problem_bank={len(seed_common.PROBLEM_BANK_100)}")
    print(f"sft={len(seed_common.SFT_ENTRIES)}")
    print(f"plan_only={len(seed_common.PLAN_ONLY_ENTRIES)}")
    print(f"repair={len(seed_common.REPAIR_ENTRIES)}")
    print(f"optimize={len(seed_common.OPTIMIZE_ENTRIES)}")
    print(f"merged={len(merged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
