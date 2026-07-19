"""
Exposed interface exports for AI/ML module backend consumption.
"""

from ai_ml.interfaces.ingestion_interface import ingest_document
from ai_ml.interfaces.query_interface import query_knowledge
from ai_ml.interfaces.graph_interface import get_graph_neighborhood, run_failure_scan

__all__ = [
    "ingest_document",
    "query_knowledge",
    "get_graph_neighborhood",
    "run_failure_scan",
]
