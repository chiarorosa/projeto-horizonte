import httpx
import openai
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.erros import AppError
from app.main import create_app
from app.provedores import criar_servicos, urls_do_banco

REQ = httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions")


def cliente_que_lanca(erro: Exception) -> TestClient:
    app = create_app()

    @app.get("/provedor")
    def provedor():
        raise erro

    return TestClient(app, raise_server_exceptions=False)


def test_limite_do_provedor_responde_429_com_retry_after():
    erro = openai.RateLimitError("limite", response=httpx.Response(429, headers={"retry-after": "7"}, request=REQ), body=None)

    res = cliente_que_lanca(erro).get("/provedor")

    assert res.status_code == 429
    assert res.headers["retry-after"] == "7"
    assert res.json()["erro"]["codigo"] == "LIMITE_DO_PROVEDOR"


def test_timeout_do_provedor_responde_504():
    res = cliente_que_lanca(openai.APITimeoutError(request=REQ)).get("/provedor")

    assert res.status_code == 504
    assert res.json()["erro"]["codigo"] == "TEMPO_ESGOTADO_PROVEDOR"


def test_falha_do_provedor_responde_502():
    erro = openai.InternalServerError("falha", response=httpx.Response(500, request=REQ), body=None)

    res = cliente_que_lanca(erro).get("/provedor")

    assert res.status_code == 502
    assert res.json()["erro"]["codigo"] == "FALHA_PROVEDOR"


def test_configuracao_incompleta_responde_503_com_as_variaveis():
    with pytest.raises(AppError) as exc:
        criar_servicos(Settings(_env_file=None, openrouter_api_key="", openrouter_model="", database_url=""))

    assert exc.value.status == 503
    assert set(exc.value.detalhes["variaveis"]) == {"DATABASE_URL", "OPENROUTER_API_KEY", "OPENROUTER_MODEL"}


def test_vetores_ficam_no_schema_rag_separado_do_prisma(monkeypatch):
    # O Prisma cuida do schema "public"; tabelas do pgvector ali seriam vistas como
    # diferença pelo prisma migrate, que proporia apagar o banco.
    from llama_index.core.embeddings import MockEmbedding
    from llama_index.vector_stores.postgres import PGVectorStore

    from app import provedores

    class Capturado(Exception):
        pass

    parametros = {}

    def from_params_falso(**kw):
        parametros.update(kw)
        raise Capturado  # não conecta ao banco

    monkeypatch.setattr(provedores, "criar_embeddings", lambda _s: MockEmbedding(embed_dim=8))
    monkeypatch.setattr(PGVectorStore, "from_params", from_params_falso)

    with pytest.raises(Capturado):
        provedores.criar_indice(Settings(_env_file=None, database_url="postgresql://u:s@host/db"))

    assert parametros["schema_name"] == "rag"
    assert parametros["embed_dim"] == 8


def test_url_do_neon_vira_conexoes_do_sqlalchemy_com_a_senha():
    # O PGVectorStore recebe texto: str(URL) do SQLAlchemy esconderia a senha como "***".
    sincrona, assincrona = urls_do_banco("postgresql://u:s3gr3do@ep-x.neon.tech/horizonte?sslmode=require&channel_binding=require")

    assert sincrona == "postgresql+psycopg2://u:s3gr3do@ep-x.neon.tech/horizonte?channel_binding=require&sslmode=require"
    assert assincrona == "postgresql+asyncpg://u:s3gr3do@ep-x.neon.tech/horizonte"
