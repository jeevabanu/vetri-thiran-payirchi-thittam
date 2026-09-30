import os
import re
from datetime import date
from dotenv import load_dotenv

load_dotenv()


# ---------- Config ----------
def get_env(key: str, default: str | None = None) -> str:
    """Read an environment variable or raise a clear error if it's missing."""
    value = os.getenv(key, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing environment variable: {key}. Add it to your .env file.")
    return value


# ---------- Input validation ----------
def validate_inputs(document_type: str, parties: str, terms: str, dates: str) -> list[str]:
    """Return a list of error messages. Empty list means the input is valid."""
    errors = []
    if not document_type.strip():
        errors.append("Document type is required.")
    if not parties.strip():
        errors.append("Parties involved are required.")
    if not dates.strip():
        errors.append("Effective date is required.")
    if len(terms) > 5000:
        errors.append("Terms are too long (max 5000 characters).")
    return errors


def sanitize_text(text: str) -> str:
    """Trim whitespace and remove control characters from user input."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.strip()


# ---------- Cleaning AI output ----------
def clean_ai_output(text: str) -> str:
    """Remove markdown symbols the model may add (**, ##, ``` etc.)."""
    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "")
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------- Terms table ----------
def extract_terms(text: str) -> list[tuple[str, str]]:
    """Find 'Key: Value' lines and return them as (key, value) pairs."""
    rows = []
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() and value.strip() and len(key.strip()) <= 40:
                rows.append((key.strip(), value.strip()))
    return rows


# ---------- File helpers ----------
def safe_filename(doc_type: str, extension: str) -> str:
    """Example: 'Non-Disclosure Agreement' -> 'non_disclosure_agreement_2026-09-28.pdf'"""
    name = re.sub(r"[^a-zA-Z0-9]+", "_", doc_type.strip().lower()).strip("_") or "document"
    return f"{name}_{date.today().isoformat()}.{extension.lstrip('.')}"


def is_valid_logo(file_bytes: bytes, max_mb: int = 2) -> bool:
    """Check the logo is a real image and under the size limit."""
    from io import BytesIO
    from PIL import Image

    if not file_bytes or len(file_bytes) > max_mb * 1024 * 1024:
        return False
    try:
        Image.open(BytesIO(file_bytes)).verify()
        return True
    except Exception:
        return False


def latin1_safe(text: str) -> str:
    """fpdf's built-in fonts only support latin-1, so replace other characters."""
    replacements = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                    "\u2013": "-", "\u2014": "-", "\u2022": "-", "\u20b9": "Rs."}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")