import os
import gspread
from google.oauth2.service_account import Credentials

def append_row_to_sheet(row_data: list):
    """Appends a row of data to the designated Google Sheet."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Path to your Google Cloud service account credentials file
    creds_path = os.path.join(os.path.dirname(__file__), '../credentials.json')
    
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Google Sheets credentials.json not found at {creds_path}")
        
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    
    # Open your Google Sheet by name or URL (update 'CareerCounselingLeads' to your actual sheet name)
    sheet = client.open("CareerCounselingLeads").sheet1
    
    # Append the data row
    sheet.append_row(row_data)
    return True