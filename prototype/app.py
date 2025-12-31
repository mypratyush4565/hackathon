from flask import Flask, request, jsonify, render_template
from utils import generate_hash, calculate_pre_entry_risk

app = Flask(__name__)
EVIDENCE_DB = {}

@app.route("/")
def home():
    return render_template("frontend.html")

@app.route("/register", methods=["POST"])
def register_evidence():
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")
    source_type = request.form.get("source_type")
    uploader_claim = request.form.get("uploader_claim")

    if not file or not evidence_id:
        return jsonify({"error": "Missing file or evidence ID"}), 400

    file_bytes = file.read()
    file_hash = generate_hash(file_bytes)
    risk = calculate_pre_entry_risk(source_type, None)

    EVIDENCE_DB[evidence_id] = {
        "hash": file_hash,
        "source_type": source_type,
        "uploader_claim": uploader_claim,
        "risk": risk
    }

    return jsonify({
        "message": "Evidence registered successfully",
        "evidence_id": evidence_id,
        "hash": file_hash,
        "pre_entry_risk": risk
    })

@app.route("/verify", methods=["POST"])
def verify_evidence():
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")

    if not file:
        return jsonify({"error": "File missing"}), 400

    if evidence_id not in EVIDENCE_DB:
        return jsonify({"error": "Evidence ID not found"}), 404

    file_bytes = file.read()
    new_hash = generate_hash(file_bytes)
    original_hash = EVIDENCE_DB[evidence_id]["hash"]

    status = "INTACT" if new_hash == original_hash else "TAMPERED"

    return jsonify({
        "evidence_id": evidence_id,
        "integrity_status": status,
        "stored_hash": original_hash,
        "current_hash": new_hash,
        "risk_note": EVIDENCE_DB[evidence_id]["risk"]
    })

if __name__ == "__main__":
    app.run(debug=True)
