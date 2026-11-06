from fastapi import Depends, FastAPI

from app.erros import AppError, registrar_tratadores
from app.modelos import ConsultaEntrada, ConsultaResposta
from app.rag import Servicos, consultar


def obter_servicos() -> Servicos:
    raise AppError(503, "SERVICO_NAO_CONFIGURADO", "Provedores de LLM e de embeddings ainda não configurados.")


def create_app() -> FastAPI:
    app = FastAPI(title="Projeto Horizonte — IA", version="0.1.0")
    registrar_tratadores(app)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/consultas")
    def consultas(entrada: ConsultaEntrada, servicos: Servicos = Depends(obter_servicos)) -> ConsultaResposta:
        return consultar(servicos, entrada.pergunta, entrada.documentos_autorizados, entrada.top_k)

    return app


app = create_app()
