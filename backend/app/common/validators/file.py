import os

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".csv", ".pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image_file(filename: str, content: bytes) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False
    if len(content) > MAX_FILE_SIZE:
        return False
    return True


def validate_document_file(filename: str, content: bytes) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        return False
    if len(content) > MAX_FILE_SIZE:
        return False
    return True
