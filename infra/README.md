# infra/

Docker e configurações de ambiente para execução local e integração dos serviços.

- Dockerfiles e arquivos auxiliares de cada serviço podem ficar aqui (ex.: `infra/backend.Dockerfile`) ou dentro do próprio módulo, conforme decidido em [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md).
- A execução integrada é feita pelo [`../compose.yaml`](../compose.yaml) na raiz.
- Mudanças que afetam outras equipes (portas, variáveis, volumes) **precisam ser comunicadas** na Issue/PR e refletidas em [`../.env.example`](../.env.example) e [`../docs/DEVELOPMENT.md`](../docs/DEVELOPMENT.md).
