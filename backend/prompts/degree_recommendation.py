def get_degree_recommendations_prompt(profile_summary: str, career_paths: str, degree_mode: str) -> str:
    """Generates higher education and degree recommendation prompt[cite: 1]."""
    return f"""You are an academic pathway advisor.
Student Profile: {profile_summary}
Target Career Direction: {career_paths}
Preferred Study Mode: {degree_mode}[cite: 1]

Suggest suitable degree programs, specializations, and study modes (e.g., Online, Offline, Hybrid, Master's, Certifications) tailored to their target career and current academic level[cite: 1]."""