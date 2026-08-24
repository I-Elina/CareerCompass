import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.helpers import run_career_pipeline, classify_lead, send_lead_to_google_sheet

# Load local environment variables (.env)
load_dotenv()

app = Flask(__name__)
# Enable CORS for frontend origin requests
CORS(app)

# Set USE_MOCK_DATA=True in your .env while testing CSS/layouts to use 0 API quota
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "False").lower() == "true"

MOCK_REPORT = {
    "career_profile": "Demonstrates strong analytical thinking and practical programming foundations with high potential for full-stack engineering and intelligent systems development.",
    "career_paths": [
        {
            "title": "Full-Stack AI Solutions Engineer",
            "fit_reason": "Direct alignment with modern web frameworks and machine learning integration pipelines.",
            "roles": ["Full-Stack Developer", "AI Engineer", "Application Architect"],
            "skill_gaps": ["Distributed Systems", "Cloud Orchestration (Docker/K8s)"]
        },
        {
            "title": "Systems & Cloud Infrastructure Engineer",
            "fit_reason": "Strong match for low-level foundations, network setups, and backend performance tuning.",
            "roles": ["DevOps Engineer", "Systems Programmer", "Backend Engineer"],
            "skill_gaps": ["CI/CD Automation", "Infrastructure as Code (Terraform)"]
        }
    ],
    "skills_to_learn": ["FastAPI & Microservices", "Vector Databases", "Docker & Kubernetes", "Asynchronous Python"],
    "recommended_degrees": ["B.Tech / M.Tech in Computer Science", "Specialized Post-Graduate Diploma in AI/Cloud"],
    "recommended_colleges": ["Premier Tech Institutes (Hybrid/Online Tracks)", "Accredited Global Cloud Platforms"],
    "short_term_plan": "Months 0-12: Build 2 production-ready capstone systems, master containerization, and publish open-source tooling.",
    "long_term_plan": "Years 1-3: Lead architectural decisions, deploy scalable microservice pipelines, and target specialized senior engineering roles.",
    "overall_summary": "High-trajectory profile suited for specialized engineering roles. Prioritize system design depth over surface-level tutorials."
}


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend is up."""
    return jsonify({
        "status": "online",
        "service": "Career Compass AI Engine",
        "version": "1.0.0"
    }), 200


@app.route("/api/analyze-career", methods=["POST"])
def analyze_career():
    """
    Main pipeline endpoint:
    1. Receives student assessment data
    2. Runs single-request AI reasoning pipeline
    3. Qualifies and classifies lead
    4. Logs to Google Sheets (if applicable)
    5. Returns structured JSON report to frontend
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing assessment data"}), 400

        print(f"[Pipeline] Processing career assessment for: {data.get('name', 'Anonymous')}")

        # Step 1: Run AI reasoning pipeline (or return mock data during UI testing)
        if USE_MOCK_DATA:
            print("[Pipeline] Using Mock Data (0 API quota used)")
            report = MOCK_REPORT
        else:
            report = run_career_pipeline(data)

        # Step 2: Classify lead and check qualification
        try:
            lead_type = classify_lead(data)
            is_lead = lead_type != "General Inquiry"
            print(f"[Lead Engine] Classified as: '{lead_type}' (Capture Required: {is_lead})")

            # Step 3: Send qualified leads to Google Sheet
            if is_lead:
                send_lead_to_google_sheet(data, lead_type)
        except Exception as lead_err:
            # Prevent sheet/classification errors from breaking the user's report generation
            print(f"[Lead Engine Notice] Could not log lead: {lead_err}")

        # Step 4: Return synthesized career report
        return jsonify(report), 200

    except Exception as e:
        print(f"[Error] Failed to process assessment: {e}")
        return jsonify({
            "error": "Failed to generate career report",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Career Compass Server running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)