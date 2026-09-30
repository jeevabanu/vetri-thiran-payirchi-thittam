import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.4"))
    MAX_OUTPUT_TOKENS: int = int(os.getenv("MAX_OUTPUT_TOKENS", "4096"))

    # App
    APP_NAME: str = "LegalEase"
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "120"))

    # Limits
    MAX_TERMS_LENGTH: int = 5000
    MAX_LOGO_MB: int = 2

    # Supported document types (shown in the Streamlit dropdown)
    DOCUMENT_TYPES: tuple = (
        "Employment Contract",
        "Non-Disclosure Agreement",
        "Residential Lease Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "Freelance Contract",
    )

    def validate(self) -> None:
        """Call once at startup to fail early with a clear message."""
        if not self.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )


settings = Settings()