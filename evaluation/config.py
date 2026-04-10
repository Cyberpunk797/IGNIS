"""
Evaluation Configuration
Settings for connecting to LM Studio and evaluation parameters.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

API_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
API_KEY = "not-needed"
MODEL_NAME = "my model"  # Fine-tuned model

TIMEOUT = int(os.getenv("EVAL_TIMEOUT", "120"))
MAX_TOKENS = int(os.getenv("EVAL_MAX_TOKENS", "2048"))
TEMPERATURE = 0.2

COMPILER = "g++"
CXX_STANDARD = "c++17"
COMPILE_FLAGS = ["-std=c++17", "-O2", "-pipe"]

MAX_ATTEMPTS = 10

DATASET_PATH = BASE_DIR / "dataset" / "build" / "train_full.jsonl"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
TEMP_DIR = BASE_DIR / "evaluation" / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
