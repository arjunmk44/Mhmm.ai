"""
Configuration settings for AI/ML module using Pydantic Settings.
Reads environment variables with sensible defaults and fallbacks.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ai_ml.config.constants import (
    DEFAULT_GEMINI_MODEL,
    DEFAULT_GROQ_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)


class AISettings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = Field(default="")
    GROQ_API_KEY: str = Field(default="")

    # Neo4j Settings
    NEO4J_URI: str = Field(default="bolt://localhost:7687")
    NEO4J_USERNAME: str = Field(default="neo4j")
    NEO4J_PASSWORD: str = Field(default="password")
    NEO4J_USER: str = Field(default="neo4j")

    # PostgreSQL / Vector Store Settings
    DATABASE_URL: str = Field(default="postgresql://app:app@localhost:5432/knowledge_platform")
    SUPABASE_URL: str = Field(default="")
    SUPABASE_KEY: str = Field(default="")

    # Model Settings
    GEMINI_MODEL: str = Field(default=DEFAULT_GEMINI_MODEL)
    GROQ_MODEL: str = Field(default=DEFAULT_GROQ_MODEL)
    EMBEDDING_MODEL_NAME: str = Field(default=DEFAULT_EMBEDDING_MODEL)
    EMBEDDING_DIM: int = EMBEDDING_DIMENSION

    # Operational Modes
    ALLOW_MOCK_FALLBACK: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def neo4j_effective_user(self) -> str:
        """Returns username checking both NEO4J_USERNAME and NEO4J_USER."""
        if self.NEO4J_USERNAME and self.NEO4J_USERNAME != "neo4j":
            return self.NEO4J_USERNAME
        if self.NEO4J_USER:
            return self.NEO4J_USER
        return "neo4j"


settings = AISettings()
