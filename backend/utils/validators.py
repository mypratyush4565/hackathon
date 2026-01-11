ALLOWED_EXTENSIONS = ['.jpg', '.png', '.mp4', '.wav', '.pdf']

def validate_file_extension(filename):
    ext = filename.lower().rsplit('.', 1)[-1]
    return f".{ext}" in ALLOWED_EXTENSIONS
