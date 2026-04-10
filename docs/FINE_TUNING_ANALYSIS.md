# Fine-Tuning Analysis: aizu_qwen_coder_v1.gguf

## What We Know About This Model

### Model Details
| Property | Value |
|----------|-------|
| **File** | `aizu_qwen_coder_v1.gguf` |
| **Size** | 4.46 GB |
| **Format** | GGUF (Q4_K_M quantization typical) |
| **Base Model** | Likely Qwen2.5-3B or Qwen2.5-7B |
| **Fine-tuned by** | Your friend |

### Estimated Base Model
Based on the 4.46 GB size, this is most likely:
- **Qwen2.5-3B** in Q4_K_M quantization (3B params ≈ 2-3 GB Q4)
- Or **Qwen2.5-1.5B** in higher quality quantization

### Training Configuration (From Your Repo)

Based on `training/configs/qlora.yaml`:

| Parameter | Value |
|-----------|-------|
| **Method** | QLoRA (4-bit NF4) |
| **LoRA Rank (r)** | 32 |
| **LoRA Alpha** | 64 |
| **LoRA Dropout** | 0.05 |
| **Target Modules** | All attention projections |
| **Max Sequence Length** | 3584 tokens |
| **Batch Size** | 1 (with gradient accumulation 16) |
| **Learning Rate** | 0.0002 (2e-4) |
| **Epochs** | 2 |
| **bf16** | Enabled |
| **Gradient Checkpointing** | Enabled |

### Training Dataset

From `dataset/build/train_full.jsonl`:

| Metric | Value |
|--------|-------|
| **Total Problems** | 50 |
| **Task Types** | SFT_SOLVE, PLAN_ONLY, REPAIR, OPTIMIZE |

#### Task Distribution:
- **SFT_SOLVE**: Primary problem solving (20 problems)
- **PLAN_ONLY**: Algorithm reasoning (10 problems)
- **REPAIR**: Debugging (10 problems)
- **OPTIMIZE**: Optimization (10 problems)

#### Difficulty Coverage:
- **Fast (900-1200)**: Easy problems
- **Medium (1200-1600)**: Medium problems  
- **High (1600+)**: Hard problems

### Topics Covered
- Arrays, Prefix Sums, Difference Array
- Sorting, Two Pointers, Sliding Window
- Monotonic Stack, Deque
- Binary Search, Greedy
- BFS/DFS, Trees, Dijkstra
- DSU, Fenwick Tree, Segment Tree
- DP (1D, 2D), Knapsack, LIS
- Bitmask, KMP, Z-Algorithm

### Recommended Mixing (From Architecture)
```
Early stage:
- SFT_SOLVE: 55%
- PLAN_ONLY: 20%
- REPAIR: 15%
- OPTIMIZE: 10%

Later stage:
- SFT_SOLVE: 40%
- PLAN_ONLY: 20%
- REPAIR: 20%
- OPTIMIZE: 20%
```

## Current Performance (From Our Evaluation)

### Overall Results (50 problems, Pass@1):
| Metric | Score |
|--------|-------|
| **Pass Rate** | 40% (20/50) |
| **Compile Rate** | 72% (36/50) |
| **Reasoning Quality** | 97.5% |

### Strengths:
- Prefix sums, difference arrays: 100%
- Two pointers, deque, DSU: 100%
- Binary search: 100%
- Sorting problems: Variable

### Weaknesses:
- Arrays (basic): 0%
- BFS/Graphs: 0%
- DP problems: 0%
- Bitmask: 0%
- Segment trees: 0%

## Comparison with Original Qwen

To compare with the original Qwen model:

1. **Unload current model in LM Studio**
2. **Download original Qwen2.5 model**:
   - Qwen2.5-3B: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF
   - Qwen2.5-7B: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
3. **Load original model in LM Studio**
4. **Run comparison**: `python evaluation/compare_models.py`

## Recommendations for Improvement

### 1. Increase Dataset Size
Current: 50 problems
Recommended: 1000-5000 problems

### 2. Add More Test Cases Per Problem
Current: 1-2 test cases
Recommended: 3-5 test cases (especially edge cases)

### 3. Balance Problem Distribution
- Add more DP problems (currently 0% success)
- Add more graph/BFS problems
- Add segment tree problems

### 4. Verify Training Mixing
Ensure the actual training followed the recommended mixing ratios

### 5. Consider Curriculum Learning
1. First: Train on easy problems (fast bucket)
2. Then: Gradually introduce medium/hard problems

## Files for Reference

- Training config: `training/configs/qlora.yaml`
- Curriculum: `training/configs/curriculum.yaml`
- Architecture: `ARCHITECTURE_Qlora_Laptop_AxLu_ZeSi.md`
- Training bootstrap: `architecture/TRAINING_BOOTSTRAP.md`
