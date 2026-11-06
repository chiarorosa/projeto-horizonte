from functools import lru_cache

from fastapi import Depends, FastAPI

from app.config import get_settings
from app.erros import registrar_tratadores
from app.modelos import ConsultaEntrada, ConsultaResposta
from app.provedores import criar_servicos
from app.rag import Servicos, consultar


@lru_cache
def obter_servicos() -> Servicos:
    # Criado na primeira consulta e reaproveitado; se faltar configuração, responde 503 e tenta de novo depois.
    return criar_servicos(get_settings())


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
