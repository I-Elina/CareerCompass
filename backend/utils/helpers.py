import json
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def run_career_pipeline(payload: dict) -> dict:
    """
    Executes the 6-stage career analysis in a single chat turn
    without developer instructions to prevent 400 errors and AFC warnings.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in the environment.")

    client = genai.Client(api_key=api_key)

    # Embed directives directly into the prompt to support models without developer instruction capability
    prompt = f"""
    You are an expert AI Career and Education Strategist. Evaluate the candidate profile thoroughly
    and return a clean, structured career blueprint in strict JSON format.

    Candidate Assessment Profile:
    - Name: {payload.get('name', 'Candidate')}
    - Education / Academic Status: {payload.get('education', 'N/A')}
    - Interests & Strengths: {payload.get('interests', 'N/A')}
    - Current Technical / Domain Skills: {payload.get('skills', 'N/A')}
    - Career Aspirations: {payload.get('goals', 'N/A')}
    - Preferred Learning / Degree Mode: {payload.get('study_mode', 'Flexible')}

    Synthesize all 6 evaluation areas:
    1. Profile Analysis & Foundational Strengths
    2. 3-4 High-Fit Career Paths (with target job titles and specific skill gaps)
    3. High-Priority Technical & Domain Skills to Master
    4. Degree & Specialization Recommendations
    5. Target Institutions & Delivery Modes
    6. Executive Short-term (0-12m) & Long-term (1-3y) Roadmap + Strategic Verdict

    Return ONLY a valid JSON object matching this schema:
    {{
      "career_profile": "Summary analysis of candidate background and positioning.",
      "career_paths": [
        {{
          "title": "Track Title",
          "fit_reason": "Specific rationale tailored to their profile.",
          "roles": ["Role 1", "Role 2"],
          "skill_gaps": ["Gap 1", "Gap 2"]
        }}
      ],
      "skills_to_learn": ["Skill 1", "Skill 2", "Skill 3", "Skill 4"],
      "recommended_degrees": ["Degree Track 1", "Degree Track 2"],
      "recommended_colleges": ["University / Provider 1", "University / Provider 2"],
      "short_term_plan": "Specific milestones for months 0-12.",
      "long_term_plan": "Strategic positioning for years 1-3.",
      "overall_summary": "Executive verdict and closing perspective."
    }}
    """

    # Using chat.send_message to eliminate AFC deprecation warnings
    chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7
        )
    )

    response = chat.send_message(prompt)
    raw_text = response.text.strip()

    # Clean markdown code block tags if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\n?", "", raw_text)
        raw_text = re.sub(r"\n?```$", "", raw_text).strip()

    return json.loads(raw_text)


def classify_lead(payload: dict) -> str:
    """Classifies user intent for counseling outreach."""
    study_mode = str(payload.get("study_mode", "")).lower()
    counseling = str(payload.get("counseling_interest", "")).lower()

    if "online" in study_mode and ("yes" in counseling or "true" in counseling):
        return "Online Degree - Counseling Interested"
    elif "online" in study_mode:
        return "Online Degree - Self Guided"
    elif "yes" in counseling or "true" in counseling:
        return "Campus Degree - Counseling Interested"
    return "General Inquiry"


def send_lead_to_google_sheet(payload: dict, classification: str):
    """Safely logs lead data to Google Sheets without crashing if credentials are missing."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "CareerCompass_Leads")

    if not os.path.exists(creds_path):
        return

    try:
        import gspread
        gc = gspread.service_account(filename=creds_path)
        sheet = gc.open(sheet_name).sheet1
        sheet.append_row([
            payload.get("name", "N/A"),
            payload.get("email", "N/A"),
            payload.get("education", "N/A"),
            payload.get("study_mode", "N/A"),
            classification
        ])
    except Exception as err:
        print(f"[Warning] Google Sheets logging failed: {err}")