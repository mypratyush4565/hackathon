import uuid
from datetime import datetime

class Evidence:
    def __init__(self, file_name, uploader, source_type, metadata=None, parent_hash=None):
        self.id = str(uuid.uuid4())
        self.file_name = file_name
        self.uploader = uploader
        self.source_type = source_type
        self.metadata = metadata or {}
        self.metadata['timestamp'] = datetime.utcnow().isoformat()
        self.parent_hash = parent_hash
        self.hash = None
        self.admissibility_score = None

    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'uploader': self.uploader,
            'source_type': self.source_type,
            'metadata': self.metadata,
            'parent_hash': self.parent_hash,
            'hash': self.hash,
            'admissibility_score': self.admissibility_score
        }
