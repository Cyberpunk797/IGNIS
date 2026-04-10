"""
Prompt templates for competitive programming problems.
"""

SYSTEM_PROMPT = """You are an expert C++ competitive programming assistant.
You specialize in C++17 code generation with clear reasoning.

For each problem:
1. Explain your core idea (1-3 sentences)
2. Outline the algorithm steps
3. Discuss correctness/invariants
4. Mention edge cases
5. State time and space complexity
6. Provide clean, compilable C++17 code

IMPORTANT RULES:
- Always use fast I/O: ios::sync_with_stdio(false); cin.tie(nullptr);
- Use long long for numbers that may exceed 2^31
- Use std::vector instead of raw arrays for dynamic data
- Include all necessary headers (#include <bits/stdc++.h>)
- Wrap main logic in main() function
- Use namespace std;

Format your response as:
## Core Idea
[Your explanation]

## Algorithm
[Steps]

## Correctness
[Why it works]

## Edge Cases
[List edge cases]

## Complexity
[Time and Space]

## Code
```cpp
[Your C++ code]
```
"""


def build_prompt(problem: dict) -> str:
    """Build prompt from problem dictionary."""
    p = problem.get('problem', problem)
    
    prompt = f"""Problem: {p.get('title', 'Untitled')}

{p.get('statement', '')}

Input:
{p.get('input_spec', 'Not specified')}

Output:
{p.get('output_spec', 'Not specified')}

Constraints:
{p.get('constraints', 'Not specified')}
"""
    
    if 'samples' in p and p['samples']:
        prompt += "\nSample:\n"
        for i, sample in enumerate(p['samples'][:2]):
            prompt += f"Input: {sample.get('input', '').strip()}\n"
            prompt += f"Output: {sample.get('output', '').strip()}\n\n"
    
    prompt += "\nSolve this problem in C++17. Include reasoning and explanation."
    
    return prompt


def build_plan_only_prompt(problem: dict) -> str:
    """Build prompt for PLAN_ONLY problems (no code)."""
    p = problem.get('problem', problem)
    
    prompt = f"""Problem: {p.get('title', 'Untitled')}

{p.get('statement', '')}

Input:
{p.get('input_spec', 'Not specified')}

Output:
{p.get('output_spec', 'Not specified')}

Constraints:
{p.get('constraints', 'Not specified')}

Task: Provide ONLY the algorithm plan and reasoning. Do NOT write any code.

Explain:
1. Core idea
2. Algorithm steps
3. Data structures to use
4. Correctness reasoning / invariants
5. Edge cases
6. Time and space complexity
"""
    
    return prompt


def build_verification_prompt(problem: dict, code: str) -> str:
    """Build prompt for self-verification."""
    p = problem.get('problem', problem)
    
    prompt = f"""Problem: {p.get('title', 'Untitled')}

{p.get('statement', '')}

Input:
{p.get('input_spec', 'Not specified')}

Output:
{p.get('output_spec', 'Not specified')}

Constraints:
{p.get('constraints', 'Not specified')}

Your solution:
```cpp
{code}
```

Task: Verify if this solution is correct. Check for:
1. Logic errors
2. Edge case handling
3. Off-by-one errors
4. Type overflow issues

If you find issues, explain them and provide a corrected version.
"""
    
    return prompt
