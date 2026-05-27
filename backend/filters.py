# filters.py — issues filter karo by skill, difficulty, label

def filter_issues(issues: list, skills: list, difficulty: str, label: str) -> list:
    result = []

    for issue in issues:
        labels_lower = [l.lower() for l in issue["labels"]]
        title_lower = issue["title"].lower()
        body_lower = issue["body_preview"].lower()
        lang_lower = (issue["repo_language"] or "").lower()

        # Skill match — repo language ya title/body mein skill mention ho
        if skills:
            matched = any(
                s in lang_lower or s in title_lower or s in body_lower
                for s in skills
            )
            if not matched:
                continue

        # Difficulty filter — label mein check karo
        if difficulty:
            diff_map = {
                "beginner": ["good first issue", "beginner", "level:beginner"],
                "intermediate": ["intermediate", "level:intermediate"],
                "advanced": ["advanced", "level:advanced"],
            }
            wanted = diff_map.get(difficulty.lower(), [])
            if not any(w in " ".join(labels_lower) for w in wanted):
                continue

        # Label filter — e.g. "bug", "feature"
        if label and label.lower() not in " ".join(labels_lower):
            continue

        result.append(issue)

    return result
