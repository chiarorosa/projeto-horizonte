# ai/

RAG, agentes e inferência com LLMs do Projeto Horizonte. Recebe pedidos **somente do Backend** e devolve respostas e sugestões com as fontes citadas.

## Stack

| Camada | Escolha |
|---|---|
| Linguagem e serviço | Python 3.x, FastAPI, Pydantic, Uvicorn |
| Orquestração RAG | LlamaIndex (preferencial): ingestão e *chunking*, recuperação semântica Top-K, construção de contexto e geração com citação das fontes |
| LLM | [OpenRouter](https://openrouter.ai/docs) (`https://openrouter.ai/api/v1`); modelo escolhido por variável de ambiente, para trocar de modelo sem mudar o pipeline; *streaming* quando necessário |
| Embeddings | Opção A: Sentence Transformers (local). Opção B: API de embeddings do OpenRouter. Modelo configurável. |
| Banco vetorial | PostgreSQL (Neon) com a extensão pgvector: chunks, metadados e referências às fontes |

Um índice só pode ser consultado com o **mesmo modelo de embeddings** (e a mesma dimensão) que o criou. Trocar `EMBEDDING_MODEL` exige reindexar os documentos.

## Configuração

Variáveis no `.env` local (modelo em [`../.env.example`](../.env.example)):

| Variável | Descrição |
|---|---|
| `AI_PORT` | Porta local do serviço (padrão `8001`). |
| `OPENROUTER_API_KEY` | Chave do OpenRouter. **Nunca** vai para o Frontend nem para o Git. |
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1`. |
| `OPENROUTER_MODEL` | Modelo de LLM usado na geração. Prefira um modelo fixo com sufixo `:free` (lista dos gratuitos: [openrouter.ai/models?q=free](https://openrouter.ai/models?q=free); passo a passo no [README](../README.md#como-obter-os-valores-do-neon-e-do-openrouter)): o roteador `openrouter/free` troca de modelo a cada chamada, o que atrapalha comparar resultados. O modelo que respondeu fica em `uso.modelo`. |
| `EMBEDDING_PROVIDER` | `local` (Sentence Transformers, padrão, sem custo) ou `openrouter`. |
| `EMBEDDING_MODEL` | Modelo de embeddings. Padrão: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (multilíngue, 384 dimensões). |
| `DATABASE_URL` | Conexão com o PostgreSQL (Neon) com pgvector, a mesma do backend. |

## Requisitos

- A chave de API nunca é exposta ao Frontend.
- A recuperação fica restrita aos documentos que o usuário pode acessar (`documentos_autorizados`).
- Cada chamada ao LLM registra modelo, tokens, latência e custo.
- As chamadas ao OpenRouter têm *timeout* e *retry* e tratam o `429` (limite de requisições).
- Toda resposta traz as fontes usadas (rastreabilidade).
- O conteúdo gerado é sugestão: só é publicado depois da validação humana (feita no Backend/Frontend).
- Só documentos autorizados, sintéticos ou anonimizados (LGPD). Modelos, dados brutos e índices não vão para o Git (ver `.gitignore`).

## Estrutura

```text
ai/
├── app/
│   ├── main.py         # App FastAPI: GET /health e POST /consultas
│   ├── __main__.py     # python -m app (sobe na AI_PORT)
│   ├── config.py       # Variáveis de ambiente (pydantic-settings, .env da raiz)
│   ├── modelos.py      # Formatos de requisição e resposta (Pydantic)
│   ├── rag.py          # Núcleo do RAG: indexar e consultar com fontes
│   ├── provedores.py   # OpenRouter, embeddings e pgvector (Neon)
│   ├── indexar.py      # python -m app.indexar <arquivo>
│   └── erros.py        # AppError e o formato de erro comum
├── tests/              # pytest; usam LLM, embeddings e índice simulados
└── exemplos/           # Documentos sintéticos para testar a indexação
```

## Execução e testes

Pré-requisito: [Python](https://www.python.org/) 3.12 ou mais recente. As variáveis vêm do `.env` da **raiz** do repositório (`cp .env.example .env`). Para consultar, preencha `DATABASE_URL`, `OPENROUTER_API_KEY` e `OPENROUTER_MODEL` (um modelo com sufixo `:free` não tem custo).

```bash
cd ai
python -m venv .venv
.venv\Scripts\activate          # Windows; no Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                          # testes: sem rede, sem chave e sem banco
python -m app                   # http://localhost:8001/health e http://localhost:8001/docs
```

Indexar o documento de exemplo e consultar (com o serviço no ar):

```bash
python -m app.indexar exemplos/politica-de-senhas.md --id doc-politica-senhas --titulo "Política de Senhas"
curl -X POST http://localhost:8001/consultas -H "Content-Type: application/json" \
  -d '{"pergunta": "De quanto em quanto tempo devo trocar a senha?", "documentos_autorizados": ["doc-politica-senhas"]}'
```

Na primeira execução com `EMBEDDING_PROVIDER=local`, o modelo de embeddings (cerca de 500 MB) é baixado e guardado no cache do Hugging Face. A instalação inclui o PyTorch e ocupa cerca de 1,3 GB no `.venv`.

**Para mudar o RAG:** escreva o teste em `tests/` (use o `MockLLM` e o `MockEmbedding` como em `tests/test_consultas.py`), altere `app/rag.py` e, se a interface mudar, atualize o template abaixo no mesmo PR, com revisão do Backend.

## Integração (template)

**Backend → IA**, HTTP/JSON. O formato de erro é o comum, definido em [`../backend/README.md`](../backend/README.md#integração-template). A documentação interativa fica em `/docs` (gerada pelo FastAPI). Para cada endpoint novo, copie o bloco abaixo.

### `GET /health`

Resposta `200`:

```json
{ "status": "ok" }
```

### `POST /consultas`

Pergunta respondida por RAG, restrita aos documentos autorizados.

Requisição:

```json
{
  "pergunta": "Qual é o prazo para trocar a senha?",
  "documentos_autorizados": ["doc-politica-senhas"],
  "top_k": 5
}
```

Resposta `200`:

```json
{
  "resposta": "A senha deve ser trocada a cada 90 dias [1].",
  "fontes": [
    {
      "documento_id": "doc-politica-senhas",
      "titulo": "Política de Senhas",
      "trecho": "As senhas devem ser alteradas a cada 90 dias.",
      "pagina": 2,
      "score": 0.87
    }
  ],
  "uso": { "modelo": "<OPENROUTER_MODEL>", "tokens_entrada": 812, "tokens_saida": 64, "latencia_ms": 1430, "custo_usd": 0.0004 }
}
```

`pagina` vem `null` em documentos sem páginas (`.md`, `.txt`). `tokens_*` e `custo_usd` vêm `null` quando o provedor não os informa.

Erros (`codigo`): `400` `REQUISICAO_INVALIDA`, `404` `DOCUMENTO_NAO_INDEXADO` (nenhum dos documentos autorizados está indexado), `429` `LIMITE_DO_PROVEDOR` (com `Retry-After`), `502` `FALHA_PROVEDOR` ou `RESPOSTA_VAZIA_DO_LLM` (o modelo não gerou texto), `503` `SERVICO_NAO_CONFIGURADO` (variáveis ausentes, listadas em `detalhes.variaveis`), `504` `TEMPO_ESGOTADO_PROVEDOR`.
