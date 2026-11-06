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


def test_url_do_neon_vira_conexoes_do_sqlalchemy():
    sincrona, assincrona = urls_do_banco("postgresql://u:s@ep-x.neon.tech/horizonte?sslmode=require&channel_binding=require")

    assert sincrona.drivername == "postgresql+psycopg2"
    assert sincrona.query["sslmode"] == "require"
    assert assincrona.drivername == "postgresql+asyncpg"
    assert dict(assincrona.query) == {}
