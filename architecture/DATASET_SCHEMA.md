# Unified Dataset Schema

## Common Fields

Every training item uses the same top-level structure:

```json
{
  "id": "string",
  "task_type": "SFT_SOLVE | PLAN_ONLY | REPAIR | OPTIMIZE",
  "language": "cpp",
  "cpp_standard": "c++17",
  "problem": {
    "problem_id": "string",
    "title": "string",
    "statement": "string",
    "input_spec": "string",
    "output_spec": "string",
    "constraints": "string",
    "samples": [
      {
        "input": "string",
        "output": "string"
      }
    ],
    "tags": ["string"],
    "difficulty_rating": 1400,
    "bucket": "fast | medium | high"
  },
  "response": {},
  "quality_tier": "gold | silver",
  "quality_score": 0.0,
  "verification_reserved": {
    "status": "UNVERIFIED",
    "notes": "string"
  },
  "created_at": "YYYY-MM-DD"
}
```

## `SFT_SOLVE`

```json
"response": {
  "core_idea": "string",
  "algorithm_steps": ["string"],
  "data_structures": ["string"],
  "invariant_or_correctness": ["string"],
  "edge_cases": ["string"],
  "complexity": {
    "time": "string",
    "memory": "string"
  },
  "explanation": "string",
  "final_code": "string"
}
```

## `PLAN_ONLY`

```json
"response": {
  "core_idea": "string",
  "algorithm_steps": ["string"],
  "data_structures": ["string"],
  "invariant_or_correctness": ["string"],
  "edge_cases": ["string"],
  "complexity": {
    "time": "string",
    "memory": "string"
  }
}
```

## `REPAIR`

```json
"response": {
  "buggy_code": "string",
  "bug_type": "string",
  "failure_description": {
    "type": "string",
    "failing_input": "string",
    "expected_output": "string",
    "got_output": "string"
  },
  "diagnosis": ["string"],
  "fix_explanation": "string",
  "fixed_code": "string"
}
```

## `OPTIMIZE`

```json
"response": {
  "slow_code": {
    "complexity": "string",
    "code": "string"
  },
  "why_too_slow": "string",
  "optimization_idea": "string",
  "new_complexity": {
    "time": "string",
    "memory": "string"
  },
  "optimized_code": "string"
}
```

## C++ Rules

- Always C++17
- Always include:
  - `ios::sync_with_stdio(false);`
  - `cin.tie(nullptr);`
- Use `long long` where sums or products can overflow `int`
- Avoid undefined behavior
- Keep code contest-readably clean
