import os
from google import genai
from google.genai import types
from prompts.profile_analysis import get_profile_analysis_prompt
from prompts.skill_recommendation import get_skill_recommendation_prompt
from prompts.final_report import get_final_report_prompt

# Initialize the Gemini client (reads GEMINI_API_KEY from environment variables)
client = genai.Client()

def generate_ai_report(student_data: dict) -> dict:
    """Orchestrates the multi-step AI pipeline and returns the final JSON report."""
    
    # 1. Profile Analysis
    profile_prompt = get_profile_analysis_prompt(student_data)
    profile_response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=profile_prompt
    )
    profile_summary = profile_response.text

    # 2. Mock or pass career paths / other data needed for final synthesis
    # (If your pipeline generates intermediate steps, plug them in here)
    career_paths_data = "Targeting roles matching their profile ambitions, including non-traditional paths like small business and logistics."
    skills_data = "Core technical skills and tools required for execution."
    degrees_data = "Relevant certifications or degree pathways."
    universities_data = "Recommended programs or self-directed milestones."

    # 3. Final Report Synthesis
    final_prompt = get_final_report_prompt(
        profile_summary=profile_summary,
        career_paths=career_paths_data,
        skills=skills_data,
        degrees=degrees_data,
        universities=universities_data
    )
    
    final_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return final_response.text