import datetime
import os

def extract_metadata(filename):
    name, ext = os.path.splitext(filename)

    return {
        "original_filename": filename,
        "extension": ext.lower(),
        "extracted_at": datetime.datetime.utcnow().isoformat(),
        "note": "Metadata extraction limited to demo-safe fields (hackathon scope)"
    }
