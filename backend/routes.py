from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate(req: DocumentRequest):
    try:
        text = generator.generate_document(
            req.document_type, req.parties, req.terms, req.dates
        )
        return {"document": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))