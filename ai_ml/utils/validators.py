"""
Validators for AI/ML module data schemas and extraction payloads.
"""

from typing import Dict, Any, List
from ai_ml.config.constants import SUPPORTED_DOCUMENT_TYPES, VALID_NODE_LABELS, VALID_RELATIONSHIP_TYPES


def validate_extraction_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes extraction result JSON structure to strictly conform to Section 1 & Section 8 specs.
    """
    if not isinstance(data, dict):
        data = {}

    doc_type = data.get("document_type", "project_file")
    if doc_type not in SUPPORTED_DOCUMENT_TYPES:
        doc_type = "project_file"

    entities = data.get("entities", {})
    if not isinstance(entities, dict):
        entities = {}

    eq_tags = entities.get("equipment_tags", [])
    if not isinstance(eq_tags, list):
        eq_tags = []

    proc_params = entities.get("process_parameters", [])
    if not isinstance(proc_params, list):
        proc_params = []

    reg_refs = entities.get("regulatory_refs", [])
    if not isinstance(reg_refs, list):
        reg_refs = []

    personnel = entities.get("personnel", [])
    if not isinstance(personnel, list):
        personnel = []

    dates = entities.get("dates", [])
    if not isinstance(dates, list):
        dates = []

    raw_relationships = data.get("relationships", [])
    if not isinstance(raw_relationships, list):
        raw_relationships = []

    valid_relationships = []
    for rel in raw_relationships:
        if isinstance(rel, dict):
            rel_from = rel.get("from") or rel.get("source_id") or rel.get("source")
            rel_to = rel.get("to") or rel.get("target_id") or rel.get("target")
            rel_type = rel.get("type") or rel.get("relation_type") or "MENTIONED_IN"
            if rel_from and rel_to:
                valid_relationships.append({
                    "from": str(rel_from),
                    "to": str(rel_to),
                    "type": str(rel_type).upper()
                })

    summary = data.get("summary", "Document processed.")

    return {
        "document_type": doc_type,
        "entities": {
            "equipment_tags": [str(t) for t in eq_tags if t],
            "process_parameters": proc_params,
            "regulatory_refs": [str(r) for r in reg_refs if r],
            "personnel": [str(p) for p in personnel if p],
            "dates": [str(d) for d in dates if d],
        },
        "relationships": valid_relationships,
        "summary": str(summary)
    }
