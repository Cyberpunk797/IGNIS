# 100-Problem Generation Plan

## Difficulty Targets

- `0-1000`: 25 problems
- `1000-1400`: 30 problems
- `1400-1800`: 25 problems
- `1800-2100`: 15 problems
- `2100-2400`: 5 problems

## Coverage Rules

- Every problem is custom-written.
- Titles and stories are original.
- Core algorithms remain standard and pedagogically useful.
- The first 100 avoid niche topics unless they teach a very clean reasoning pattern.

## Topic Coverage

The 100-problem bank intentionally spans:

- arrays
- sorting
- prefix sums
- difference arrays
- two pointers
- sliding window
- binary search on answer
- hashing
- stacks / monotonic stacks
- queues / deques
- greedy
- intervals
- BFS
- DFS
- trees
- subtree DP basics
- DSU
- shortest paths
- topo sort
- Fenwick tree
- segment tree basics
- 1D DP
- 2D DP
- knapsack-style DP
- LIS
- bitmask brute force
- string algorithms
- KMP / Z
- modular arithmetic
- combinatorics basics

## Batch Strategy

### Batch 001

- 20 fully authored `SFT_SOLVE`
- 10 fully authored `PLAN_ONLY`
- 10 fully authored `REPAIR`
- 10 fully authored `OPTIMIZE`

### Batch 002+

Use the problem bank in `dataset/raw/problem_bank_100.jsonl` to continue authoring:

- more full SFT problems
- paired repair data
- optimization upgrades
- verifier-ready reserved metadata

## Operational Rule

Every later batch must maintain:

- difficulty balance
- topic spread
- no near-duplicate statements
- split safety by `problem_id`
- future compatibility with compiler/checker augmentation
