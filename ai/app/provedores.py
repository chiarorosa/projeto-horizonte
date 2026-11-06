"""Provedores reais: embeddings (local ou OpenRouter), LLM (OpenRouter) e pgvector (Neon).

As integrações são importadas dentro das funções para que os testes, que usam
simulações, não precisem carregar o PyTorch nem conectar ao banco.
"""

from llama_index.core import VectorStoreIndex
from llama_index.core.embeddings import BaseEmbedding
from sqlalchemy.engine import make_url

from app.config import Settings
from app.erros import AppError
from app.rag import Servicos

TABELA = "chunks"  # o PGVectorStore cria a tabela "data_chunks"
# Schema próprio da IA no banco compartilhado. O "public" é do Prisma (backend):
# tabelas do pgvector ali seriam vistas como diferença e o `prisma migrate dev`
# proporia apagar o banco.
SCHEMA = "rag"
TIMEOUT_S = 30
TENTATIVAS = 3  # o cliente repete com espera crescente em 429, timeout e erros 5xx
# Limite de tokens de saída. O padrão do LlamaIndex (256) não basta para modelos de
# raciocínio, que gastam parte dos tokens "pensando" antes de responder.
MAX_TOKENS_SAIDA = 2048


def _exigir(settings: Settings, *nomes: str) -> None:
    faltando = [n.upper() for n in nomes if not str(_valor(settings, n))]
    if faltando:
        raise AppError(503, "SERVICO_NAO_CONFIGURADO", "Variáveis de ambiente ausentes no .env.", {"variaveis": faltando})


def _valor(settings: Settings, nome: str) -> str:
    valor = getattr(settings, nome)
    return valor.get_secret_value() if hasattr(valor, "get_secret_value") else valor


def urls_do_banco(database_url: str) -> tuple[str, str]:
    """DATABASE_URL do Neon → conexões síncrona (psycopg2) e assíncrona (asyncpg, não usada).

    Devolve texto com a senha: str(URL) do SQLAlchemy a esconderia como "***".
    """
    url = make_url(database_url)
    sincrona = url.set(drivername="postgresql+psycopg2")
    assincrona = url.set(drivername="postgresql+asyncpg", query={})
    return sincrona.render_as_string(hide_password=False), assincrona.render_as_string(hide_password=False)


def criar_embeddings(settings: Settings) -> BaseEmbedding:
    if settings.embedding_provider == "local":
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        return HuggingFaceEmbedding(model_name=settings.embedding_model)

    _exigir(settings, "openrouter_api_key")
    from llama_index.embeddings.openai_like import OpenAILikeEmbedding

    return OpenAILikeEmbedding(
        model_name=settings.embedding_model,
        api_base=settings.openrouter_base_url,
        api_key=_valor(settings, "openrouter_api_key"),
        max_retries=TENTATIVAS,
        timeout=TIMEOUT_S,
    )


def criar_indice(settings: Settings) -> VectorStoreIndex:
    _exigir(settings, "database_url", "embedding_model")
    from llama_index.vector_stores.postgres import PGVectorStore

    embeddings = criar_embeddings(settings)
    # A dimensão do vetor depende do modelo; trocar de modelo exige reindexar.
    dimensao = len(embeddings.get_text_embedding("dimensão"))
    sincrona, assincrona = urls_do_banco(settings.database_url)
    store = PGVectorStore.from_params(
        connection_string=sincrona,
        async_connection_string=assincrona,
        table_name=TABELA,
        schema_name=SCHEMA,
        embed_dim=dimensao,
    )
    return VectorStoreIndex.from_vector_store(store, embed_model=embeddings)


def criar_servicos(settings: Settings) -> Servicos:
    _exigir(settings, "database_url", "openrouter_api_key", "openrouter_model")
    from llama_index.llms.openrouter import OpenRouter

    llm = OpenRouter(
        model=settings.openrouter_model,
        api_key=_valor(settings, "openrouter_api_key"),
        api_base=settings.openrouter_base_url,
        max_retries=TENTATIVAS,
        timeout=TIMEOUT_S,
        max_tokens=MAX_TOKENS_SAIDA,
    )
    return Servicos(indice=criar_indice(settings), llm=llm, modelo=settings.openrouter_model)
