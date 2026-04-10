import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Starter launcher placeholder for QLoRA training.")
    parser.add_argument("--config", default="training/configs/qlora.yaml", help="Path to qlora yaml config")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config: {config_path}")

    print("Starter script only.")
    print("Use this repository's dataset preparation first, then connect your preferred TRL/PEFT trainer.")
    print(f"Loaded config path: {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
