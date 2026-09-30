import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiDocumentGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    @staticmethod
    def build_prompt(document_type, parties, terms, dates) -> str:
        return f"""You are an expert legal drafter. Draft a professional {document_type}.

Parties involved: {parties}
Key terms and conditions: {terms}
Effective date / dates: {dates}

Requirements:
- Use a clear title, numbered sections and formal legal language.
- Include standard clauses (definitions, obligations, confidentiality,
  termination, governing law, signatures) that fit this document type.
- Use the given parties, terms and dates exactly; do not invent facts.
- Plain text only, no markdown symbols such as ** or #.
- Put each key term on its own line as 'Term: Value' in a
  section called 'KEY TERMS' so it can be converted into a table.
"""

    def generate_document(self, document_type, parties, terms, dates) -> str:
        prompt = self.build_prompt(document_type, parties, terms, dates)
        response = self.model.generate_content(prompt)
        return response.text.strip()