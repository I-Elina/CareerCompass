def get_university_recommendation_prompt(degree_rec: str, budget: str, location: str) -> str:
    """Generates university and college recommendation prompt[cite: 1]."""
    return f"""You are a university admissions consultant.
Recommended Degrees: {degree_rec}[cite: 1]
Student Budget: {budget}[cite: 1]
Preferred Location: {location}[cite: 1]

Suggest matching colleges and universities that offer these programs[cite: 1].
Distinguish between verified institutions and AI-suggested exploratory options[cite: 1]."""