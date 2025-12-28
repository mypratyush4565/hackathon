from flask import Flask, request, jsonify
import os
from utils import register_evidence, verify_evidence

app = Flask(__name__)
UPLOAD_FOLDER = "prototype/evidence_store"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/register", methods=["POST"])
def register():
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")
    source_type = request.form.get("source_type")
    uploader_claim = request.form.get("uploader_claim")

    if not all([file, evidence_id, source_type, uploader_claim]):
        return jsonify({"error": "Missing required fields"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    hash_value = register_evidence(
        evidence_id,
        file_path,
        source_type,
        uploader_claim
    )

    return jsonify({
        "message": "Evidence registered successfully",
        "evidence_id": evidence_id,
        "hash": hash_value,
        "legal_strength": source_type
    })


@app.route("/verify", methods=["POST"])
def verify():
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")

    if not all([file, evidence_id]):
        return jsonify({"error": "Missing required fields"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, "temp_verify")
    file.save(file_path)

    status, message = verify_evidence(evidence_id, file_path)
    os.remove(file_path)

    return jsonify({
        "evidence_id": evidence_id,
        "status": status,
        "message": message
    })


if __name__ == "__main__":
    app.run(debug=True)
