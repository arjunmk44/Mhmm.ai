"""
Model Router for dispatching LLM tasks with fallback redundancy.
Routes between Gemini 2.5 Flash, Groq Llama 3.3 70B, and a deterministic offline fallback.
"""

from typing import Optional, Dict, Any
from ai_ml.llm.gemini_client import GeminiClient
from ai_ml.llm.groq_client import GroqClient
from ai_ml.utils.logger import logger
from ai_ml.utils.helpers import extract_equipment_tags_regex


class ModelRouter:

    def __init__(self):
        self.gemini = GeminiClient()
        self.groq = GroqClient()

    def generate_extraction(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """
        Attempts extraction via Gemini Flash (multimodal if image_bytes provided).
        Falls back to Groq if text-only, or mock fallback if offline.
        """
        # 1. Try Gemini
        if self.gemini.is_available():
            try:
                if image_bytes:
                    logger.info("Attempting multimodal extraction with Gemini 2.5 Flash...")
                    return self.gemini.generate_multimodal(prompt, image_bytes, mime_type, system_instruction)
                else:
                    logger.info("Attempting extraction with Gemini 2.5 Flash...")
                    return self.gemini.generate_json(prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Gemini extraction failed: {e}. Falling back...")

        # 2. Try Groq (text only)
        if not image_bytes and self.groq.is_available():
            try:
                logger.info("Attempting fallback extraction with Groq Llama 3.3 70B...")
                return self.groq.generate_json(prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Groq extraction failed: {e}. Falling back to rule-based fallback.")

        # 3. Deterministic Mock Fallback
        logger.info("Using rule-based offline fallback extraction engine.")
        return self._rule_based_fallback_extraction(prompt)

    def generate_synthesis(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Attempts query answer synthesis via Gemini Flash, fallback to Groq, fallback to rule engine.
        """
        # 1. Try Gemini
        if self.gemini.is_available():
            try:
                return self.gemini.generate_text(prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Gemini synthesis failed: {e}")

        # 2. Try Groq
        if self.groq.is_available():
            try:
                return self.groq.generate_text(prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Groq synthesis failed: {e}")

        # 3. Offline Fallback
        logger.info("Using rule-based offline synthesis engine.")
        return f"Synthesized knowledge response based on context:\n{prompt[:300]}..."

    def _rule_based_fallback_extraction(self, prompt: str) -> Dict[str, Any]:
        tags = extract_equipment_tags_regex(prompt)
        doc_type = "maintenance_record"
        if "inspection" in prompt.lower():
            doc_type = "inspection_report"
        elif "safety" in prompt.lower() or "procedure" in prompt.lower():
            doc_type = "safety_procedure"
        elif "drawing" in prompt.lower() or "p&id" in prompt.lower() or "diagram" in prompt.lower():
            doc_type = "pnid"

        relationships = []
        if len(tags) >= 2:
            relationships.append({
                "from": tags[0],
                "to": tags[1],
                "type": "CONNECTED_TO"
            })

        return {
            "document_type": doc_type,
            "entities": {
                "equipment_tags": tags if tags else ["TAG-101"],
                "process_parameters": [{"name": "Pressure", "value": "15.2", "unit": "bar"}],
                "regulatory_refs": ["OSHA-1910"],
                "personnel": ["Maintenance Staff"],
                "dates": ["2026-07-14"]
            },
            "relationships": relationships,
            "summary": "Extracted industrial document details and equipment references."
        }


model_router = ModelRouter()
