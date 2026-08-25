# 🧭 Career Compass AI Engine

An AI-powered career guidance and lead qualification platform built for intelligent student counseling, automated roadmap generation, and streamlined lead management.

## 🚀 Features
* **AI-Driven Assessment:** Synthesizes custom career profiles, skill gap analyses, and actionable short/long-term plans using Google Gemini models.
* **Smart Lead Qualification:** Automatically detects high-potential student leads opting into counseling or specialized educational tracks.
* **Google Sheets Integration:** Seamlessly syncs qualified student leads directly into a designated Google Sheet.
* **Responsive Dashboard:** Modern frontend interface providing detailed reports, print-ready views, and user feedback support.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-CORS, Google GenAI SDK, gspread
* **Frontend:** HTML5, CSS3, JavaScript, Tailwind CSS
* **Data Integration:** Google Sheets API & Google Drive API (via Service Accounts)

---

## ⚙️ Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/CareerCompass.git](https://github.com/your-username/CareerCompass.git)
cd CareerCompass

2. Set Up a Virtual Environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root/backend directory (refer to env.example):

GEMINI_API_KEY=your_actual_gemini_api_key_here
USE_MOCK_DATA=False

5. Configure Google Sheets Credentials (credentials.json)
To enable Google Sheets lead logging:
Go to the Google Cloud Console.
Enable the Google Sheets API and Google Drive API.
Create a Service Account under IAM & Admin, and download its key as a JSON file.
Place that JSON file in the services/ folder and rename it to credentials.json (Note: A boilerplate structure is typically ignored via .gitignore for security).
Share your target Google Sheet (CareerCounselingLeads) with the client_email found inside your credentials.json file granting Editor access.

Running the Application

Start the Flask Backend:

cd backend
python app.py

Launch the Frontend:
Open frontend/index.html using a local live server (such as VS Code's Live Server extension).