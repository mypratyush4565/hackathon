from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import hashlib
import time

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

CORS(app)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Register Evidence API
@app.route("/api/register", methods=["POST"])
def register_evidence():
    file = request.files.get("file")
    case_id = request.form.get("caseId")
    uploader = request.form.get("uploaderName")
    source = request.form.get("sourceType")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    content = file.read()
    sha256 = hashlib.sha256(content).hexdigest()

    evidence_id = f"EVD-{int(time.time())}"

    return jsonify({
        "evidenceId": evidence_id,
        "hash": sha256[:32] + "...",
        "status": "registered"
    })

# Verify Evidence API
@app.route("/api/verify", methods=["POST"])
def verify_evidence():
    file = request.files.get("file")
    expected_hash = request.form.get("hash")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    sha256 = hashlib.sha256(file.read()).hexdigest()

    return jsonify({
        "match": sha256.startswith(expected_hash[:20]),
        "calculatedHash": sha256[:32] + "..."
    })

if __name__ == "__main__":
    app.run(debug=True)
