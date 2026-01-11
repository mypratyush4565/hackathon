from datetime import datetime

def time_anchor(evidence_hash):
    # Simple UTC timestamp anchor
    anchor_record = {
        'hash': evidence_hash,
        'time': datetime.utcnow().isoformat()
    }
    return anchor_record
