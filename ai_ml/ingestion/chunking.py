"""
Text chunking module using RecursiveCharacterTextSplitter with tag context preservation.
"""

from typing import List, Dict, Any

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        class RecursiveCharacterTextSplitter:
            def __init__(self, chunk_size=500, chunk_overlap=100, **kwargs):
                self.chunk_size = chunk_size
                self.chunk_overlap = chunk_overlap
            def split_text(self, text: str) -> List[str]:
                chunks = []
                step = max(1, self.chunk_size - self.chunk_overlap)
                for i in range(0, len(text), step):
                    chunks.append(text[i:i+self.chunk_size])
                return chunks

from ai_ml.utils.helpers import generate_chunk_id, extract_equipment_tags_regex


class TextChunker:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "; ", " ", ""]
        )

    def chunk_document(self, text: str, document_id: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Splits text into chunks enriched with metadata and equipment tags.
        """
        if not text or not text.strip():
            return []

        raw_chunks = self.splitter.split_text(text)
        chunks = []

        for idx, chunk_text in enumerate(raw_chunks):
            chunk_tags = extract_equipment_tags_regex(chunk_text)
            c_id = generate_chunk_id(document_id, idx)
            chunks.append({
                "chunk_id": c_id,
                "document_id": document_id,
                "chunk_index": idx,
                "text": chunk_text,
                "equipment_tags": chunk_tags,
                "metadata": metadata or {}
            })

        return chunks


text_chunker = TextChunker()
