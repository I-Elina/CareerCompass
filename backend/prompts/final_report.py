def get_final_report_prompt(profile_summary: str, career_paths: str, skills: str, degrees: str, universities: str) -> str:
    """Generates final synthesized structured JSON report[cite: 1]."""
    return f"""You are an executive career coach compiling the final student career report[cite: 1].
Combine the following structured sections:
- Profile Analysis: {profile_summary}[cite: 1]
- Recommended Career Paths: {career_paths}[cite: 1]
- Prioritized Skills: {skills}[cite: 1]
- Degree Pathways: {degrees}[cite: 1]
- College Suggestions: {universities}[cite: 1]

You must output STRICT JSON with this exact schema (no markdown wraps, pure JSON)[cite: 1]:
{{
  "career_profile": "Concise summary of student profile",
  "career_paths": [
    {{
      "title": "Role Name",
      "fit_reason": "Why it suits them",
      "roles": ["Job 1", "Job 2"],
      "skill_gaps": ["Gap 1", "Gap 2"]
    }}
  ],
  "skills_to_learn": ["Skill 1", "Skill 2", "Skill 3"],
  "recommended_degrees": ["Degree 1", "Degree 2"],
  "recommended_colleges": ["University 1", "University 2"],
  "short_term_plan": "Next 3-6 months focus (projects, learning, internships)",
  "long_term_plan": "Next 1-3 years progression (degrees, higher roles)",
  "overall_summary": "Encouraging closing recommendation"
}}"""