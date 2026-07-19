"""
Unit and integration tests for document ingestion interface.
"""

import pytest
from ai_ml.interfaces.ingestion_interface import ingest_document

SAMPLE_MAINTENANCE_TEXT = """
MAINTENANCE REPORT
Date: 2026-07-14
Equipment Tag: PUMP-101A
Location: Unit 4 Refectory
Inspector: John Doe

Summary:
Centrifugal pump PUMP-101A exhibited high vibration readings during routine operation.
Inspected bearing assembly and replaced damaged seals. Upstream isolation valve V-204 was closed during procedure.
Operating pressure restored to 15.2 bar. Adhered to safety standard OSHA-1910.
"""


def test_ingest_document_success():
    content = SAMPLE_MAINTENANCE_TEXT.encode("utf-8")
    meta = {"filename": "maintenance_pump_101a.txt", "author": "John Doe"}

    result = ingest_document(content, meta)

    assert result["status"] == "success"
    assert "document_id" in result
    assert result["entities_extracted"] >= 1


def test_ingest_document_invalid_empty():
    with pytest.raises(ValueError):
        ingest_document(b"", {"filename": "empty.txt"})
