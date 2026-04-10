# AxLu-ZeSi CP

C++ Competitive Programming Reasoning Model - Fine-tuned on Qwen2.5 for competitive programming problem solving with structured reasoning.

## Overview

This project fine-tunes Qwen2.5 for C++ competitive programming tasks. The model generates:
- Algorithm plan and reasoning
- Correctness/invariant analysis
- Edge case handling
- Time and space complexity
- Clean, compilable C++17 code

## Quick Start

### Prerequisites
- LM Studio (for local inference)
- g++ compiler (C++17) OR a remote judge (see below)
- Python 3.10+

### Setup

```bash
# 1. Install Python dependencies
cd axlu-zesi-cp/evaluation
pip install -r requirements.txt

# 2. Load model in LM Studio
# - Open LM Studio
# - Load: aizu_qwen_coder_v1.gguf
# - Start server (Developer > Local Server)

# 3. Run evaluation
cd axlu-zesi-cp/evaluation
python run.py --problems 50
```

## True Server-Side Judge (No Local g++)

LeetCode-style platforms compile and run submissions on their own servers. This repo can do the same by running the
included judge service on a server that has Docker installed.

### Start the Judge on a Server

On the judge machine (Linux VM recommended):

```bash
cd axlu-zesi-cp
pip install -r judge/requirements.txt
export JUDGE_API_KEY="change-me"   # optional but strongly recommended
uvicorn judge.server:app --host 0.0.0.0 --port 8000
```

### Point the Web App at the Judge

On any machine running the UI:

```bash
export IGNIS_JUDGE_URL="http://<judge-host>:8000"
export IGNIS_JUDGE_API_KEY="change-me"  # if the judge requires it
```

Security note: a judge executes untrusted code. Keep it private (VPN/firewall), use an API key, and sandbox with Docker.

## Project Structure

```
axlu-zesi-cp/
├── architecture/          # Design documents
├── dataset/              # Training data
│   ├── build/            # Processed datasets
│   ├── raw/              # Raw problems
│   ├── schema/           # Data schemas
│   └── tools/            # Dataset utilities
├── evaluation/           # Evaluation harness
│   ├── client.py         # LM Studio API
│   ├── compiler.py       # C++ compilation
│   ├── harness.py        # Evaluation pipeline
│   ├── grader.py         # Pass@K metrics
│   └── results/          # Evaluation outputs
├── training/            # Training configs
│   ├── configs/         # QLoRA configs
│   └── scripts/         # Training scripts
├── app/                 # Inference app
└── libs/                # Shared libraries
```

## Model Details

| Property | Value |
|----------|-------|
| Base Model | Qwen2.5-3B/7B |
| Fine-tuning | QLoRA (4-bit NF4) |
| Format | GGUF |
| Language | C++17 only |

## Performance

### Test Results (50 problems, Pass@1)

| Metric | Score |
|--------|-------|
| Pass Rate | 40% |
| Compile Rate | 72% |
| Reasoning Quality | 97.5% |

### Topic Performance

**Strong (100%):**
- Prefix sums, Difference arrays
- Two pointers, Deque
- DSU (Disjoint Set Union)
- Binary search

**Needs Improvement (0%):**
- Arrays (basic)
- BFS/Graphs
- DP problems
- Bitmask

## Evaluation

### Run Full Evaluation
```bash
cd evaluation
python run.py --problems 50 --max-attempts 3
```

### Compare with Baseline
```bash
# Load original Qwen in LM Studio first
python compare_models.py --problems 20
```

### Evaluation Metrics
- **Pass@K**: Correct within K attempts
- **Compilation Rate**: % of responses that compile
- **Reasoning Score**: Quality of reasoning output

## Training

### Dataset
- 50 problems (currently)
- Task types: SFT_SOLVE, PLAN_ONLY, REPAIR, OPTIMIZE
- Difficulty: Fast (900-1200), Medium (1200-1600), High (1600+)

### Recommended Improvements
1. Expand dataset to 1000+ problems
2. Add more test cases per problem
3. Balance problem distribution
4. Add DP and graph problems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add problems or improve evaluation
4. Submit a pull request

## License

MIT

## Acknowledgments

- Base model: [Qwen](https://huggingface.co/Qwen/Qwen2.5)
- Framework: [LM Studio](https://lmstudio.ai/)
