def get_university_recommendation_prompt(degree_rec: str, budget: str, location: str) -> str:
    """Generates university and college recommendation prompt."""
    return f"""You are a university admissions consultant.
Recommended Degrees: {degree_rec}
Student Budget: {budget}
Preferred Location: {location}

Suggest matching colleges and universities that offer these programs.
Distinguish between verified institutions and AI-suggested exploratory options."""