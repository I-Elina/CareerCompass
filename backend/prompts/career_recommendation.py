def get_career_recommendations_prompt(profile_summary: str) -> str:
    """Generates the career paths recommendation promp]."""
    return f"""You are a senior career advisor.
Based on this student profile summary:
{profile_summary}

Recommend 3 to 5 realistic, high-potential career path].
For each path, strictly format as:
- Career Title: [Title]
- Why it suits the student: [Explanation]
- Relevant job roles: [Role 1, Role 2]
- Core skills required: [Skill 1, Skill 2]
- Current skill gaps: [Gap 1, Gap 2]"""