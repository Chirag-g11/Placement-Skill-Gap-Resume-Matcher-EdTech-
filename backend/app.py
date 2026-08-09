"""
app.py
Flask API for the Placement Skill-Gap & Resume Matcher.

Endpoints
---------
POST /api/analyze
    multipart/form-data: resume=<file>, job_description=<text>
    -> full analysis JSON (match score, ATS check, skill gaps, roadmap)

GET /api/health
    simple health check
"""
import os
import traceback

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from resume_parser import extract_text, run_ats_checks
from matcher import analyze
from roadmap import generate_roadmap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
CORS(app)  # kept as a safety net; not needed once frontend is served from this same app

MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@app.route("/", methods=["GET"])
def index():
    """Serve the frontend directly, so there's exactly one server and one port."""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "resume-matcher-api"})


@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume file uploaded. Please attach a PDF/DOCX/TXT resume."}), 400

        job_description = (request.form.get("job_description") or "").strip()
        if not job_description or len(job_description) < 30:
            return jsonify({"error": "Please paste a full job description (at least a few sentences)."}), 400

        resume_file = request.files["resume"]
        filename = resume_file.filename or ""
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return jsonify({"error": f"Unsupported file type '{ext}'. Please upload a PDF, DOCX, or TXT resume."}), 400

        file_bytes = resume_file.read()
        if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
            return jsonify({"error": f"File too large. Max size is {MAX_FILE_SIZE_MB}MB."}), 400

        resume_text = extract_text(file_bytes, filename)
        if not resume_text or len(resume_text.strip()) < 30:
            return jsonify({"error": "Could not extract readable text from this resume. Try a text-based PDF (not a scanned image)."}), 422

        # --- Core NLP skill-gap analysis ---
        match_result = analyze(resume_text, job_description)

        # --- ATS formatting checks ---
        ats_result = run_ats_checks(resume_text)

        # --- Personalized roadmap for missing skills ---
        roadmap_result = generate_roadmap(match_result["missing_skills"])

        # --- Combined overall readiness score (match + ATS format) ---
        overall_score = round(
            match_result["final_match_score"] * 0.75 + ats_result["ats_format_score"] * 0.25, 1
        )

        response = {
            "overall_readiness_score": overall_score,
            "match": match_result,
            "ats": ats_result,
            "roadmap": roadmap_result,
            "meta": {
                "resume_filename": filename,
                "resume_word_count": ats_result["word_count"],
            },
        }
        return jsonify(response), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Internal error while analyzing: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
