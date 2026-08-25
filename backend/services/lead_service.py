from services.sheets_service import append_row_to_sheet
from datetime import datetime

def save_counseling_lead(
    name: str, 
    email: str, 
    phone: str, 
    current_education: str,
    current_course: str,
    college: str,
    career_interest: str,
    preferred_degree_mode: str,
    counseling_required: str,
    preferred_specialization: str,
    ai_recommended_career: str,
    ai_recommended_degree: str,
    lead_source: str = "Web Form"
) -> bool:
    """Formats and saves complete counseling lead data matching project specs."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Order of columns matching the project specification sheet fields
        row_data = [
            timestamp, 
            name, 
            phone, 
            email, 
            current_education, 
            current_course, 
            college, 
            career_interest, 
            preferred_degree_mode, 
            counseling_required, 
            preferred_specialization, 
            ai_recommended_career, 
            ai_recommended_degree, 
            lead_source
        ]
        
        success = append_row_to_sheet(row_data)
        return success
    except Exception as e:
        print(f"[Lead Service Error]: {e}")
        # Fallback graceful handling so the app doesn't crash if credentials.json is missing locally
        print(f"[Local Lead Capture fallback]: Lead identified for {name} ({email})")
        return False