# Quality Rubric

## Gold

- problem statement is unambiguous
- solution choice matches constraints
- correctness reasoning is explicit
- edge cases are non-empty and relevant
- complexity is stated
- code style is clean C++17
- fast I/O is present

## Silver

- still trainable
- may have shorter explanation or lighter proof detail
- no obvious algorithmic mismatch

## Automatic Heuristics

The first-pass scorer checks for:

- required fields by task type
- non-empty tags and samples
- presence of fast I/O in code tasks
- complexity fields
- invariant or correctness fields for reasoning tasks
- suspiciously short outputs

Automatic scoring is advisory. Human review can override.
