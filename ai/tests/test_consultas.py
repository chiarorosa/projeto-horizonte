import pytest
from fastapi.testclient import TestClient
from llama_index.core import VectorStoreIndex
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

from app.main import create_app, obter_servicos
from app.rag import Servicos, indexar


@pytest.fixture
def servicos() -> Servicos:
    # Índice em memória, embeddings e LLM simulados: sem rede, sem chave, sem banco.
    indice = VectorStoreIndex([], embed_model=MockEmbedding(embed_dim=8))
    indexar(indice, "As senhas devem ser alteradas a cada 90 dias.", "doc-senhas", "Política de Senhas")
    indexar(indice, "O colaborador tem direito a 30 dias de férias por ano.", "doc-ferias", "Política de Férias")
    return Servicos(indice=indice, llm=MockLLM(), modelo="mock")


@pytest.fixture
def cliente(servicos: Servicos) -> TestClient:
    app = create_app()
    app.dependency_overrides[obter_servicos] = lambda: servicos
    return TestClient(app)


def consultar(cliente: TestClient, **corpo):
    return cliente.post("/consultas", json={"pergunta": "Qual o prazo da senha?", **corpo})


def test_responde_com_resposta_fontes_e_uso(cliente):
    res = consultar(cliente, documentos_autorizados=["doc-senhas"])

    assert res.status_code == 200
    corpo = res.json()
    assert corpo["resposta"]
    assert corpo["fontes"][0] == {
        "documento_id": "doc-senhas",
        "titulo": "Política de Senhas",
        "trecho": "As senhas devem ser alteradas a cada 90 dias.",
        "pagina": None,
        "score": pytest.approx(corpo["fontes"][0]["score"]),
    }
    assert corpo["uso"]["modelo"] == "mock"
    assert corpo["uso"]["latencia_ms"] >= 0


def test_usa_somente_documentos_autorizados(cliente):
    res = consultar(cliente, documentos_autorizados=["doc-ferias"], top_k=10)

    assert {f["documento_id"] for f in res.json()["fontes"]} == {"doc-ferias"}
    assert "90 dias" not in res.json()["resposta"]


def test_documento_nao_indexado_responde_404(cliente):
    res = consultar(cliente, documentos_autorizados=["doc-inexistente"])

    assert res.status_code == 404
    assert res.json()["erro"]["codigo"] == "DOCUMENTO_NAO_INDEXADO"


def test_lista_de_documentos_vazia_responde_400(cliente):
    res = consultar(cliente, documentos_autorizados=[])

    assert res.status_code == 400
    assert "documentos_autorizados" in res.json()["erro"]["detalhes"]["campos"]


def test_reindexar_substitui_a_versao_anterior(servicos, cliente):
    indexar(servicos.indice, "As senhas devem ser alteradas a cada 60 dias.", "doc-senhas", "Política de Senhas")

    fontes = consultar(cliente, documentos_autorizados=["doc-senhas"], top_k=10).json()["fontes"]

    assert [f["trecho"] for f in fontes] == ["As senhas devem ser alteradas a cada 60 dias."]
