# Inference Contracts

## Fast Mode

Use for low latency. Output:

1. core idea
2. short algorithm steps
3. complexity
4. final C++17

## Medium Mode

Use as default. Output:

1. plan
2. correctness argument
3. edge cases
4. complexity
5. final C++17

## High Mode

Use for harder problems. Output:

1. restatement
2. key observations
3. algorithm plan
4. correctness / invariant reasoning
5. edge-case audit
6. complexity
7. final C++17

## Safety Constraints

- never output non-C++ code
- default to C++17
- always include fast I/O
- avoid speculative unsupported optimizations
