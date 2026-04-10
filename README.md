# IGNIS

Self-Verifying Competitive Programming AI - Fine-tuned on Qwen2.5 for competitive programming problem solving with automatic self-correction.

## Overview

IGNIS is a next-gen competitive programming assistant that generates, executes, and iteratively repairs C++ solutions using a fine-tuned Qwen2.5-3B model.

Unlike standard LLMs, IGNIS does not return the first answer. It runs code against test cases, detects failures, and attempts automatic fixes before producing a final solution.

## Quick Start

### Prerequisites
- LM Studio (for local inference)
- g++ compiler (C++17) OR a remote judge (see below)
- Python 3.10+

### Setup

```bash
# 1. Install Python dependencies
cd evaluation
pip install -r requirements.txt

# 2. Load model in LM Studio
# - Open LM Studio
# - Load: aizu_qwen_coder_v1.gguf
# - Start server (Developer > Local Server)

# 3. Run evaluation
cd evaluation
python run_pass_at_k.py
```

## Features

- **Self-Verification Loop**: Generates solution → Tests it → Repairs if failed (up to 3 attempts)
- **Multi-attempt Solution Generation**: Pass@1, Pass@2, Pass@3 metrics
- **Built-in Compilation & Execution**: C++17 support with g++
- **LeetCode-Style Web Interface**: Dark theme with instant execution
- **50+ Practice Problems**: Arrays, Graphs, DP, Strings, etc.

## Project Structure

```
ignis/
├── app/                   # Flask web app
│   ├── main_app.py       # Backend server
│   └── templates/        # HTML templates
├── evaluation/           # Evaluation harness
│   ├── client.py        # LM Studio API
│   ├── compiler.py      # C++ compilation
│   ├── harness.py       # Evaluation pipeline
│   ├── grader.py        # Pass@K metrics
│   └── results/         # Evaluation outputs
├── dataset/             # Training data
├── training/           # QLoRA fine-tuning configs
├── judge/              # Docker judge server
└── libs/               # Shared utilities
```

## Performance

### Evaluation Results (20 problems, 3 attempts max)

| Metric | Score |
|--------|-------|
| **Pass@1** | 50% |
| **Pass@2** | 60% |
| **Pass@3** | 70% |
| Compilation Rate | 90% |
| Reasoning Quality | 98% |

### How Self-Verification Helps

| Attempts | Improvement |
|----------|-------------|
| 1 → 2 | +10% |
| 2 → 3 | +10% |

The self-repair loop significantly improves success rates!

## Stack

- **Python** - Backend & evaluation
- **Flask** - Web framework
- **C++17** - Code execution
- **QLoRA** - Fine-tuning
- **Qwen2.5-3B** - Base model
- **LM Studio** - Local inference

## License

MIT

## Acknowledgments

- Base model: [Qwen](https://huggingface.co/Qwen/Qwen2.5)
- Framework: [LM Studio](https://lmstudio.ai/)
