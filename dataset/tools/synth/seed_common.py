from copy import deepcopy
from textwrap import dedent

CREATED_AT = "2026-03-22"


def clean(text: str) -> str:
    return dedent(text).strip("\n")


def block(text: str) -> str:
    return clean(text) + "\n"


def sample(input_text: str, output_text: str) -> dict:
    return {"input": block(input_text), "output": block(output_text)}


def cpp(code: str) -> str:
    return block(code)


def bucket_from_difficulty(difficulty: int) -> str:
    if difficulty <= 1200:
        return "fast"
    if difficulty <= 1800:
        return "medium"
    return "high"


def make_problem(
    problem_id: str,
    title: str,
    statement: str,
    input_spec: str,
    output_spec: str,
    constraints: str,
    samples: list[dict],
    tags: list[str],
    difficulty_rating: int,
) -> dict:
    return {
        "problem_id": problem_id,
        "title": title,
        "statement": clean(statement),
        "input_spec": clean(input_spec),
        "output_spec": clean(output_spec),
        "constraints": clean(constraints),
        "samples": samples,
        "tags": tags,
        "difficulty_rating": difficulty_rating,
        "bucket": bucket_from_difficulty(difficulty_rating),
    }


def make_bank_entry(problem_id: str, title: str, difficulty_rating: int, tags: list[str], planned_tasks: list[str], status: str, concept_pitch: str) -> dict:
    return {
        "problem_id": problem_id,
        "title": title,
        "difficulty_rating": difficulty_rating,
        "bucket": bucket_from_difficulty(difficulty_rating),
        "tags": tags,
        "planned_tasks": planned_tasks,
        "status": status,
        "concept_pitch": concept_pitch,
    }


PROBLEMS: dict[str, dict] = {}
PROBLEM_BANK_100: list[dict] = []
SFT_ENTRIES: list[dict] = []
PLAN_ONLY_ENTRIES: list[dict] = []
REPAIR_ENTRIES: list[dict] = []
OPTIMIZE_ENTRIES: list[dict] = []


def register_detailed(problem: dict, planned_tasks: list[str], concept_pitch: str) -> None:
    PROBLEMS[problem["problem_id"]] = problem
    PROBLEM_BANK_100.append(
        make_bank_entry(
            problem_id=problem["problem_id"],
            title=problem["title"],
            difficulty_rating=problem["difficulty_rating"],
            tags=problem["tags"],
            planned_tasks=planned_tasks,
            status="detailed",
            concept_pitch=concept_pitch,
        )
    )


def register_planned(problem_id: str, title: str, difficulty_rating: int, tags: list[str], planned_tasks: list[str], concept_pitch: str) -> None:
    PROBLEM_BANK_100.append(
        make_bank_entry(problem_id, title, difficulty_rating, tags, planned_tasks, "planned", concept_pitch)
    )


def build_entry(problem_id: str, task_type: str, response: dict, quality_tier: str, quality_score: float) -> dict:
    return {
        "id": f"{problem_id}_{task_type.lower()}",
        "task_type": task_type,
        "language": "cpp",
        "cpp_standard": "c++17",
        "problem": deepcopy(PROBLEMS[problem_id]),
        "response": response,
        "quality_tier": quality_tier,
        "quality_score": quality_score,
        "verification_reserved": {
            "status": "UNVERIFIED",
            "notes": "Custom-authored item. Reserved for future compile/checker verification.",
        },
        "created_at": CREATED_AT,
    }


def sft_response(core_idea: str, algorithm_steps: list[str], data_structures: list[str], invariant_or_correctness: list[str], edge_cases: list[str], time_complexity: str, memory_complexity: str, explanation: str, final_code: str) -> dict:
    return {
        "core_idea": core_idea,
        "algorithm_steps": algorithm_steps,
        "data_structures": data_structures,
        "invariant_or_correctness": invariant_or_correctness,
        "edge_cases": edge_cases,
        "complexity": {"time": time_complexity, "memory": memory_complexity},
        "explanation": explanation,
        "final_code": final_code,
    }


def plan_only_response(core_idea: str, algorithm_steps: list[str], data_structures: list[str], invariant_or_correctness: list[str], edge_cases: list[str], time_complexity: str, memory_complexity: str) -> dict:
    return {
        "core_idea": core_idea,
        "algorithm_steps": algorithm_steps,
        "data_structures": data_structures,
        "invariant_or_correctness": invariant_or_correctness,
        "edge_cases": edge_cases,
        "complexity": {"time": time_complexity, "memory": memory_complexity},
    }
