# ingest/validators.py

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv"}
ALLOWED_ROLES = {"hr", "it", "staff", "general"}
ALLOWED_ACCESS_LEVELS = {"public", "internal", "sensitive"}


def validate_files(files):
    errors = []

    for f in files:
        name = f.name.lower()
        if not any(name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            errors.append(f"- File `{f.name}` không hỗ trợ.")

    return errors


def validate_role(role: str) -> bool:
    return role in ALLOWED_ROLES


def validate_access_level(level: str) -> bool:
    return level in ALLOWED_ACCESS_LEVELS

