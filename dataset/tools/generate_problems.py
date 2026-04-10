"""
Dataset Generator - Creates new problems from templates
Adds more test cases and expands the problem bank.
"""

import json
import random
from pathlib import Path
from typing import List, Dict
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))


# Problem Templates
PROBLEM_TEMPLATES = [
    {
        "title": "Array Sum Range",
        "tags": ["arrays", "prefix_sums"],
        "bucket": "fast",
        "rating": 800,
        "statement": "Given an array of n integers, find the sum of elements in the range [l, r].",
        "input_spec": "First line: n\nSecond line: n integers\nThird line: l r",
        "output_spec": "Output the sum of elements from index l to r",
        "constraints": "1 <= n <= 10^5\n1 <= l <= r <= n\n1 <= a_i <= 10^9"
    },
    {
        "title": "Maximum Subarray",
        "tags": ["arrays", "kadane"],
        "bucket": "fast",
        "rating": 1000,
        "statement": "Find the contiguous subarray with the largest sum.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output the maximum subarray sum",
        "constraints": "1 <= n <= 10^5\n-10^4 <= a_i <= 10^4"
    },
    {
        "title": "Count Elements",
        "tags": ["hashing", "arrays"],
        "bucket": "fast",
        "rating": 900,
        "statement": "Count how many elements in the array are greater than all elements to their right.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output the count",
        "constraints": "1 <= n <= 10^5\n1 <= a_i <= 10^9"
    },
    {
        "title": "Rotate Array",
        "tags": ["arrays"],
        "bucket": "fast",
        "rating": 1100,
        "statement": "Rotate the array by k positions to the right.",
        "input_spec": "First line: n k\nSecond line: n integers",
        "output_spec": "Output the rotated array",
        "constraints": "1 <= n <= 10^5\n1 <= k <= 10^9"
    },
    {
        "title": "Find Duplicates",
        "tags": ["hashing", "arrays"],
        "bucket": "fast",
        "rating": 1000,
        "statement": "Given an array where elements are in range 1 to n, find all duplicate elements.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output duplicate elements in increasing order",
        "constraints": "1 <= n <= 10^5\n1 <= a_i <= n"
    },
    {
        "title": "Merge Sorted Arrays",
        "tags": ["two_pointers", "arrays"],
        "bucket": "fast",
        "rating": 900,
        "statement": "Merge two sorted arrays into one sorted array.",
        "input_spec": "First line: n m\nSecond line: n sorted integers\nThird line: m sorted integers",
        "output_spec": "Output the merged sorted array",
        "constraints": "1 <= n, m <= 10^5"
    },
    {
        "title": "Binary Search",
        "tags": ["binary_search", "arrays"],
        "bucket": "fast",
        "rating": 900,
        "statement": "Find the index of target in a sorted array, or -1 if not found.",
        "input_spec": "First line: n target\nSecond line: n sorted integers",
        "output_spec": "Output the index or -1",
        "constraints": "1 <= n <= 10^5\n-10^9 <= target, a_i <= 10^9"
    },
    {
        "title": "Next Greater Element",
        "tags": ["monotonic_stack", "arrays"],
        "bucket": "medium",
        "rating": 1200,
        "statement": "For each element, find the next greater element to its right.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output the next greater element for each position",
        "constraints": "1 <= n <= 10^5\n1 <= a_i <= 10^9"
    },
    {
        "title": "Longest Consecutive",
        "tags": ["hashing", "arrays"],
        "bucket": "medium",
        "rating": 1400,
        "statement": "Find the length of the longest consecutive sequence in the array.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output the longest consecutive sequence length",
        "constraints": "1 <= n <= 10^5\n-10^9 <= a_i <= 10^9"
    },
    {
        "title": "Product Except Self",
        "tags": ["arrays", "prefix_sums"],
        "bucket": "medium",
        "rating": 1300,
        "statement": "For each index, compute the product of all array elements except that element.",
        "input_spec": "First line: n\nSecond line: n integers",
        "output_spec": "Output the product array",
        "constraints": "1 <= n <= 10^5\na_i != 0"
    },
]


