import json
import os
import datetime
import uuid

CUSTODY_LOG_PATH = "backend/storage/custody_log.json"

def _load_log():
    if not os.path.exists(CUSTODY_LOG_PATH):
        return []
    with open(CUSTODY_LOG_PATH, "r") as f:
        return json.load(f)

def _save_log(log):
    with open(CUSTODY_LOG_PATH, "w") as f:
        json.dump(log, f, indent=4)

def log_custody_action(evidence_id, action, actor):
    log = _load_log()

    entry = {
        "entry_id": str(uuid.uuid4()),
        "evidence_id": evidence_id,
        "action": action,
        "actor": actor,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    log.append(entry)
    _save_log(log)
    return entry

def get_custody_timeline(evidence_id):
    log = _load_log()
    return [e for e in log if e["evidence_id"] == evidence_id]
