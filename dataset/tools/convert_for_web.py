"""
Convert dataset problems to web app format
"""

import json
from pathlib import Path

def get_difficulty(rating):
    if rating < 1200:
        return "Easy"
    elif rating < 1600:
        return "Medium"
    else:
        return "Hard"

def convert_problem(p):
    """Convert dataset format to web app format."""
    problem = p.get('problem', p)
    
    samples = problem.get('samples', [])
    formatted_samples = []
    for s in samples:
        input_str = s.get('input', '').strip()
        output_str = s.get('output', '').strip()
        formatted_samples.append({
            "input": input_str,
            "output": output_str
        })
    
    return {
        "id": problem.get('problem_id', p.get('id', 'unknown')),
        "title": problem.get('title', 'Unknown'),
        "difficulty": get_difficulty(problem.get('difficulty_rating', 1200)),
        "tags": problem.get('tags', []),
        "statement": problem.get('statement', '').replace('\n', ' '),
        "input_format": problem.get('input_spec', 'Not specified'),
        "output_format": problem.get('output_spec', 'Not specified'),
        "constraints": problem.get('constraints', 'Not specified'),
        "examples": formatted_samples,
        "rating": problem.get('difficulty_rating', 1200),
        "bucket": problem.get('bucket', 'medium')
    }

def main():
    dataset_path = Path(__file__).parent.parent.parent / 'dataset' / 'build' / 'train_full.jsonl'
    
    problems = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            p = json.loads(line)
            # Only include SFT_SOLVE problems (have code + test cases)
            if p.get('task_type') == 'SFT_SOLVE':
                problems.append(convert_problem(p))
    
    print(f"Found {len(problems)} problems with solutions")
    
    # Print as Python list for easy copy
    print("\n# Copy this to main_app.py SAMPLE_PROBLEMS variable:\n")
    print("SAMPLE_PROBLEMS = [")
    for p in problems:
        print(f"    {{")
        print(f"        \"id\": \"{p['id']}\",")
        print(f"        \"title\": \"{p['title']}\",")
        print(f"        \"difficulty\": \"{p['difficulty']}\",")
        print(f"        \"tags\": {json.dumps(p['tags'])},")
        print(f"        \"statement\": \"{p['statement'][:100]}...\" if len(p['statement']) > 100 else \"{json.dumps(p['statement'])}\",")
        print(f"        \"input_format\": {json.dumps(p['input_format'])},")
        print(f"        \"output_format\": {json.dumps(p['output_format'])},")
        print(f"        \"constraints\": {json.dumps(p['constraints'])[:50]}...\" if len(p['constraints']) > 50 else {json.dumps(p['constraints'])}},")
        print(f"        \"examples\": {json.dumps(p['examples'])}")
        print(f"    }},")
        print()
    print("]")
    
    # Save as JSON for reference
    output_path = Path(__file__).parent.parent / 'web_problems.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(problems)} problems to {output_path}")

if __name__ == "__main__":
    main()
