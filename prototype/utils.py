import hashlib
import datetime

def generate_hash(file_bytes):
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()

def calculate_pre_entry_risk(source_type, capture_time):
    """
    Very simple & explainable risk logic for Round 1
    """
    source_type = source_type.lower()

    if source_type in ["cctv", "bodycam", "official"]:
        return "LOW"
    elif source_type in ["dashcam"]:
        return "MEDIUM"
    elif source_type in ["mobile", "phone"]:
        return "HIGH"
    else:
        return "VERY HIGH"
