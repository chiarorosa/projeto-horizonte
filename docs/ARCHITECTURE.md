# Arquitetura do Projeto Horizonte

Este documento registra as responsabilidades dos módulos, os fluxos de comunicação, os limites entre equipes e as decisões arquiteturais. Ele deve ser atualizado no mesmo PR de qualquer mudança relevante de arquitetura.

## 1. Visão geral

O Horizonte é organizado como um **monorepo modular**: um único repositório com módulos independentes para Backend, Frontend e IA, que se comunicam por contratos explícitos.

```text
┌────────────┐   HTTP (contracts/)   ┌────────────┐   HTTP (contracts/)   ┌────────────┐
│  frontend  │ ────────────────────▶ │  backend   │ ────────────────────▶ │     ai     │
│ (interface)│ ◀──────────────────── │ (API/dados)│ ◀──────────────────── │ (agentes,  │
└────────────┘                       └────────────┘                       │  RAG, LLMs)│
                                           │                              └────────────┘
                                           ▼
                                     ┌────────────┐
                                     │   banco    │
                                     └────────────┘
```

> O diagrama representa o fluxo **proposto**. A comunicação direta Frontend → IA, se necessária, deve ser decidida e registrada na seção 5.

## 2. Responsabilidades dos módulos

| Módulo | Responsabilidade | Não deve |
|---|---|---|
| `backend/` | API pública, autenticação, persistência e regras de negócio. | Implementar lógica de interface ou de modelos de IA. |
| `frontend/` | Páginas, componentes, navegação, dashboards e gamificação. | Acessar o banco de dados diretamente ou guardar segredos. |
| `ai/` | Agentes, RAG, inferência com LLMs e avaliações. | Persistir dados de negócio sem passar pelo Backend. |
| `contracts/` | OpenAPI, JSON Schemas, códigos de erro e autenticação entre serviços. | Conter implementação. |
| `infra/` | Docker e configuração do ambiente local integrado. | Conter credenciais reais. |
| `docs/` | Arquitetura, desenvolvimento e decisões técnicas. | — |

## 3. Fluxos de comunicação

A definir pelas equipes e documentar em `contracts/`. Para cada fluxo, registrar:

- Origem e destino (ex.: Frontend → Backend).
- Protocolo e formato (ex.: HTTP/JSON).
- Contrato correspondente (arquivo em `contracts/`).
- Forma de autenticação.

| Fluxo | Protocolo | Contrato | Autenticação |
|---|---|---|---|
| Frontend → Backend | _a definir_ | _a definir_ | _a definir_ |
| Backend → IA | _a definir_ | _a definir_ | _a definir_ |

## 4. Limites e dependências

- Cada equipe altera **apenas o seu módulo**; mudanças em outro módulo exigem alinhamento com a equipe responsável.
- Os módulos dependem uns dos outros **somente por meio dos contratos** em `contracts/`.
- Frontend e IA podem usar **dados simulados** enquanto os serviços dependentes não estiverem prontos, desde que sigam os contratos.
- Pastas separadas não significam integração automática: nomes de campos, códigos de erro e autenticação devem ser combinados antes.

## 5. Decisões arquiteturais

Registre cada decisão relevante (stack, banco de dados, provedor de LLM, formato de autenticação etc.) usando o modelo abaixo.

| # | Data | Decisão | Motivo | Status |
|---|---|---|---|---|
| 001 | 2026-10-09 | Monorepo modular com GitHub Flow e integração via PR revisado. | Um único repositório para as três frentes, com isolamento por pastas e revisão obrigatória. | Aceita |
| 002 | 2026-10-09 | Sem GitHub Actions/CI nesta etapa. | Testes e evidências são responsabilidade de alunos e professores, apresentados no PR. | Aceita |
