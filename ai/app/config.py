from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variáveis de ambiente do serviço de IA, lidas do .env da raiz do repositório."""

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    ai_port: int = 8001
    openrouter_api_key: SecretStr = SecretStr("")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = ""
    embedding_provider: Literal["local", "openrouter"] = "local"
    # Modelo local multilíngue (os documentos estão em português), 384 dimensões.
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    database_url: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
