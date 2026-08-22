import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default-dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Google Sheets Configuration (Optional Lead Engine)
    GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "CareerCompass_Leads")
    CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

    @classmethod
    def validate_config(cls):
        """Validates that critical environment variables are loaded."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("CRITICAL ERROR: GEMINI_API_KEY is not set in the environment.")