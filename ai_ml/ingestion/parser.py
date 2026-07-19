"""
Industrial document parser for extracting metadata, sections, and preliminary tags.
"""

from typing import Dict, Any, List
from ai_ml.utils.helpers import extract_equipment_tags_regex, normalize_tag


class DocumentParser:

    def parse_structure(self, raw_text: str, filename: str) -> Dict[str, Any]:
        """
        Parses raw document text into structured sections and tags.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        
        # Pre-extract equipment tags using regex
        tags = extract_equipment_tags_regex(raw_text)
        
        # Detect basic document category hints
        lower_fn = filename.lower()
        hint_type = "project_file"
        if any(w in lower_fn for w in ["maint", "work-order", "wo", "repair"]):
            hint_type = "maintenance_record"
        elif any(w in lower_fn for w in ["inspect", "audit", "ncr", "checklist"]):
            hint_type = "inspection_report"
        elif any(w in lower_fn for w in ["sop", "safety", "hazard", "procedure"]):
            hint_type = "safety_procedure"
        elif any(w in lower_fn for w in ["pnid", "p&id", "drawing", "schematic"]):
            hint_type = "pnid"
        elif any(w in lower_fn for w in ["manual", "operating", "instruction"]):
            hint_type = "operating_instruction"

        return {
            "filename": filename,
            "hint_document_type": hint_type,
            "extracted_tags": tags,
            "line_count": len(lines),
            "char_count": len(raw_text),
            "head_snippet": raw_text[:500] if raw_text else ""
        }


document_parser = DocumentParser()
