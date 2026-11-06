# Projeto Horizonte: capacitação corporativa com IA generativa, RAG e gamificação

[![Regras do PR](https://github.com/chiarorosa/projeto-horizonte/actions/workflows/regras-pr.yml/badge.svg)](https://github.com/chiarorosa/projeto-horizonte/actions/workflows/regras-pr.yml)
[![Documentação](https://github.com/chiarorosa/projeto-horizonte/actions/workflows/documentacao.yml/badge.svg)](https://github.com/chiarorosa/projeto-horizonte/actions/workflows/documentacao.yml)
[![Licença do código: Apache-2.0](https://img.shields.io/badge/c%C3%B3digo-Apache--2.0-blue)](LICENSE)
[![Licença da documentação: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE-DOCS)

O **Projeto Horizonte** é um protótipo de **plataforma de capacitação contínua** em que **agentes de IA generativa** transformam normas, políticas e manuais de uma organização em **trilhas de aprendizagem gamificadas** (níveis, XP, badges e milestones), com um **tutor de IA** para o colaborador. O conteúdo é recuperado dos documentos institucionais por **RAG** (*Retrieval-Augmented Generation*) com embeddings, mantém a rastreabilidade das fontes e é validado por um gestor antes de ser publicado, em conformidade com a **LGPD**. É um projeto de pesquisa aplicada do **UniSenac-RS**.

**In English:** Horizonte is an applied research prototype (UniSenac-RS, Brazil) of a gamified, agent-based corporate learning platform. Generative AI agents use Retrieval-Augmented Generation (RAG) over an organization's own documents to suggest learning paths, activities and assessments, which a manager reviews before publishing, with source traceability and LGPD (Brazil's data protection law) compliance.

> **Guia de contribuição para as equipes de Backend, Frontend e Inteligência Artificial.**
>
> **Regra principal:** cada tarefa deve ter sua própria Issue e branch. Nenhum aluno deve enviar alterações diretamente para `main`: toda integração deve ocorrer por **Pull Request (PR)**, após revisão.

## Sobre o Horizonte

**Plataforma Inteligente para Capacitação Contínua assistida por IA Generativa e Gamificação**, projeto de pesquisa aplicada do UniSenac-RS (linha Transformação Digital e Segurança da Informação), com vigência de julho/2026 a junho/2027.

**Objetivo:** desenvolver, testar e avaliar um protótipo de plataforma agêntica gamificada, baseada em embeddings e *Retrieval-Augmented Generation* (RAG), que apoie a criação assistida por IA de jornadas de letramento digital e treinamento corporativo personalizado a partir de documentos institucionais.

**Problema:** organizações têm dificuldade em transformar normas, políticas, manuais e materiais internos em aprendizagem personalizada e atualizada. Ferramentas comerciais de IA generativa não têm acesso seguro e contextualizado a esses documentos, e criar trilhas, atividades e avaliações manualmente exige tempo e equipe especializada.

**Escopo do protótipo:**

| Componente | Descrição | Módulo |
|---|---|---|
| Pipeline RAG | Ingestão de documentos, extração de texto, segmentação, embeddings, indexação vetorial e recuperação contextualizada. | `ai/` |
| Agentes de IA | Sugerem trilhas, milestones, atividades, avaliações e feedbacks a partir de um objetivo e de documentos selecionados; agente tutor para o colaborador. | `ai/` |
| Gamificação | Níveis, XP, badges/conquistas e milestones de progresso. | `backend/` e `frontend/` |
| Experiência do colaborador | Onboarding conversacional, nivelamento, dashboard da trilha, ambiente de aprendizagem com tutor. | `frontend/` |
| Painel de gestão | Seleção de documentos, criação e revisão de jornadas, acompanhamento de progresso. | `frontend/` e `backend/` |
| API e dados | Autenticação, persistência, regras de negócio e integração dos módulos. | `backend/` |

**Perfis de usuário:** colaborador (aprende), gestor (cria e valida jornadas) e administrador (configura a plataforma).

**Princípios obrigatórios:**

- O conteúdo gerado pelos agentes é **sugestão**: o gestor revisa e valida antes de publicar.
- Usar apenas documentos **autorizados, sintéticos ou anonimizados**, com minimização de dados, controle de acesso e conformidade com a **LGPD** (Lei nº 13.709/2018).
- Respostas e conteúdos gerados devem manter **rastreabilidade das fontes** consultadas.

## 1. Início rápido

```bash
ssh -T git@github.com                       # verifica o acesso SSH ao GitHub
git clone git@github.com:chiarorosa/projeto-horizonte.git
cd projeto-horizonte
cp .env.example .env                        # preencha os valores localmente
```

Depois:

1. Leia o [`AGENTS.md`](AGENTS.md). Ele vale para você **e** para o seu assistente de IA: fluxo SDD, boas práticas e templates de Issue.
2. Leia o README do seu módulo: [`backend/`](backend/README.md), [`frontend/`](frontend/README.md) ou [`ai/`](ai/README.md). Lá estão a stack, os comandos e os templates de integração.
3. Escolha uma Issue atribuída a você no GitHub Project e siga o fluxo da seção 5.

Pré-requisitos: [Git](https://git-scm.com/), conta no GitHub com chave SSH e as ferramentas da stack do seu módulo. O [Node.js](https://nodejs.org/) também roda o lint de Markdown local.

## 2. Estrutura do repositório

Um **monorepo**: um único repositório com uma pasta por equipe.

```text
projeto-horizonte/
├── backend/         # API, autenticação, banco, regras de negócio e gamificação
├── frontend/        # Telas, navegação, dashboards e gamificação visual
├── ai/              # RAG, agentes e inferência com LLMs
├── .github/         # Templates de Issue e PR, workflows do CI
├── AGENTS.md        # Regras para alunos e assistentes de IA
├── CONTRIBUTING.md  # Regras de colaboração
├── README.md        # Este arquivo
└── .env.example     # Variáveis de ambiente, sem valores reais
```

Cada equipe altera **apenas o seu módulo**. Pastas separadas não significam integração automática: endpoints, campos e erros são combinados antes, na seção "Integração" do README do módulo dono. Não inclua senhas, tokens, chaves de API nem arquivos `.env` reais no Git.

## 3. Arquitetura

```text
┌────────────┐   HTTP/JSON   ┌────────────┐   HTTP/JSON   ┌────────────┐
│  frontend  │ ────────────▶ │  backend   │ ────────────▶ │     ai     │
│  (Vercel)  │ ◀──────────── │  (Render)  │ ◀──────────── │ (RAG, LLM) │──▶ OpenRouter
└────────────┘               └────────────┘               └────────────┘
                                   │                            │
                                   ▼                            ▼
                             ┌──────────────────────────────────────┐
                             │     PostgreSQL (Neon) + pgvector     │
                             └──────────────────────────────────────┘
```

| Módulo | Responsabilidade | Não deve | Integração |
|---|---|---|---|
| `backend/` | API pública, autenticação, persistência, regras de negócio e gamificação. | Ter lógica de interface ou de modelos de IA. | Frontend → Backend e formato de erro comum: [`backend/README.md`](backend/README.md#integração-template) |
| `frontend/` | Páginas, componentes, navegação, dashboards e gamificação. | Acessar o banco, chamar a IA diretamente ou guardar segredos. | Consome o Backend. |
| `ai/` | RAG, agentes, inferência via OpenRouter e avaliações. | Persistir dados de negócio sem passar pelo Backend. | Backend → IA: [`ai/README.md`](ai/README.md#integração-template) |

### Decisões

Registre cada decisão relevante (stack, banco, provedor de LLM, autenticação etc.) como uma nova linha.

| # | Data | Decisão | Motivo | Status |
|---|---|---|---|---|
| 001 | 2026-10-09 | Monorepo modular com GitHub Flow e integração via PR revisado. | Um único repositório para as três frentes, com isolamento por pastas e revisão obrigatória. | Aceita |
| 002 | 2026-10-09 | Sem GitHub Actions/CI nesta etapa. | Testes e evidências são responsabilidade de alunos e professores, apresentados no PR. | Substituída pela 003 |
| 003 | 2026-10-19 | GitHub Actions valida cada PR (regras do `CONTRIBUTING.md` e qualidade da documentação); os checks são obrigatórios na `main`. Os testes dos módulos seguem locais até entrarem como jobs. | Com o repositório público, o Actions é gratuito, e as conferências ficam automáticas e iguais para todos. | Aceita |
| 004 | 2026-11-06 | Sem Docker: cada módulo roda com as ferramentas da sua stack e é publicado em serviços gerenciados (Render, Vercel, Neon). Saem `compose.yaml` e `infra/`. | Começo mais simples para os alunos. | Aceita |
| 005 | 2026-11-06 | A documentação fica no `README.md`, no `AGENTS.md` e nos READMEs dos módulos; os templates de integração ficam na seção "Integração" do módulo dono. Saem `docs/` e `contracts/`. | Menos lugares para procurar e manter. | Aceita |
| 006 | 2026-11-06 | Fluxo SDD com a spec na Issue (template Tarefa) e boas práticas karpathy-guidelines e agent-skills em qualquer assistente de IA (`AGENTS.md`). | Especificar antes de codar, com o mesmo padrão em todas as ferramentas. | Aceita |
| 007 | 2026-11-06 | Backend: Node.js, TypeScript, Express, Prisma (ORM e Migrate), Zod, JWT, bcrypt, Swagger/OpenAPI, Vitest e Supertest; deploy no Render. | Stack definida pela coordenação ([`backend/README.md`](backend/README.md)). | Aceita |
| 008 | 2026-11-06 | Frontend: React, TypeScript, Vite, React Router, React Hook Form, Zod, Zustand, Fetch API (TanStack Query opcional), Vitest, React Testing Library e Playwright; deploy na Vercel. | Stack definida pela coordenação ([`frontend/README.md`](frontend/README.md)). | Aceita |
| 009 | 2026-11-06 | IA: Python, FastAPI, Pydantic, Uvicorn, LlamaIndex, OpenRouter (LLM e, opcionalmente, embeddings), Sentence Transformers e pgvector no PostgreSQL (Neon). | Stack definida pela coordenação ([`ai/README.md`](ai/README.md)). | Aceita |
| 010 | 2026-11-06 | Frontend: MVP só para testar backend e IA, testes reduzidos a um teste de fumaça (Playwright adiado) e chamadas por `/api` com proxy (Vite em desenvolvimento, *rewrite* na Vercel). | Começo mais simples para a equipe de frontend; o proxy evita CORS e endereços no código. | Aceita |

## 4. Variáveis de ambiente

As variáveis ficam no `.env` local (não versionado). O [`.env.example`](.env.example) lista todas, sem valores secretos. Ao adicionar uma variável, inclua-a no `.env.example` e nesta tabela, no mesmo PR.

| Variável | Módulo | Descrição |
|---|---|---|
| `APP_ENV` | todos | Ambiente de execução (`development`). |
| `DATABASE_URL` | backend, ai | Conexão com o PostgreSQL (Neon), com pgvector. |
| `BACKEND_PORT` | backend | Porta local da API. |
| `JWT_SECRET` | backend | Segredo para assinatura de tokens. |
| `FRONTEND_PORT` | frontend | Porta local da interface. |
| `API_BASE_URL` | frontend | Endereço do backend. O frontend chama `/api` e o proxy do Vite repassa para cá. |
| `VITE_USAR_DADOS_SIMULADOS` | frontend | `true` usa dados simulados nas telas, sem o backend no ar; `false` chama o backend. |
| `AI_PORT` | ai | Porta local do serviço de IA. |
| `OPENROUTER_API_KEY` | ai | Chave do OpenRouter (nunca no Frontend). |
| `OPENROUTER_BASE_URL` | ai | `https://openrouter.ai/api/v1`. |
| `OPENROUTER_MODEL` | ai | Modelo de LLM. |
| `EMBEDDING_PROVIDER` | ai | `local` (Sentence Transformers) ou `openrouter`. |
| `EMBEDDING_MODEL` | ai | Modelo de embeddings. |

### Como obter os valores do Neon e do OpenRouter

Guarde os valores só no `.env` da **raiz** do repositório (`projeto-horizonte/.env`, não na pasta de cima). Nunca cole chaves ou senhas em Issues, PRs ou no chat.

**`DATABASE_URL` (Neon, banco compartilhado):** todos usam **o mesmo projeto Neon**, criado pela coordenação na região de São Paulo (`sa-east-1`).

| Branch do Neon | Quem usa | Regra |
|---|---|---|
| `production` | **Ninguém desenvolve nela** | Reservada para o que já está pronto: só recebe migrações (`npx prisma migrate deploy`), seed e indexação **depois do merge do PR**. É a branch padrão do Neon. |
| `dev-banco` | Todos (backend e IA) | Desenvolvimento do dia a dia. É uma cópia da `production`. **Só o responsável pelo banco roda `npm run db:migrate`**, e avisa a equipe antes de aceitar um *reset* (os dados de teste de todos iriam junto). |

Os dados da `dev-banco` são fictícios e se recriam com o seed e o `python -m app.indexar`. Para deixá-la igual à `production` de novo, use **Reset from parent** na página da branch no Neon.

Para o aluno:

1. Aceite o convite do Neon que chega por e-mail.
2. No projeto, clique em **Connect**, escolha a branch **`dev-banco`** e **desligue "Connection pooling"**. O Prisma precisa da conexão **direta**: o endereço do *host* não pode ter `-pooler`.
3. Copie a *connection string* (termina em `?sslmode=require...`) para `DATABASE_URL`. O backend e a IA usam a mesma.

No banco, cada módulo tem o seu schema: o **`public`** é do Prisma (backend) e o **`rag`** é dos vetores da IA (criado na primeira indexação, com a extensão pgvector). Não crie tabelas à mão em nenhum dos dois.

**Novas migrações:** o responsável cria a migração na `dev-banco` e a envia no PR (`backend/prisma/migrations/`). Depois do merge do PR, o responsável aplica na `production` com `cd backend && npx prisma migrate deploy` (que só aplica migrações e nunca apaga dados), usando temporariamente o `DATABASE_URL` da `production`.

Para a coordenação (uma vez):

1. Na organização do Neon, em **People → Invite member**, convide cada aluno pelo e-mail com o papel **Collaborator** (o plano gratuito tem membros ilimitados).
2. No projeto, em **Settings → Project permissions**, dê **Editor** a cada aluno. Não use **Settings → Sharing**, que o Neon está descontinuando.
3. Em **Branches**, crie a `dev-banco` com *parent* `production` (o plano gratuito permite 10 branches por projeto).

**`OPENROUTER_API_KEY` e `OPENROUTER_MODEL` (OpenRouter):**

1. Em [openrouter.ai](https://openrouter.ai), vá em **Keys → Create Key** e copie a chave (`sk-or-...`) para `OPENROUTER_API_KEY`. Se quiser, defina ali um limite de crédito.
2. Para escolher um modelo sem custo, filtre a lista pelos gratuitos: [openrouter.ai/models?q=free](https://openrouter.ai/models?q=free). Copie o id de um modelo terminado em `:free` para `OPENROUTER_MODEL`.
3. Em [Settings → Privacy](https://openrouter.ai/settings/privacy), deixe **desligada** a opção **"Allow free endpoints that train on request data"**. Com ela ligada, o provedor gratuito pode **guardar e treinar com os prompts e as respostas**, e os prompts levam trechos dos documentos indexados (LGPD). Testamos com ela desligada e o `openrouter/free` funcionou: o roteador passa a usar só provedores que não treinam com os dados, o que reduz os modelos disponíveis.
   - Se um id `:free` fixo falhar com `No endpoints found matching your data policy` (no serviço de IA, `502` `FALHA_PROVEDOR`), aquele modelo só existe em provedores que treinam com os dados: troque de modelo em vez de ligar a opção.
   - Mesmo assim, com modelos gratuitos use **apenas documentos sintéticos ou anonimizados**, nunca documentos internos reais.
4. No primeiro teste de integração usamos `OPENROUTER_MODEL=openrouter/free`. Ele não é um modelo, e sim um **roteador** que escolhe um modelo gratuito diferente a cada chamada (o modelo que respondeu aparece em `uso.modelo`). Serve para começar; para comparar resultados, fixe um id `:free`.

## 5. Fluxo de trabalho do aluno: da Issue à entrega

**Regras:** nada de push direto na `main`; uma Issue por entrega verificável e uma branch por Issue; nada de branches permanentes `backend`, `frontend` ou `ai`; não misture funcionalidades independentes no mesmo PR. Detalhes em [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Passo 1 — Escolher a Issue e completar a spec

No GitHub Project, selecione uma Issue atribuída a você. A Issue **é a spec** da tarefa (fluxo SDD, [`AGENTS.md`](AGENTS.md) §3): confira objetivo, requisitos, integração, fora do escopo e critérios de aceitação. Se algo estiver indefinido, pergunte nos comentários **antes de começar**, e preencha a seção "Plano". Mude o status no Project para *In progress*.

### Passo 2 — Criar sua branch a partir de `main`

```bash
git switch main
git pull origin main
git switch -c feat/backend-12-login
```

**Formato:** `tipo/area-numero-descricao-curta`. Tipos: `feat` (funcionalidade), `fix` (correção), `docs` (documentação), `chore` (organização/configuração) e `refactor` (reestruturação sem alterar comportamento). Áreas: `backend`, `frontend`, `ai`, `docs` e `repo`.

### Passo 3 — Implementar e testar localmente

Altere apenas os arquivos da tarefa, seguindo a spec e os templates de integração. Antes de registrar o trabalho:

1. Execute o módulo modificado e os testes disponíveis.
2. Confira cada critério de aceitação da Issue.
3. Revise os arquivos alterados com `git status` e `git diff`.
4. Confirme que não há credenciais nem arquivos gerados no commit.

### Passo 4 — Fazer commit e publicar a branch

```bash
git status
git add backend/
git commit -m "feat(backend): implementa login"
git push -u origin feat/backend-12-login
```

O `git add backend/` é **apenas um exemplo**: inclua somente os arquivos da sua tarefa.

### Passo 5 — Abrir um Pull Request (PR)

No GitHub, clique em **Compare & pull request** (ou **Pull requests → New pull request**) e defina:

- **Base:** `main`; **Compare:** sua branch.
- **Título:** no formato de commit (ex.: `feat(backend): login de usuários`).
- **Descrição:** o template do PR, com o que foi feito, como testar, os resultados dos testes e `Closes #12` (troque pelo número certo).
- **Revisor:** outro membro autorizado ou o responsável técnico.

Mude o status no Project para *In review*. **PR aberto não é tarefa finalizada:** ela termina após revisão e merge (Squash and Merge).

### Passo 6 — Atualizar seu repositório local

```bash
git switch main
git pull origin main
git branch -D feat/backend-12-login   # só depois de confirmar que o PR foi integrado
```

**Resumo:** `Issue (spec) → branch → implementação → testes locais → commit/push → Pull Request → revisão → Squash and Merge → Issue concluída`.

## 6. CI e problemas comuns

Cada PR passa por dois workflows do GitHub Actions, e o merge exige todos os checks verdes:

| Workflow | Check | O que confere |
|---|---|---|
| Regras do PR | Regras do CONTRIBUTING | Título `tipo(area): descrição`, branch `tipo/area-numero-descricao`, `Closes #N` na descrição e commits do aluno, sem coautoria nem rodapé de IA. |
| Documentação | Markdown (markdownlint) | Estilo dos `.md`. Rode antes do push: `npx markdownlint-cli2@0.23.2 "**/*.md"`. |
| Documentação | Links (lychee) | Links e âncoras dos `.md`. |
| Documentação | Workflows (actionlint) | Sintaxe dos workflows. |

| Problema | Solução |
|---|---|
| `Permission denied (publickey)` no push/pull | Configure uma chave SSH e adicione-a à sua conta ([documentação do GitHub](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh)). |
| Push para `main` rejeitado | Esperado: crie uma branch `tipo/area-numero-descricao` e abra um PR. |
| Check **Regras do CONTRIBUTING** falhou | Leia o log do check. Título e `Closes #N` se corrigem editando o PR. Para a branch, renomeie (`git branch -m <novo-nome>`), publique (`git push -u origin <novo-nome>`) e abra um novo PR. Para tirar um trailer `Co-authored-by` de IA, reescreva a mensagem dos commits (`git commit --amend` ou `git rebase -i main` com `reword`) e faça `git push --force-with-lease`. |
| Check **Markdown** ou **Links** falhou | Corrija o que o log aponta e faça um novo push. Um link externo fora do ar pode ser temporário: rode o check de novo antes de alterar o texto. |
| Arquivos alterados só por fim de linha | O `.gitattributes` normaliza para LF; rode `git add --renormalize .` em uma branch própria. |
| `.env` aparece no `git status` | Não deve ocorrer (está no `.gitignore`). Se já foi versionado, remova com `git rm --cached .env` e avise o responsável técnico para trocar as credenciais. |

## 7. Documentação

| Documento | Conteúdo |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Regras para alunos e assistentes de IA: SDD, boas práticas, templates de Issue, autoria e branch/commit/PR. O [`CLAUDE.md`](CLAUDE.md) só o importa. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Convenções de Issues, branches, commits, PRs, revisão e integração. |
| READMEs dos módulos | Stack, comandos e templates de integração: [`backend/`](backend/README.md), [`frontend/`](frontend/README.md) e [`ai/`](ai/README.md). |
| [`SECURITY.md`](SECURITY.md) | Como reportar vulnerabilidades e dados expostos de forma privada. |
| [Protótipos no Figma](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=47-2) | Estudos de UI/UX das telas da plataforma (acesso conforme permissões do arquivo). |

## 8. Licença e citação

- **Código:** [Apache License 2.0](LICENSE).
- **Documentação** (arquivos `.md`): [Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](LICENSE-DOCS).

Para citar o projeto em trabalhos acadêmicos, use os metadados de [`CITATION.cff`](CITATION.cff) ou o botão **Cite this repository** na página do repositório.
