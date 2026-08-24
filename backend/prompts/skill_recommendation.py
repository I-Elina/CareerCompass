def get_skill_recommendation_prompt(career_paths: str, profile_summary: str) -> str:
    """Generates prioritized skill recommendation prompt."""
    return f"""You are a technical skills coach.
Based on the selected career paths:
{career_paths}

And current student profile:
{profile_summary}

Identify and prioritize the essential skills the student must acquire.
Group them into:
1. Core Technical / Hard Skills
2. High-Impact Tools & Frameworks
3. Essential Soft / Workplace Skills
Avoid overwhelming lists; prioritize high-leverage skills only."""