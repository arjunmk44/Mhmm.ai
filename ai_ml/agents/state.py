"""
LangGraph State definitions for Ingestion Agent and Failure Intelligence Agent.
"""

from typing import TypedDict, List, Dict, Any, Optional


class IngestionState(TypedDict):
    file_content: bytes
    filename: str
    metadata: Dict[str, Any]
    document_id: str
    extracted_text: str
    image_bytes: Optional[bytes]
    mime_type: str
    document_type: str
    extraction_payload: Dict[str, Any]
    chunks: List[Dict[str, Any]]
    embeddings: List[List[float]]
    graph_elements_count: int
    status: str
    error: Optional[str]


class FailureScanState(TypedDict):
    equipment_id: Optional[str]
    graph_context: Dict[str, Any]
    historical_records: List[Dict[str, Any]]
    analysis_payload: Dict[str, Any]
    risk_level: str
    potential_failures: List[Dict[str, Any]]
    recommendations: List[str]
    alerts: List[Dict[str, Any]]
    error: Optional[str]
