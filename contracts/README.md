# contracts/

Contratos de comunicação e schemas compartilhados entre Backend, Frontend e IA.

Exemplos do que deve ficar aqui:

- Especificações **OpenAPI** dos endpoints (`openapi.yaml`).
- **JSON Schemas** de requisições, respostas e eventos.
- Tabela de **códigos de erro** e formato padrão de erro.
- Definição da forma de **autenticação** entre os serviços.

## Regras

- Toda mudança em `contracts/` deve ser feita em PR próprio ou claramente identificado.
- Mudanças exigem **alinhamento entre as equipes afetadas** antes do merge; marque representantes de cada equipe como revisores.
- Mudanças incompatíveis (remover/renomear campos, alterar tipos) devem ser registradas em [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md).
