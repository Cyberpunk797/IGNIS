# Dataset Architecture Plan

## Design Targets

The dataset is built for small-model reasoning quality, not raw scale. Every training item should reinforce a stable internal routine:

1. Understand the problem.
2. Choose an algorithm deliberately.
3. State a correctness argument or invariant.
4. Identify edge cases.
5. State complexity.
6. Produce disciplined C++17.

## Task Types

### `SFT_SOLVE`

Primary supervised format. The model sees the full problem and learns to emit:

- core idea
- algorithm steps
- data structures
- invariant / correctness reasoning
- edge cases
- complexity
- final C++17 code

### `PLAN_ONLY`

Reasoning-only format that suppresses code generation and strengthens algorithm selection, proof sketches, and complexity awareness.

### `REPAIR`

Bug-fixing format built around realistic failure modes:

- overflow
- off-by-one
- wrong comparator
- invalid loop order in DP
- stale state across test cases
- boundary handling
- missing cycle detection

### `OPTIMIZE`

Performance-refinement format that teaches the model to replace naive but correct code with a scalable algorithm.

## Dataset Flow

1. Author or synthesize custom problem specs.
2. Produce task-specific responses.
3. Validate schema and required fields.
4. Score structural quality.
5. Deduplicate by normalized statement and code signatures.
6. Merge into unified build files.
7. Split by `problem.problem_id` to prevent leakage across task variants.

## Quality Gates

An item is `gold` only if it has:

- a concrete algorithm selection
- a correctness argument
- stated edge cases
- explicit time and memory complexity
- clean C++17 with fast I/O
- no obvious statement ambiguity

`silver` remains trainable but typically has one weaker dimension, such as a shorter explanation or simpler reasoning.

## Future Verifier Compatibility

All entries reserve a `verification_reserved` block for future compiler, checker, or fuzzing signals. The current schema is designed so later passes can append:

- compile status
- sample execution status
- generated tests
- failure categories
- repair lineage

without breaking the training data contract.

## Split Policy

Split by `problem_id`, not by entry id. This prevents the same problem from appearing in train as `SFT_SOLVE` and in validation as `REPAIR` or `PLAN_ONLY`.

## Corpus Strategy

- First 100 problems are broad and pedagogical.
- Avoid exotic techniques unless they have unusually high teaching value.
- Prefer custom statements with standard algorithmic cores.
- Keep statements compact and deterministic so later synthesis remains easy to audit.