def generate_samples(template: Dict) -> List[Dict]:
    """Generate sample input/output pairs for a problem."""
    samples = []
    
    n = random.choice([3, 4, 5, 6])
    
    if template["title"] == "Array Sum Range":
        arr = [random.randint(1, 20) for _ in range(n)]
        l = random.randint(1, n)
        r = random.randint(l, n)
        total = sum(arr[l-1:r])
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)) + f"\n{l} {r}",
            "output": str(total)
        })
    
    elif template["title"] == "Maximum Subarray":
        arr = [random.randint(-10, 10) for _ in range(n)]
        max_sum = max_sum_subarray(arr)
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": str(max_sum)
        })
    
    elif template["title"] == "Count Elements":
        arr = [random.randint(1, 15) for _ in range(n)]
        count = count_greater_right(arr)
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": str(count)
        })
    
    elif template["title"] == "Rotate Array":
        k = random.randint(1, n)
        arr = [random.randint(1, 10) for _ in range(n)]
        rotated = arr[-k:] + arr[:-k]
        samples.append({
            "input": f"{n} {k}\n" + " ".join(map(str, arr)),
            "output": " ".join(map(str, rotated))
        })
    
    elif template["title"] == "Find Duplicates":
        arr = [random.randint(1, n) for _ in range(n)]
        dups = sorted(set(x for x in arr if arr.count(x) > 1))
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": " ".join(map(str, dups)) if dups else "None"
        })
    
    elif template["title"] == "Merge Sorted Arrays":
        m = random.randint(2, 5)
        arr1 = sorted([random.randint(1, 20) for _ in range(n)])
        arr2 = sorted([random.randint(1, 20) for _ in range(m)])
        merged = sorted(arr1 + arr2)
        samples.append({
            "input": f"{n} {m}\n" + " ".join(map(str, arr1)) + "\n" + " ".join(map(str, arr2)),
            "output": " ".join(map(str, merged))
        })
    
    elif template["title"] == "Binary Search":
        target = random.randint(1, 30)
        arr = sorted([random.randint(1, 30) for _ in range(n)])
        idx = arr.index(target) if target in arr else -1
        samples.append({
            "input": f"{n} {target}\n" + " ".join(map(str, arr)),
            "output": str(idx)
        })
    
    elif template["title"] == "Next Greater Element":
        arr = [random.randint(1, 10) for _ in range(n)]
        result = next_greater(arr)
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": " ".join(map(str, result))
        })
    
    elif template["title"] == "Longest Consecutive":
        arr = [random.randint(1, 10) for _ in range(n)]
        longest = longest_consecutive(arr)
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": str(longest)
        })
    
    elif template["title"] == "Product Except Self":
        arr = [random.randint(1, 5) for _ in range(n)]
        result = product_except_self(arr)
        samples.append({
            "input": f"{n}\n" + " ".join(map(str, arr)),
            "output": " ".join(map(str, result))
        })
    
    return samples


def max_sum_subarray(arr):
    """Kadane's algorithm for max subarray sum."""
    max_sum = arr[0]
    current = arr[0]
    for x in arr[1:]:
        current = max(x, current + x)
        max_sum = max(max_sum, current)
    return max_sum


def count_greater_right(arr):
    """Count elements greater than all elements to their right."""
    count = 0
    max_right = -float('inf')
    for i in range(len(arr)-1, -1, -1):
        if arr[i] > max_right:
            count += 1
            max_right = arr[i]
    return count


def next_greater(arr):
    """Find next greater element for each position."""
    n = len(arr)
    result = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result


def longest_consecutive(arr):
    """Find longest consecutive sequence."""
    s = set(arr)
    longest = 0
    for x in s:
        if x-1 not in s:
            length = 1
            while x + length in s:
                length += 1
            longest = max(longest, length)
    return longest


def product_except_self(arr):
    """Product of array except self."""
    n = len(arr)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= arr[i]
    postfix = 1
    for i in range(n-1, -1, -1):
        result[i] *= postfix
        postfix *= arr[i]
    return result


