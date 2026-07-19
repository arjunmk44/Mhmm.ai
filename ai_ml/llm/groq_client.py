"""
Client for interacting with Groq API (Llama 3.3 70B / Llama 3.1 8B).
Acts as a backup LLM provider when Gemini quota or rate limits are hit.
"""

from typing import Optional, Dict, Any
from ai_ml.config.settings import settings
from ai_ml.utils.logger import logger
from ai_ml.utils.helpers import parse_json_safely

try:
    from groq import Groq
    HAS_GROQ_SDK = True
except ImportError:
    HAS_GROQ_SDK = False


class GroqClient:

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.client = None

        if HAS_GROQ_SDK and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info(f"Groq client initialized with model '{self.model}'")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.2) -> str:
        if not self.is_available():
            raise RuntimeError("Groq API key not configured or SDK unavailable.")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Error calling Groq generate_text: {e}")
            raise RuntimeError(f"Groq API error: {e}") from e

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Groq API key not configured or SDK unavailable.")

        sys_prompt = (system_instruction or "") + "\nRespond ONLY with valid JSON."
        raw_text = self.generate_text(prompt, system_instruction=sys_prompt, temperature=0.1)
        return parse_json_safely(raw_text)
