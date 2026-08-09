"""
roadmap.py
Turns the list of missing skills into a prioritized, week-by-week
study roadmap using the curated LEARNING_RESOURCES map. Pure rule-based
logic — deterministic, explainable, and fast (no LLM dependency needed
for the core feature to work reliably during a live demo).
"""
from skills_db import LEARNING_RESOURCES, DEFAULT_RESOURCE, ALIAS_TO_SKILL, SKILL_TAXONOMY

# Category priority weighting — technical/core skills bridged before soft skills
CATEGORY_WEIGHT = {
    "Programming Languages": 5,
    "Data Structures & Algorithms": 5,
    "Backend": 4,
    "Databases": 4,
    "Frontend": 3,
    "Cloud & DevOps": 3,
    "Data Science & ML": 3,
    "Tools & Practices": 2,
    "Soft Skills": 1,
}


def _find_category(skill: str) -> str:
    for cat, skills in SKILL_TAXONOMY.items():
        if skill in skills:
            return cat
    return "Tools & Practices"


def generate_roadmap(missing_skills, max_items: int = 10) -> list:
    """
    Builds an ordered roadmap (highest priority first) capped at max_items
    so students get a focused, achievable plan instead of an overwhelming list.
    Each item includes a suggested start week so it reads like a real plan.
    """
    items = []
    for skill in missing_skills:
        category = _find_category(skill)
        resource_info = LEARNING_RESOURCES.get(skill, DEFAULT_RESOURCE)
        weight = CATEGORY_WEIGHT.get(category, 2)
        items.append({
            "skill": skill,
            "category": category,
            "resource": resource_info["resource"],
            "estimated_time": resource_info["time"],
            "difficulty": resource_info["difficulty"],
            "priority_weight": weight,
        })

    # Sort by category importance (desc); ties keep original (JD-frequency) order
    items.sort(key=lambda x: x["priority_weight"], reverse=True)
    items = items[:max_items]

    # Assign sequential "start week" so the roadmap reads as a real timeline
    week_cursor = 1
    for item in items:
        item["start_week"] = week_cursor
        time_str = item["estimated_time"]
        weeks = 1
        if "week" in time_str:
            try:
                weeks = int(time_str.split()[0].split("-")[0])
            except ValueError:
                weeks = 1
        elif "day" in time_str:
            weeks = 1
        week_cursor += max(weeks, 1)
        del item["priority_weight"]

    total_weeks = week_cursor - 1
    return {"roadmap": items, "estimated_total_weeks": total_weeks}
