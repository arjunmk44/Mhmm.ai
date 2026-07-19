"""
Entity Extractor for parsing and filtering equipment, personnel, regulatory references, and parameters.
"""

from typing import Dict, Any, List
from ai_ml.utils.helpers import normalize_tag, extract_equipment_tags_regex


class EntityExtractor:

    def process_entities(self, raw_entities: Dict[str, Any], raw_text: str = "") -> Dict[str, Any]:
        """
        Processes and enriches extracted entity dictionary.
        """
        eq_tags = raw_entities.get("equipment_tags", [])
        regex_tags = extract_equipment_tags_regex(raw_text)
        
        # Merge LLM tags and regex tags
        all_tags = set([normalize_tag(t) for t in eq_tags if t] + regex_tags)
        
        return {
            "equipment_tags": sorted(list(all_tags)),
            "process_parameters": raw_entities.get("process_parameters", []),
            "regulatory_refs": raw_entities.get("regulatory_refs", []),
            "personnel": raw_entities.get("personnel", []),
            "dates": raw_entities.get("dates", [])
        }


entity_extractor = EntityExtractor()
