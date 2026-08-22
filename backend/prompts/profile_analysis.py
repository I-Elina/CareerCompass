import json

def get_profile_analysis_prompt(student_data: dict) -> str:
    """Generates the profile analysis prompt[cite: 1]."""
    return f"""You are an expert educational counselor and student profiler.
Analyze the following student assessment data:
{json.dumps(student_data, indent=2)}

Provide a concise, objective summary of the student's core strengths, academic background, demonstrated interests, and career ambitions[cite: 1].
Keep it factual, encouraging, structured, and under 150 words."""