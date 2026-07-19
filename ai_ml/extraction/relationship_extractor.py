"""
Relationship Extractor for structuring knowledge graph edges.
"""

from typing import List, Dict, Any
from ai_ml.config.constants import VALID_RELATIONSHIP_TYPES, REL_MENTIONED_IN
from ai_ml.utils.helpers import normalize_tag


class RelationshipExtractor:

    def normalize_relationships(self, raw_relationships: List[Dict[str, Any]], doc_id: str = "") -> List[Dict[str, Any]]:
        """
        Normalizes and formats relationship edges for Neo4j consumption.
        """
        formatted = []
        for rel in raw_relationships:
            src = rel.get("from") or rel.get("source_id") or rel.get("source")
            tgt = rel.get("to") or rel.get("target_id") or rel.get("target")
            rel_type = (rel.get("type") or rel.get("relation_type") or REL_MENTIONED_IN).upper()

            if not src or not tgt:
                continue

            if rel_type not in VALID_RELATIONSHIP_TYPES:
                rel_type = REL_MENTIONED_IN

            formatted.append({
                "source": normalize_tag(str(src)),
                "target": normalize_tag(str(tgt)),
                "type": rel_type,
                "document_id": doc_id
            })

        return formatted


relationship_extractor = RelationshipExtractor()
