"""
Embedding model wrapper for sentence-transformers/all-MiniLM-L6-v2.
Provides 384-dimensional dense vector embeddings with fallback handling.
"""

from typing import List
import numpy as np
from ai_ml.config.settings import settings
from ai_ml.config.constants import EMBEDDING_DIMENSION
from ai_ml.utils.logger import logger

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


class EmbeddingModel:

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.model = None
        self._load_attempted = False

    def _get_model(self):
        if self.model is None and not self._load_attempted:
            self._load_attempted = True
            if HAS_SENTENCE_TRANSFORMERS:
                try:
                    logger.info(f"Loading SentenceTransformer model '{self.model_name}'...")
                    self.model = SentenceTransformer(self.model_name)
                except Exception as e:
                    logger.warning(f"Could not load SentenceTransformer model '{self.model_name}': {e}")
        return self.model

    def embed_text(self, text: str) -> List[float]:
        """Generates 384-dim embedding vector for single string."""
        if not text or not text.strip():
            return [0.0] * EMBEDDING_DIMENSION

        model = self._get_model()
        if model is not None:
            try:
                vec = self.model.encode(text, convert_to_numpy=True)
                return vec.tolist()
            except Exception as e:
                logger.error(f"Error generating embedding with SentenceTransformer: {e}")

        # Fallback deterministic pseudo-embedding based on hash string
        return self._fallback_pseudo_embedding(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generates batch embeddings."""
        if not texts:
            return []

        if self.model is not None:
            try:
                vecs = self.model.encode(texts, convert_to_numpy=True)
                return vecs.tolist()
            except Exception as e:
                logger.error(f"Error generating batch embeddings: {e}")

        return [self.embed_text(t) for t in texts]

    def _fallback_pseudo_embedding(self, text: str) -> List[float]:
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(EMBEDDING_DIMENSION)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()


embedding_model = EmbeddingModel()
