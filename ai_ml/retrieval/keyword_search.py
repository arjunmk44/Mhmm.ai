"""
Keyword Search module for exact tag and equipment identifier match fallback.
"""

from typing import List, Dict, Any
from ai_ml.embeddings.vector_store import vector_store
from ai_ml.utils.helpers import extract_equipment_tags_regex


class KeywordSearch:

    def search(self, query_text: str) -> List[Dict[str, Any]]:
        """
        Executes exact keyword tag matching against stored chunks.
        """
        tags = extract_equipment_tags_regex(query_text)
        if not tags:
            return []

        results = []
        for chunk in vector_store.memory_store:
            chunk_text = chunk.get("chunk_text", "")
            chunk_tags = chunk.get("equipment_tags", [])

            for t in tags:
                if t in chunk_tags or t in chunk_text.upper():
                    results.append({
                        "type": "keyword",
                        "doc_id": chunk.get("document_id"),
                        "chunk_id": chunk.get("chunk_id"),
                        "text": chunk_text,
                        "score": 0.95,
                        "source": f"Exact Tag Match ({t})"
                    })
                    break

        return results[:5]


keyword_search = KeywordSearch()
