"""
Ingestion interface exposed to the Backend API per Section 4 of the Integration Contract.
"""

from typing import Dict, Any, Optional
from ai_ml.agents.ingestion_agent import ingestion_agent_executor
from ai_ml.utils.helpers import generate_document_id
from ai_ml.utils.logger import logger


def ingest_document(file_content: bytes, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ingests an industrial document, extracts entities/relationships, generates embeddings,
    and updates Neo4j and pgvector.

    Inputs:
        file_content: Raw bytes of the uploaded file.
        metadata: Dictionary containing 'filename' and optional document metadata.

    Outputs:
        { "status": "success", "document_id": "uuid", "entities_extracted": int }

    Raises:
        ValueError: If file_content or filename is missing/invalid.
        RuntimeError: If critical ingestion step fails.
    """
    if not file_content:
        raise ValueError("Invalid document: file_content cannot be empty.")

    filename = metadata.get("filename", "document.txt")
    doc_id = metadata.get("document_id") or generate_document_id(filename, file_content)

    initial_state = {
        "file_content": file_content,
        "filename": filename,
        "metadata": metadata,
        "document_id": doc_id,
        "extracted_text": "",
        "image_bytes": None,
        "mime_type": "text/plain",
        "document_type": "project_file",
        "extraction_payload": {},
        "chunks": [],
        "embeddings": [],
        "graph_elements_count": 0,
        "status": "pending",
        "error": None
    }

    try:
        final_state = ingestion_agent_executor.invoke(initial_state)
        extracted_payload = final_state.get("extraction_payload", {})
        eq_count = len(extracted_payload.get("entities", {}).get("equipment_tags", []))
        
        return {
            "status": "success",
            "document_id": final_state.get("document_id", doc_id),
            "entities_extracted": eq_count,
            "summary": extracted_payload.get("summary", "")
        }
    except Exception as e:
        logger.error(f"Ingestion failed for document '{filename}': {e}")
        raise RuntimeError(f"Ingestion failed: {e}") from e
