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
| `OPENROUTER_MODEL` | Modelo de LLM usado na geração. |
| `EMBEDDING_PROVIDER` | `local` (Sentence Transformers) ou `openrouter`. |
| `EMBEDDING_MODEL` | Modelo de embeddings. |
| `DATABASE_URL` | Conexão com o PostgreSQL (Neon) com pgvector. |

## Requisitos

- A chave de API nunca é exposta ao Frontend.
- A recuperação fica restrita aos documentos que o usuário pode acessar (`documentos_autorizados`).
- Cada chamada ao LLM registra modelo, tokens, latência e custo.
- As chamadas ao OpenRouter têm *timeout* e *retry* e tratam o `429` (limite de requisições).
- Toda resposta traz as fontes usadas (rastreabilidade).
- O conteúdo gerado é sugestão: só é publicado depois da validação humana (feita no Backend/Frontend).
- Só documentos autorizados, sintéticos ou anonimizados (LGPD). Modelos, dados brutos e índices não vão para o Git (ver `.gitignore`).

## Execução e testes

*A definir na Issue do esqueleto do serviço de IA (instalação, execução com Uvicorn e testes).*

## Integração (template)

**Backend → IA**, HTTP/JSON. O formato de erro é o comum, definido em [`../backend/README.md`](../backend/README.md#integração-template). Esta é a **proposta inicial**: a equipe de IA confirma ou ajusta os campos no PR do esqueleto, com revisão do Backend. Para cada endpoint novo, copie o bloco abaixo.

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

Erros: `400` (requisição inválida), `404` (documento não indexado), `429` (limite do provedor, com `Retry-After`), `502`/`504` (falha ou *timeout* do provedor).
