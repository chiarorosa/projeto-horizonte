"""Núcleo do RAG: indexar documentos e responder perguntas citando as fontes."""

import logging
import time
from dataclasses import dataclass
from typing import Any

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.llms import LLM
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import FilterOperator, MetadataFilter, MetadataFilters

from app.erros import AppError
from app.modelos import ConsultaResposta, Fonte, Uso

log = logging.getLogger("horizonte.ai")

DIVISOR = SentenceSplitter(chunk_size=512, chunk_overlap=50)

PROMPT = """Você é o assistente do Projeto Horizonte. Responda à pergunta usando apenas os trechos abaixo.
Cite as fontes no formato [n]. Se os trechos não tiverem a resposta, diga que não encontrou a informação nos documentos.

Trechos:
{trechos}

Pergunta: {pergunta}
Resposta:"""


@dataclass
class Servicos:
    indice: VectorStoreIndex
    llm: LLM
    modelo: str


def indexar(indice: VectorStoreIndex, texto: str, documento_id: str, titulo: str) -> int:
    """Divide o texto em chunks e grava no índice, substituindo a versão anterior do documento."""
    indice.delete_ref_doc(documento_id, delete_from_docstore=True)
    documento = Document(text=texto, id_=documento_id, metadata={"documento_id": documento_id, "titulo": titulo})
    chunks = DIVISOR.get_nodes_from_documents([documento])
    indice.insert_nodes(chunks)
    return len(chunks)


def consultar(servicos: Servicos, pergunta: str, documentos_autorizados: list[str], top_k: int) -> ConsultaResposta:
    # Recuperação restrita aos documentos que o usuário pode acessar.
    filtros = MetadataFilters(
        filters=[MetadataFilter(key="documento_id", value=documentos_autorizados, operator=FilterOperator.IN)]
    )
    nos = servicos.indice.as_retriever(similarity_top_k=top_k, filters=filtros).retrieve(pergunta)
    if not nos:
        raise AppError(404, "DOCUMENTO_NAO_INDEXADO", "Nenhum dos documentos autorizados está indexado.")

    trechos = "\n".join(f"[{i}] ({n.node.metadata['titulo']}) {n.node.get_content()}" for i, n in enumerate(nos, 1))
    inicio = time.perf_counter()
    resposta = servicos.llm.complete(PROMPT.format(trechos=trechos, pergunta=pergunta))
    uso = _uso(resposta.raw, servicos.modelo, round((time.perf_counter() - inicio) * 1000))
    log.info("consulta modelo=%s tokens_entrada=%s tokens_saida=%s latencia_ms=%s custo_usd=%s",
             uso.modelo, uso.tokens_entrada, uso.tokens_saida, uso.latencia_ms, uso.custo_usd)

    return ConsultaResposta(
        resposta=resposta.text.strip(),
        fontes=[
            Fonte(
                documento_id=n.node.metadata["documento_id"],
                titulo=n.node.metadata["titulo"],
                trecho=n.node.get_content(),
                pagina=n.node.metadata.get("pagina"),
                score=n.score,
            )
            for n in nos
        ],
        uso=uso,
    )


def _campo(objeto: Any, nome: str) -> Any:
    return objeto.get(nome) if isinstance(objeto, dict) else getattr(objeto, nome, None)


def _uso(raw: Any, modelo: str, latencia_ms: int) -> Uso:
    """Tokens e custo informados pelo provedor (o OpenRouter devolve em `usage`)."""
    usage = _campo(raw, "usage") if raw is not None else None
    return Uso(
        modelo=modelo,
        tokens_entrada=_campo(usage, "prompt_tokens") if usage is not None else None,
        tokens_saida=_campo(usage, "completion_tokens") if usage is not None else None,
        latencia_ms=latencia_ms,
        custo_usd=_campo(usage, "cost") if usage is not None else None,
    )
