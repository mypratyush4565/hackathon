import hashlib
import json
import os
from datetime import datetime

STORE_PATH = "prototype/evidence_store/metadata.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_metadata():
    if not os.path.exists(STORE_PATH):
        return {}
    with open(STORE_PATH, "r") as f:
        return json.load(f)


def save_metadata(data):
    with open(STORE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def register_evidence(evidence_id, file_path, source_type, uploader_claim):
    hash_value = calculate_hash(file_path)
    metadata = load_metadata()

    metadata[evidence_id] = {
        "hash": hash_value,
        "source_type": source_type,
        "uploader_claim": uploader_claim,
        "registered_at": datetime.utcnow().isoformat()
    }

    save_metadata(metadata)
    return hash_value


def verify_evidence(evidence_id, file_path):
    metadata = load_metadata()

    if evidence_id not in metadata:
        return False, "Evidence ID not found"

    current_hash = calculate_hash(file_path)
    stored_hash = metadata[evidence_id]["hash"]

    if current_hash == stored_hash:
        return True, "Integrity intact"
    else:
        return False, "Integrity compromised"
