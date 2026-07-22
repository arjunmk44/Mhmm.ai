"""
Client for interacting with Google Gemini API (Gemini 2.5 Flash).
Supports text, multimodal (images/PDFs), and structured JSON output.
"""

import os
import socket
from typing import Optional, Union, Dict, Any, List
from ai_ml.config.settings import settings
from ai_ml.utils.logger import logger
from ai_ml.utils.helpers import parse_json_safely

try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False

# Ensure IPv4 socket preference for dual-stack Linux containers
try:
    _old_getaddrinfo = socket.getaddrinfo
    def _ipv4_first_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        res = _old_getaddrinfo(host, port, family, type, proto, flags)
        return sorted(res, key=lambda x: 0 if x[0] == socket.AF_INET else 1)
    socket.getaddrinfo = _ipv4_first_getaddrinfo
except Exception:
    pass


class GeminiClient:

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL
        self.client = None

        if HAS_GENAI_SDK and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Gemini client initialized with model '{self.model}'")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.2) -> str:
        if not self.is_available():
            raise RuntimeError("Gemini API key not configured or SDK unavailable.")

        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction if system_instruction else None,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Error calling Gemini generate_text: {e}")
            raise RuntimeError(f"Gemini API error: {e}") from e

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Gemini API key not configured or SDK unavailable.")

        try:
            config = types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                system_instruction=system_instruction if system_instruction else None,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            return parse_json_safely(response.text or "{}")
        except Exception as e:
            logger.warning(f"Gemini forced JSON failed, retrying standard generation: {e}")
            raw_text = self.generate_text(prompt, system_instruction=system_instruction, temperature=0.1)
            return parse_json_safely(raw_text)

    def generate_multimodal(self, prompt: str, image_bytes: bytes, mime_type: str = "image/jpeg", system_instruction: Optional[str] = None) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Gemini API key not configured or SDK unavailable.")

        try:
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            )
            config = types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                system_instruction=system_instruction if system_instruction else None,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image_part],
                config=config,
            )
            return parse_json_safely(response.text or "{}")
        except Exception as e:
            logger.error(f"Gemini multimodal generation failed: {e}")
            raise RuntimeError(f"Gemini Multimodal error: {e}") from e
