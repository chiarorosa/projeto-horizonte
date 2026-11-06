"""Formatos de requisição e resposta (ai/README.md, seção "Integração")."""

from pydantic import BaseModel, Field


class ConsultaEntrada(BaseModel):
    pergunta: str = Field(min_length=1)
    documentos_autorizados: list[str] = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class Fonte(BaseModel):
    documento_id: str
    titulo: str
    trecho: str
    pagina: int | None
    score: float | None


class Uso(BaseModel):
    modelo: str
    tokens_entrada: int | None
    tokens_saida: int | None
    latencia_ms: int
    custo_usd: float | None


class ConsultaResposta(BaseModel):
    resposta: str
    fontes: list[Fonte]
    uso: Uso
