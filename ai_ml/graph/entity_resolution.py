"""
Entity Resolution module for fuzzy-matching and deduplicating equipment tags and nodes.
"""

from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
from ai_ml.config.constants import FUZZY_MATCH_THRESHOLD
from ai_ml.utils.helpers import normalize_tag


class EntityResolver:

    def __init__(self, threshold: float = FUZZY_MATCH_THRESHOLD):
        self.threshold = threshold

    def resolve_tag(self, tag: str, existing_tags: List[str]) -> str:
        """
        Matches an incoming tag against existing tags.
        If fuzzy similarity >= threshold, returns the canonical existing tag.
        Otherwise returns the normalized tag.
        """
        norm_tag = normalize_tag(tag)
        if not norm_tag:
            return ""

        for existing in existing_tags:
            norm_existing = normalize_tag(existing)
            if norm_tag == norm_existing:
                return norm_existing
            
            sim = SequenceMatcher(None, norm_tag, norm_existing).ratio()
            if sim >= self.threshold:
                return norm_existing

        return norm_tag

    def deduplicate_tags(self, tags: List[str]) -> List[str]:
        """Deduplicates a list of tags by resolving fuzzy matches."""
        canonical: List[str] = []
        for tag in tags:
            resolved = self.resolve_tag(tag, canonical)
            if resolved not in canonical:
                canonical.append(resolved)
        return canonical


entity_resolver = EntityResolver()
