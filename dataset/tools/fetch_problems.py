"""
Problem Fetcher - LeetCode and Codeforces
Fetches real competitive programming problems from public APIs.
"""

import json
import random
import time
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error


class LeetCodeFetcher:
    """Fetch problems from LeetCode GraphQL API."""
    
    GRAPHQL_URL = "https://leetcode.com/graphql"
    
    QUERY = """
    {
        problemsetQuestionList(
            limit: 100
            skip: 0
            filters: {"difficulty": "%s"}
        ) {
            titleSlug
            title
            difficulty
            topicTags { name }
        }
    }
    """
    
    def __init__(self):
        self.session = None
    
    def fetch_problems(self, difficulty: str = "MEDIUM") -> List[Dict]:
        """Fetch problems by difficulty: EASY, MEDIUM, HARD"""
        query = self.QUERY % difficulty.upper()
        
        try:
            req = urllib.request.Request(
                self.GRAPHQL_URL,
                data=json.dumps({"query": query}).encode(),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read())
                problems = data.get("data", {}).get("problemsetQuestionList", [])
                
                return [
                    {
                        "source": "leetcode",
                        "title": p["title"],
                        "slug": p["titleSlug"],
                        "difficulty": p["difficulty"],
                        "tags": [t["name"] for t in p.get("topicTags", [])],
                        "url": f"https://leetcode.com/problems/{p['titleSlug']}/"
                    }
                    for p in problems
                ]
        except Exception as e:
            print(f"LeetCode fetch error: {e}")
            return []
    
    def fetch_problem_details(self, slug: str) -> Optional[Dict]:
        """Fetch detailed problem info including examples."""
        query = """
        {
            question(titleSlug: "%s") {
                title
                difficulty
                exampleTestcases
                content
                topicTags { name }
            }
        }
        """ % slug
        
        try:
            req = urllib.request.Request(
                self.GRAPHQL_URL,
                data=json.dumps({"query": query}).encode(),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read())
                return data.get("data", {}).get("question")
        except Exception as e:
            print(f"LeetCode detail fetch error: {e}")
            return None


class CodeforcesFetcher:
    """Fetch problems from Codeforces API."""
    
    API_URL = "https://codeforces.com/api"
    
    def fetch_problems(self, min_rating: int = 800, max_rating: int = 1600) -> List[Dict]:
        """Fetch problems by rating range."""
        try:
            url = f"{self.API_URL}/problemset.problems"
            
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read())
                
                if data["status"] != "OK":
                    return []
                
                problems = []
                for p in data["result"]["problems"]:
                    rating = p.get("rating", 0)
                    if min_rating <= rating <= max_rating:
                        problems.append({
                            "source": "codeforces",
                            "title": p.get("name", "Unknown"),
                            "contest_id": p.get("contestId", 0),
                            "index": p.get("index", ""),
                            "rating": rating,
                            "tags": p.get("tags", []),
                            "url": f"https://codeforces.com/problemset/problem/{p.get('contestId')}/{p.get('index')}"
                        })
                
                return problems
        except Exception as e:
            print(f"Codeforces fetch error: {e}")
            return []
    
    def fetch_contest_problems(self, contest_id: int) -> List[Dict]:
        """Fetch problems from a specific contest."""
        try:
            url = f"{self.API_URL}/problemset.problems?tags="
            
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read())
                
                if data["status"] != "OK":
                    return []
                
                return [
                    {
                        "source": "codeforces",
                        "title": p.get("name", "Unknown"),
                        "contest_id": p.get("contestId", 0),
                        "index": p.get("index", ""),
                        "rating": p.get("rating", 0),
                        "tags": p.get("tags", []),
                        "url": f"https://codeforces.com/problemset/problem/{p.get('contestId')}/{p.get('index')}"
                    }
                    for p in data["result"]["problems"]
                    if p.get("contestId") == contest_id
                ]
        except Exception as e:
            print(f"Codeforces contest fetch error: {e}")
            return []


def create_mixed_dataset(count: int = 30, difficulty: str = "MEDIUM") -> List[Dict]:
    """Create a mixed dataset from LeetCode and Codeforces."""
    
    print("Fetching problems from LeetCode...")
    lc_fetcher = LeetCodeFetcher()
    lc_problems = lc_fetcher.fetch_problems(difficulty)
    print(f"  Found {len(lc_problems)} LeetCode {difficulty} problems")
    
    time.sleep(1)
    
    print("Fetching problems from Codeforces...")
    cf_fetcher = CodeforcesFetcher()
    cf_problems = cf_fetcher.fetch_problems(min_rating=800, max_rating=1600)
    print(f"  Found {len(cf_problems)} Codeforces problems (rating 800-1600)")
    
    mixed = []
    
    lc_count = count // 2
    cf_count = count - lc_count
    
    if lc_problems:
        sample_lc = random.sample(lc_problems, min(lc_count, len(lc_problems)))
        for p in sample_lc:
            p["id"] = f"lc_{len(mixed)+1:03d}"
            mixed.append(p)
    
    if cf_problems:
        sample_cf = random.sample(cf_problems, min(cf_count, len(cf_problems)))
        for p in sample_cf:
            p["id"] = f"cf_{len(mixed)+1:03d}"
            mixed.append(p)
    
    random.shuffle(mixed)
    
    return mixed


def save_to_jsonl(problems: List[Dict], output_path: Path):
    """Save problems to JSONL file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for p in problems:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    print(f"\nSaved {len(problems)} problems to {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch LeetCode and Codeforces problems")
    parser.add_argument('--count', type=int, default=30, help='Total problems to fetch')
    parser.add_argument('--difficulty', type=str, default='MEDIUM', 
                       choices=['EASY', 'MEDIUM', 'HARD'], help='LeetCode difficulty')
    parser.add_argument('--output', type=str, default=None, help='Output file')
    
    args = parser.parse_args()
    
    problems = create_mixed_dataset(args.count, args.difficulty)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent.parent / 'dataset' / 'build' / 'mixed_problems.jsonl'
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_to_jsonl(problems, output_path)
    
    print("\nProblem Sources:")
    lc_count = sum(1 for p in problems if p['source'] == 'leetcode')
    cf_count = sum(1 for p in problems if p['source'] == 'codeforces')
    print(f"  LeetCode: {lc_count}")
    print(f"  Codeforces: {cf_count}")
    
    return problems


if __name__ == "__main__":
    main()
