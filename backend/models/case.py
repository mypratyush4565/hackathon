import uuid
import datetime

class Case:
    def __init__(self, title, created_by):
        self.id = str(uuid.uuid4())
        self.title = title
        self.created_by = created_by
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.evidence_ids = []

    def add_evidence(self, evidence_id):
        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "evidence_ids": self.evidence_ids
        }
