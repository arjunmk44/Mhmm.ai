"""
Query interface exposed to the Backend API per Section 4 of the Integration Contract.
"""

from typing import Dict, Any, Optional
from ai_ml.retrieval.hybrid_retriever import hybrid_retriever
from ai_ml.utils.logger import logger


def query_knowledge(query_text: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Submits a natural language query against the hybrid vector + graph knowledge base.

    Inputs:
        query_text: Natural language search string.
        filters: Optional filter dictionary (e.g. date ranges, document types).

    Outputs:
        { "answer": "text", "sources": [...], "confidence": float }

    Raises:
        ValueError: If query_text is empty.
        TimeoutError: If execution exceeds timeout limits.
    """
    if not query_text or not query_text.strip():
        raise ValueError("Invalid query: query_text cannot be empty.")

    try:
        return hybrid_retriever.retrieve_and_answer(query_text, filters)
    except Exception as e:
        logger.error(f"Query execution failed for '{query_text}': {e}")
        raise RuntimeError(f"Query knowledge error: {e}") from e
