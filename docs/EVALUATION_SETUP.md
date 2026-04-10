# Evaluation Setup Guide

## Environment Requirements

### Hardware
- **GPU**: Recommended for training (RTX 4060 or better)
- **RAM**: 16GB+ recommended
- **Storage**: 10GB+ for models and datasets

### Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Scripts |
| LM Studio | Latest | Local inference |
| g++ | C++17 | Compile C++ code |
| Git | Latest | Version control |

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/axlu-zesi-cp.git
cd axlu-zesi-cp
```

### 2. Install Python Dependencies

```bash
cd axlu-zesi-cp/evaluation
pip install -r requirements.txt
```

### 3. Set Up LM Studio

1. Download [LM Studio](https://lmstudio.ai/)
2. Launch LM Studio
3. Load your model:
   - Click "Load Model"
   - Select `aizu_qwen_coder_v1.gguf`
   - Wait for model to load
4. Start local server:
   - Go to "Developer" tab
   - Click "Start Local Server"
   - Note the port (default: 1234)

### 4. Verify Setup

```bash
# Check g++ installation
g++ --version

# Check LM Studio connection
curl http://localhost:1234/v1/models
```

## Running Evaluation

### Basic Evaluation

```bash
cd axlu-zesi-cp/evaluation

# Test 10 problems
python run.py --problems 10

# Test all 50 problems
python run.py --problems 50

# Test with multiple attempts (Pass@K)
python run.py --problems 50 --max-attempts 3
```

### Filter by Task Type

```bash
# Only SFT_SOLVE problems (with code)
python run.py --task-type SFT_SOLVE

# Only PLAN_ONLY problems (reasoning only)
python run.py --task-type PLAN_ONLY
```

### Filter by Difficulty

```bash
# Easy problems (900-1200 rating)
python run.py --difficulty fast

# Medium problems (1200-1600 rating)
python run.py --difficulty medium

# Hard problems (1600+ rating)
python run.py --difficulty high
```

## Understanding Results

### Output Files

After evaluation, results are saved to:
```
evaluation/results/
├── raw_results.jsonl    # Detailed per-problem results
├── metrics.json         # Aggregated metrics
└── report.md           # Human-readable report
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| Pass@1 | % solved on first attempt |
| Pass@5 | % solved within 5 attempts |
| Pass@10 | % solved within 10 attempts |
| Compilation Rate | % of responses that compile |
| Reasoning Score | Quality of reasoning output |

## Comparing Models

### Test Original Qwen

1. In LM Studio, unload fine-tuned model
2. Load original Qwen model
3. Run comparison:

```bash
cd axlu-zesi-cp/evaluation
python quick_original_test.py
```

### Side-by-Side Comparison

1. Load fine-tuned model
2. Run: `python quick_finetuned_test.py`
3. Note results
4. Load original model
5. Run: `python quick_original_test.py`
6. Compare outputs in `results/COMPARISON_REPORT.md`

## Troubleshooting

### "No models loaded" Error

1. Check LM Studio server is running
2. Verify model is loaded (shows in top bar)
3. Try refreshing the server connection

### Compilation Errors

- Ensure g++ supports C++17: `g++ --version`
- Check MinGW is properly installed
- Try compiling manually: `g++ -std=c++17 -o test test.cpp`

### Connection Issues

- Check LM Studio server URL (default: `http://localhost:1234`)
- Verify firewall allows local connections
- Try different port in LM Studio settings

## Advanced Usage

### Custom Evaluation

Edit `config.py` to customize:
- `MAX_TOKENS`: Maximum response length
- `TEMPERATURE`: Sampling temperature (lower = more deterministic)
- `TIMEOUT`: Request timeout in seconds

### Adding New Problems

1. Add to `dataset/build/train_full.jsonl`
2. Follow schema format:
```json
{
  "id": "unique_id",
  "task_type": "SFT_SOLVE",
  "problem": {
    "title": "Problem Title",
    "statement": "...",
    "input_spec": "...",
    "output_spec": "...",
    "constraints": "...",
    "samples": [{"input": "...", "output": "..."}]
  },
  "response": {
    "final_code": "#include ..."
  }
}
```

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create new issue with:
   - Error message
   - System configuration
   - Steps to reproduce
