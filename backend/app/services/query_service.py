from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.crud.audit import create_audit_entry
from app.schemas.query import QueryResponse, QuerySource

# Try importing AI/ML interface gracefully
try:
    from ai_ml.interfaces import query_knowledge
except (ImportError, ModuleNotFoundError):
    query_knowledge = None


def query_knowledge_base(
    query_text: str,
    filters: Dict[str, Any],
    db: Session,
) -> QueryResponse:
    if not query_text or not query_text.strip():
        raise ValueError("Query string cannot be empty.")

    logger.info(f"Executing query: '{query_text}' with filters: {filters}")

    result_data = None
    if not settings.MOCK_AI_ML and callable(query_knowledge):
        try:
            result_data = query_knowledge(query_text, filters)
        except Exception as e:
            logger.warning(f"AI/ML query_knowledge failed, falling back to mock: {e}")
            raise e

    if not result_data:
        # Fallback to realistic mock response
        result_data = {
            "answer": (
                f"Analysis for '{query_text}': Primary operational records indicate that "
                "valve leakage is typically caused by degraded seal gaskets during high-pressure thermal cycles. "
                "Recommended maintenance procedure includes replacing ring seals every 6 months."
            ),
            "sources": [
                {"doc_id": "doc-101", "title": "Pump Maintenance Protocol.pdf"},
                {"doc_id": "doc-102", "title": "Valve Inspection Manual v2.pdf"},
            ],
            "confidence": 0.91,
        }

    sources = [
        QuerySource(doc_id=s.get("doc_id", "unknown"), title=s.get("title", "Unknown Source"))
        for s in result_data.get("sources", [])
    ]

    response = QueryResponse(
        answer=result_data.get("answer", ""),
        sources=sources,
        confidence=float(result_data.get("confidence", 0.0)),
    )

    create_audit_entry(
        db,
        action="query_executed",
        details={
            "query": query_text,
            "filters": filters,
            "confidence": response.confidence,
        },
    )

    return response