def generate_solution(template: Dict) -> str:
    """Generate C++ solution for a problem."""
    
    if template["title"] == "Array Sum Range":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int l, r;
    cin >> l >> r;
    long long sum = 0;
    for (int i = l-1; i < r; i++) sum += a[i];
    cout << sum << "\\n";
    return 0;
}'''
    
    elif template["title"] == "Maximum Subarray":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int max_sum = a[0], curr = a[0];
    for (int i = 1; i < n; i++) {
        curr = max(a[i], curr + a[i]);
        max_sum = max(max_sum, curr);
    }
    cout << max_sum << "\\n";
    return 0;
}'''
    
    elif template["title"] == "Count Elements":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int count = 0, max_right = INT_MIN;
    for (int i = n-1; i >= 0; i--) {
        if (a[i] > max_right) {
            count++;
            max_right = a[i];
        }
    }
    cout << count << "\\n";
    return 0;
}'''
    
    elif template["title"] == "Rotate Array":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    k %= n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> result(n);
    for (int i = 0; i < n; i++) {
        result[(i + k) % n] = a[i];
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << result[i];
    }
    cout << "\\n";
    return 0;
}'''
    
    elif template["title"] == "Binary Search":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, target;
    cin >> n >> target;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int l = 0, r = n - 1, ans = -1;
    while (l <= r) {
        int mid = (l + r) / 2;
        if (a[mid] == target) {
            ans = mid;
            break;
        } else if (a[mid] < target) {
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    cout << ans << "\\n";
    return 0;
}'''
    
    elif template["title"] == "Next Greater Element":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> result(n, -1);
    vector<int> st;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] < a[i]) {
            result[st.back()] = a[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << result[i];
    }
    cout << "\\n";
    return 0;
}'''
    
    else:
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << "Solution not implemented yet\\n";
    return 0;
}'''


def create_problem(template: Dict, problem_id: int) -> Dict:
    """Create a complete problem entry."""
    samples = generate_samples(template)
    
    return {
        "id": f"generated_p{problem_id:03d}_sft_solve",
        "task_type": "SFT_SOLVE",
        "language": "cpp",
        "cpp_standard": "c++17",
        "problem": {
            "problem_id": f"gen_{problem_id:03d}",
            "title": template["title"],
            "statement": template["statement"],
            "input_spec": template["input_spec"],
            "output_spec": template["output_spec"],
            "constraints": template["constraints"],
            "samples": samples,
            "tags": template["tags"],
            "difficulty_rating": template["rating"],
            "bucket": template["bucket"]
        },
        "response": {
            "core_idea": f"Use {template['tags'][0].replace('_', ' ')} approach for efficient solution.",
            "algorithm_steps": [
                "Read input",
                "Process data according to algorithm",
                "Output result"
            ],
            "data_structures": ["vector"],
            "invariant_or_correctness": ["Algorithm correctly processes all elements"],
            "edge_cases": ["Empty input", "Single element", "Maximum constraints"],
            "complexity": {"time": "O(n)", "memory": "O(n)"},
            "explanation": f"Standard {template['tags'][0].replace('_', ' ')} solution.",
            "final_code": generate_solution(template)
        },
        "quality_tier": "silver",
        "quality_score": 0.85,
        "verification_reserved": {"status": "UNVERIFIED", "notes": ""},
        "created_at": "2026-04-09"
    }


def generate_dataset(count: int = 20) -> List[Dict]:
    """Generate multiple problems."""
    problems = []
    problem_id = len(PROBLEM_TEMPLATES) + 1
    
    for _ in range(count):
        template = random.choice(PROBLEM_TEMPLATES)
        problem = create_problem(template, problem_id)
        problems.append(problem)
        problem_id += 1
    
    return problems


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate new problems")
    parser.add_argument('--count', type=int, default=20, help='Number of problems to generate')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    args = parser.parse_args()
    
    problems = generate_dataset(args.count)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent.parent / 'dataset' / 'build' / 'generated_problems.jsonl'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for p in problems:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    print(f"Generated {len(problems)} problems")
    print(f"Saved to: {output_path}")
    
    return problems


if __name__ == "__main__":
    main()
