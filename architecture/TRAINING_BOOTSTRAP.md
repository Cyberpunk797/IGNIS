# Training Bootstrap

## Intent

The repository is dataset-first, but the starter training configs are shaped for laptop-GPU QLoRA.

## Recommended Starting Point

- base model class: code-capable 3B-7B instruct model
- quantization: 4-bit NF4
- adapter: LoRA or QLoRA
- target context: 3072 to 4096 tokens
- curriculum: emphasize `SFT_SOLVE` and `PLAN_ONLY` first, then mix in `REPAIR` and `OPTIMIZE`

## Suggested Mixing

Early stage:

- `SFT_SOLVE`: 55%
- `PLAN_ONLY`: 20%
- `REPAIR`: 15%
- `OPTIMIZE`: 10%

Later stage:

- `SFT_SOLVE`: 40%
- `PLAN_ONLY`: 20%
- `REPAIR`: 20%
- `OPTIMIZE`: 20%

## Why This Mix

- `SFT_SOLVE` teaches end-to-end behavior
- `PLAN_ONLY` stabilizes algorithm selection
- `REPAIR` teaches local debugging
- `OPTIMIZE` teaches asymptotic discipline
