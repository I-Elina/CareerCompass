import os
import sys
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gspread
from google.oauth2.service_account import Credentials

# Ensure backend directory is in sys.path
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Load environment variables
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

# Initialize Google GenAI client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("[WARNING] GEMINI_API_KEY is not set in backend/.env!")

client = genai.Client(api_key=api_key)

# Import prompt generators
from prompts.profile_analysis import get_profile_analysis_prompt
from prompts.career_recommendation import get_career_recommendations_prompt
from prompts.skill_recommendation import get_skill_recommendation_prompt
from prompts.degree_recommendation import get_degree_recommendations_prompt
from prompts.university_recommendation import get_university_recommendation_prompt
from prompts.final_report import get_final_report_prompt

def call_llm(prompt_text: str, json_mode: bool = False) -> str:
    """Helper to send prompts to Google Gemini using the recommended Chat interface."""
    config = types.GenerateContentConfig(
        response_mime_type="application/json" if json_mode else "text/plain",
        temperature=0.7
    )
    # Using client.chats.create avoids the Automatic Function Calling (AFC) warning
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=config
    )
    
    response = chat.send_message(prompt_text)
    return response.text.strip()

def clean_json_response(raw_text: str) -> dict:
    """Safely extracts and parses JSON even if wrapped in markdown formatting."""
    cleaned = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
    return json.loads(cleaned)

def run_prompt_pipeline(student_data: dict) -> dict:
    """Executes the 6-stage modular prompt pipeline."""
    # 1. Profile Analysis
    p1 = get_profile_analysis_prompt(student_data)
    profile_summary = call_llm(p1)

    # 2. Career Recommendations
    p2 = get_career_recommendations_prompt(profile_summary)
    career_paths = call_llm(p2)

    # 3. Skills Recommendation
    p3 = get_skill_recommendation_prompt(career_paths, profile_summary)
    skills_rec = call_llm(p3)

    # 4. Degree Recommendations
    p4 = get_degree_recommendations_prompt(
        profile_summary, 
        career_paths, 
        student_data.get("degree_mode", "Not Sure")
    )
    degree_rec = call_llm(p4)

    # 5. University Recommendations
    p5 = get_university_recommendation_prompt(
        degree_rec, 
        student_data.get("budget", "Flexible"), 
        student_data.get("preferred_location", "Any")
    )
    university_rec = call_llm(p5)

    # 6. Final Report Synthesis
    p6 = get_final_report_prompt(profile_summary, career_paths, skills_rec, degree_rec, university_rec)
    final_raw = call_llm(p6, json_mode=True)
    return clean_json_response(final_raw)

def classify_lead(data: dict) -> tuple[bool, str]:
    """Classifies lead based on assessment answers."""
    mode = data.get("degree_mode", "")
    intent = data.get("counseling_intent", "")

    is_lead = (
        mode in ["Online Degree", "Distance Learning", "Hybrid"] or
        intent in ["Yes, I want counseling", "Yes, I want more information"]
    )

    if intent in ["Yes, I want counseling", "Yes, I want more information"]:
        lead_type = f"{mode} - Counseling Interested" if mode else "Counseling Interested"
    elif mode == "Online Degree":
        lead_type = "Online Degree Lead"
    elif mode == "Distance Learning":
        lead_type = "Distance Learning Lead"
    elif mode == "Hybrid":
        lead_type = "Hybrid Degree Lead"
    elif mode == "Offline/Regular Degree":
        lead_type = "Offline Degree Explorer"
    else:
        lead_type = "Career Guidance Only"

    return is_lead, lead_type

def send_lead_to_google_sheet(data: dict, lead_type: str, report: dict):
    """Logs qualified student leads to Google Sheet."""
    creds_path = os.path.join(BACKEND_DIR, "credentials.json")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Career_Leads")

    if not os.path.exists(creds_path):
        print("[Lead Logger] Optional: credentials.json not found. Lead recorded locally.")
        return

    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        gc = gspread.authorize(creds)
        sheet = gc.open(sheet_name).sheet1

        ai_career = report.get("career_paths", [{}])[0].get("title", "N/A") if isinstance(report.get("career_paths"), list) else "N/A"
        ai_degrees = ", ".join(report.get("recommended_degrees", [])) if isinstance(report.get("recommended_degrees"), list) else str(report.get("recommended_degrees", "N/A"))

        row = [
            data.get("name", ""),
            data.get("phone", ""),
            data.get("email", ""),
            data.get("course", ""),
            data.get("college", ""),
            data.get("career_field", ""),
            data.get("degree_mode", ""),
            data.get("counseling_intent", ""),
            lead_type,
            ai_career,
            ai_degrees,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CareerCompass Web App"
        ]

        sheet.append_row(row)
        print(f"[Lead Logger] Successfully logged lead for {data.get('name')}")
    except Exception as e:
        print(f"[Lead Logger] Google Sheets error: {e}")