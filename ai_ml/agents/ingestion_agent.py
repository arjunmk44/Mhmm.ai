"""
LangGraph Ingestion Agent for end-to-end document processing.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from ai_ml.agents.state import IngestionState
from ai_ml.ingestion.loader import document_loader
from ai_ml.ingestion.chunking import text_chunker
from ai_ml.extraction.gemini_extractor import gemini_extractor
from ai_ml.embeddings.embedding_model import embedding_model
from ai_ml.embeddings.vector_store import vector_store
from ai_ml.graph.graph_builder import graph_builder
from ai_ml.utils.helpers import generate_document_id
from ai_ml.utils.logger import logger


def node_load_document(state: IngestionState) -> Dict[str, Any]:
    file_bytes = state["file_content"]
    filename = state["filename"]
    doc_id = state.get("document_id") or generate_document_id(filename, file_bytes)

    text, img_bytes, mtype = document_loader.load(file_bytes, filename)
    return {
        "document_id": doc_id,
        "extracted_text": text,
        "image_bytes": img_bytes,
        "mime_type": mtype,
        "status": "loaded"
    }


def node_extract_knowledge(state: IngestionState) -> Dict[str, Any]:
    text = state.get("extracted_text", "")
    img_bytes = state.get("image_bytes")
    mtype = state.get("mime_type", "image/jpeg")

    extraction = gemini_extractor.extract(text, image_bytes=img_bytes, mime_type=mtype)
    return {
        "document_type": extraction.get("document_type", "project_file"),
        "extraction_payload": extraction,
        "status": "extracted"
    }


def node_write_graph(state: IngestionState) -> Dict[str, Any]:
    doc_id = state["document_id"]
    filename = state["filename"]
    extraction = state["extraction_payload"]

    count = graph_builder.build_graph(doc_id, filename, extraction)
    return {
        "graph_elements_count": count,
        "status": "graph_updated"
    }


def node_embed_and_index(state: IngestionState) -> Dict[str, Any]:
    text = state.get("extracted_text", "")
    doc_id = state["document_id"]
    meta = state.get("metadata", {})

    if text and text.strip():
        chunks = text_chunker.chunk_document(text, doc_id, meta)
        chunk_texts = [c["text"] for c in chunks]
        embeddings = embedding_model.embed_documents(chunk_texts)
        vector_store.add_chunks(chunks, embeddings)
        return {
            "chunks": chunks,
            "embeddings": embeddings,
            "status": "completed"
        }
    return {"status": "completed"}


def build_ingestion_graph():
    workflow = StateGraph(IngestionState)
    
    workflow.add_node("load_document", node_load_document)
    workflow.add_node("extract_knowledge", node_extract_knowledge)
    workflow.add_node("write_graph", node_write_graph)
    workflow.add_node("embed_and_index", node_embed_and_index)

    workflow.set_entry_point("load_document")
    workflow.add_edge("load_document", "extract_knowledge")
    workflow.add_edge("extract_knowledge", "write_graph")
    workflow.add_edge("write_graph", "embed_and_index")
    workflow.add_edge("embed_and_index", END)

    return workflow.compile()


ingestion_agent_executor = build_ingestion_graph()
