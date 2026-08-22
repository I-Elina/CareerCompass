import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.helpers import run_prompt_pipeline, classify_lead, send_lead_to_google_sheet

app = Flask(__name__)
# Enable CORS so your frontend pages can send requests without origin errors
CORS(app)

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
    2. Runs 6-stage AI prompt pipeline
    3. Qualifies and classifies lead
    4. Logs to Google Sheets (if applicable)
    5. Returns structured JSON report to frontend
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing assessment data"}), 400

        # Step 1: Run multi-stage AI reasoning chain
        print(f"[Pipeline] Processing career assessment for: {data.get('name', 'Anonymous')}")
        report = run_prompt_pipeline(data)

        # Step 2: Classify lead and check qualification
        is_lead, lead_type = classify_lead(data)
        print(f"[Lead Engine] Classified as: '{lead_type}' (Capture Required: {is_lead})")

        # Step 3: Send qualified leads to Google Sheet
        if is_lead:
            send_lead_to_google_sheet(data, lead_type, report)

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