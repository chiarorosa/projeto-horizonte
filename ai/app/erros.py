"""Formato de erro comum (backend/README.md, seção "Integração")."""

import logging
from typing import Any

import openai
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

log = logging.getLogger("horizonte.ai")


class AppError(Exception):
    """Erro esperado: raise AppError(404, "DOCUMENTO_NAO_INDEXADO", "...")."""

    def __init__(self, status: int, codigo: str, mensagem: str, detalhes: dict[str, Any] | None = None,
                 headers: dict[str, str] | None = None):
        super().__init__(mensagem)
        self.status, self.codigo, self.mensagem = status, codigo, mensagem
        self.detalhes, self.headers = detalhes or {}, headers


def resposta_erro(status: int, codigo: str, mensagem: str, detalhes: dict[str, Any] | None = None,
                  headers: dict[str, str] | None = None) -> JSONResponse:
    corpo = {"erro": {"codigo": codigo, "mensagem": mensagem, "detalhes": detalhes or {}}}
    return JSONResponse(corpo, status_code=status, headers=headers)


def registrar_tratadores(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error(_req: Request, exc: AppError):
        return resposta_erro(exc.status, exc.codigo, exc.mensagem, exc.detalhes, exc.headers)

    @app.exception_handler(RequestValidationError)
    async def validacao(_req: Request, exc: RequestValidationError):
        campos: dict[str, list[str]] = {}
        for e in exc.errors():
            nome = ".".join(str(p) for p in e["loc"] if p != "body")
            campos.setdefault(nome, []).append(e["msg"])
        return resposta_erro(400, "REQUISICAO_INVALIDA", "Dados inválidos.", {"campos": campos})

    @app.exception_handler(HTTPException)
    async def http(req: Request, exc: HTTPException):
        if exc.status_code == 404:
            return resposta_erro(404, "ROTA_NAO_ENCONTRADA", f"Rota não encontrada: {req.method} {req.url.path}")
        return resposta_erro(exc.status_code, "ERRO_HTTP", str(exc.detail))

    # Falhas do OpenRouter (cliente openai), depois das tentativas automáticas.
    @app.exception_handler(openai.RateLimitError)
    async def limite(_req: Request, exc: openai.RateLimitError):
        espera = exc.response.headers.get("retry-after")
        return resposta_erro(429, "LIMITE_DO_PROVEDOR", "Limite de requisições do provedor de LLM. Tente mais tarde.",
                             headers={"Retry-After": espera} if espera else None)

    @app.exception_handler(openai.APITimeoutError)
    async def timeout(_req: Request, _exc: openai.APITimeoutError):
        return resposta_erro(504, "TEMPO_ESGOTADO_PROVEDOR", "O provedor de LLM não respondeu a tempo.")

    @app.exception_handler(openai.APIError)
    async def falha_provedor(_req: Request, exc: openai.APIError):
        log.warning("Falha do provedor de LLM: %s", type(exc).__name__)
        return resposta_erro(502, "FALHA_PROVEDOR", "Falha no provedor de LLM.")

    @app.exception_handler(Exception)
    async def inesperado(_req: Request, exc: Exception):
        log.exception("Erro inesperado", exc_info=exc)
        return resposta_erro(500, "ERRO_INTERNO", "Erro interno do serviço de IA.")
