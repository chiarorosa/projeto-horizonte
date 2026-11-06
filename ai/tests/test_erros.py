import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.erros import AppError
from app.main import create_app


class Entrada(BaseModel):
    pergunta: str


def cliente_com_rotas_de_teste() -> TestClient:
    app = create_app()

    @app.get("/app-error")
    def app_error():
        raise AppError(404, "DOCUMENTO_NAO_INDEXADO", "Nenhum documento indexado.")

    @app.get("/falha")
    def falha():
        raise RuntimeError("chave secreta: sk-123")

    @app.post("/validacao")
    def validacao(entrada: Entrada):
        return entrada

    return TestClient(app, raise_server_exceptions=False)


def test_rota_inexistente_responde_404():
    res = cliente_com_rotas_de_teste().get("/nao-existe")

    assert res.status_code == 404
    assert res.json() == {
        "erro": {"codigo": "ROTA_NAO_ENCONTRADA", "mensagem": "Rota não encontrada: GET /nao-existe", "detalhes": {}}
    }


def test_app_error_usa_status_e_codigo():
    res = cliente_com_rotas_de_teste().get("/app-error")

    assert res.status_code == 404
    assert res.json()["erro"]["codigo"] == "DOCUMENTO_NAO_INDEXADO"


def test_corpo_invalido_responde_400_com_os_campos():
    res = cliente_com_rotas_de_teste().post("/validacao", json={})

    assert res.status_code == 400
    corpo = res.json()["erro"]
    assert corpo["codigo"] == "REQUISICAO_INVALIDA"
    assert "pergunta" in corpo["detalhes"]["campos"]


@pytest.mark.parametrize("corpo", [b"{ruim", b'{"pergunta": "hor\xe1rio"}'], ids=["json-malformado", "nao-utf8"])
def test_corpo_ilegivel_responde_400_requisicao_invalida(corpo):
    res = cliente_com_rotas_de_teste().post("/validacao", content=corpo, headers={"Content-Type": "application/json"})

    assert res.status_code == 400
    assert res.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"


def test_erro_inesperado_responde_500_sem_expor_a_mensagem():
    res = cliente_com_rotas_de_teste().get("/falha")

    assert res.status_code == 500
    assert res.json() == {"erro": {"codigo": "ERRO_INTERNO", "mensagem": "Erro interno do serviço de IA.", "detalhes": {}}}
