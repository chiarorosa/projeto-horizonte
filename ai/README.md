# ai/

Agentes, RAG, LLMs, inferência, avaliações e demais processamentos de Inteligência Artificial do Projeto Horizonte.

- Pode criar **simulações dos serviços dependentes** enquanto eles não estiverem disponíveis.
- A comunicação com o Backend segue os contratos de [`../contracts/`](../contracts/).
- **Não versionar** modelos, bases de dados brutas/processadas nem índices vetoriais (ver `.gitignore`). Documente em [`../docs/DEVELOPMENT.md`](../docs/DEVELOPMENT.md) como obtê-los.
- Chaves de API de provedores de LLM ficam apenas no `.env` local (ver [`../.env.example`](../.env.example)).
