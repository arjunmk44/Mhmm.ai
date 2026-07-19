"""
Gemini Extractor for multimodal and text document extraction.
"""

from typing import Dict, Any, Optional
from ai_ml.llm.model_router import model_router
from ai_ml.prompts.extraction_prompt import EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT
from ai_ml.utils.validators import validate_extraction_payload
from ai_ml.utils.logger import logger


class GeminiExtractor:

    def extract(
        self,
        text_content: str,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """
        Executes forced JSON extraction via LLM model router.
        """
        prompt = EXTRACTION_USER_PROMPT.format(document_text=text_content if text_content else "Visual/scanned industrial document.")
        
        raw_result = model_router.generate_extraction(
            prompt=prompt,
            system_instruction=EXTRACTION_SYSTEM_PROMPT,
            image_bytes=image_bytes,
            mime_type=mime_type
        )
        
        return validate_extraction_payload(raw_result)


gemini_extractor = GeminiExtractor()
