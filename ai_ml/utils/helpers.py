"""
Helper functions for text parsing, JSON extraction, entity normalization, and hashing.
"""

import json
import re
import uuid
import hashlib
from typing import Dict, Any, List, Optional


def clean_json_markdown(content: str) -> str:
    """
    Extracts raw JSON string from LLM responses that may be wrapped in ```json ... ``` blocks.
    """
    if not content:
        return "{}"
    
    cleaned = content.strip()
    
    # Remove markdown code fence blocks if present
    if "```" in cleaned:
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()
        else:
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    return cleaned


def parse_json_safely(content: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Safely parses JSON content, returning a default dictionary if parsing fails.
    """
    if default is None:
        default = {}
        
    cleaned = clean_json_markdown(content)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
        return default
    except json.JSONDecodeError:
        # Try finding the first '{' and last '}'
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start:end+1])
            except json.JSONDecodeError:
                pass
        return default


def generate_document_id(filename: str, content_bytes: bytes) -> str:
    """Generates a reproducible UUID v5 based on filename and content SHA256 hash."""
    content_hash = hashlib.sha256(content_bytes).hexdigest()
    namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # URL namespace
    return str(uuid.uuid5(namespace, f"{filename}:{content_hash}"))


def generate_chunk_id(doc_id: str, chunk_index: int) -> str:
    """Generates a UUID string for a document chunk."""
    return f"chunk-{doc_id[:8]}-{chunk_index:04d}"


def normalize_tag(tag: str) -> str:
    """
    Normalizes equipment tags (e.g. 'Pump-101-A' -> 'PUMP-101A').
    Removes extraneous hyphens/spaces and converts to uppercase.
    """
    if not tag:
        return ""
    tag_clean = tag.strip().upper()
    # Normalize internal spaces and trailing/leading symbols
    tag_clean = re.sub(r"\s+", "-", tag_clean)
    tag_clean = re.sub(r"-+", "-", tag_clean)
    return tag_clean


def extract_equipment_tags_regex(text: str) -> List[str]:
    """
    Uses regex patterns common in industrial assets (e.g., P-101, V-204B, E-301, HX-402, TK-500)
    to identify potential equipment tag identifiers in text.
    """
    if not text:
        return []
    
    # Common industrial tag prefixes: P, V, E, TK, HX, HE, CV, FE, PT, TT, LT, TE, FT, PIC, TIC, LIC
    pattern = r"\b(?:[A-Z]{1,4})[-_ ]?\d{2,4}[A-Z]?\b"
    raw_tags = re.findall(pattern, text)
    
    normalized = list(set([normalize_tag(t) for t in raw_tags if len(t) >= 3]))
    return sorted(normalized)
