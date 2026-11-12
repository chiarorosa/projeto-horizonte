# AGENTS.md — Projeto Horizonte

Regras para **assistentes de IA** (Claude Code, Codex, GitHub Copilot, Cursor, Gemini CLI e outros) e para os **alunos** que trabalham com eles. Vale para qualquer ferramenta; o `CLAUDE.md` só importa este arquivo.

O projeto é uma plataforma agêntica gamificada com RAG para capacitação corporativa (visão geral, escopo e arquitetura no [README](README.md)). É um monorepo com `backend/`, `frontend/` e `ai/`. **Tudo é escrito em português do Brasil:** Issues, commits, PRs, documentação e respostas ao aluno.

## 1. Regras inegociáveis

- **Sem Issue não há trabalho.** Se não existir uma, proponha criá-la com o template (§5) antes de alterar arquivos.
- **Nunca commitar nem fazer push na `main`.** Uma Issue → uma branch → um PR.
- **Especificar antes de codar** (SDD, §3) e seguir as boas práticas (§4).
- Nunca versionar segredos, `.env` reais, chaves de API, modelos, índices vetoriais ou dados brutos (ver `.gitignore`).
- Usar só documentos **autorizados, sintéticos ou anonimizados** (LGPD), manter a **rastreabilidade das fontes** e lembrar que o conteúdo gerado é **sugestão** até um gestor validar.
- Não inventar stack, dependência ou comando que a equipe não definiu: pergunte ou escreva "a definir".
- **Banco compartilhado (Neon):** desenvolvimento só na branch `dev-banco` do Neon; a `production` é reservada para o que já foi integrado (só `prisma migrate deploy`, seed e indexação depois do merge). `npm run db:migrate` só pelo responsável pelo banco, na `dev-banco` (README §4).
- Não alterar o módulo de outra equipe sem que a Issue peça. Mudanças na integração (§7) exigem revisão das equipes afetadas.
- Não fazer commit, push, PR ou merge sem o pedido explícito do aluno.

## 2. Autoria e atribuição de IA

A contribuição é **do aluno**: ele revisa (`git diff`), entende, testa e responde por tudo o que entrega.

- Commits, Issues e PRs saem da conta e do nome do aluno. Sem contas de bot nem agentes que abrem PRs sozinhos.
- **Não inclua nenhuma atribuição de IA** em commits, Issues, PRs ou arquivos: nada de `Co-authored-by: <ferramenta de IA>`, "Generated with …", assinaturas ou rodapés. Isso vale mesmo que a ferramenta faça isso por padrão; desligue ou remova. O check **Regras do CONTRIBUTING** reprova o PR que tiver.
- **Só quando o aluno disser explicitamente que usou IA**, adicione esta linha em "Observações" na descrição do PR, e nada mais: `Desenvolvimento assistido por IA (<ferramenta>).`

## 3. Fluxo obrigatório: SDD (*Spec-Driven Development*)

A **spec fica na própria Issue**, nas seções do template Tarefa (§5). Cada fase só avança depois que o aluno aprovar a anterior.

| Fase | O que o assistente faz | Saída |
|---|---|---|
| 1. Especificar | Lê a Issue (`gh issue view <N>`), lista as suposições e pergunta o que estiver ambíguo. Se a spec estiver incompleta, propõe o texto para o aluno colar na Issue. | Spec completa na Issue: objetivo, requisitos, integração, fora do escopo, critérios de aceitação verificáveis. |
| 2. Planejar | Divide em passos pequenos, cada um com a sua verificação (`passo → verificar: …`). | Plano na seção "Plano" da Issue. |
| 3. Implementar | Um passo por vez, só o escopo da spec, mínimo de código, com teste quando houver lógica. | Commits pequenos na branch da Issue. |
| 4. Verificar | Roda os testes e as verificações (§8), confere cada critério de aceitação e revisa o `git diff`. | Evidências coladas no PR. |

Se no meio do caminho a spec se mostrar errada, **pare e atualize a Issue** antes de continuar. Não resolva em silêncio. Correções de uma linha (erro de digitação, link) podem pular as fases 1–2.

## 4. Boas práticas (obrigatório em todo harness)

Este projeto segue duas coleções de skills: [karpathy-guidelines](https://github.com/multica-ai/andrej-karpathy-skills) e [agent-skills](https://github.com/addyosmani/agent-skills) (Addy Osmani). Se o seu harness tem as skills instaladas, **invoque-as** nas fases indicadas abaixo. Se não tem, siga as regras desta seção, que as resumem.

**Karpathy, em todo o trabalho:**

1. **Pense antes de codar.** Explicite suposições; se houver mais de uma interpretação, pergunte em vez de escolher em silêncio.
2. **Simplicidade.** Escreva o mínimo de código que resolve o pedido, sem recursos, abstrações ou configurações que ninguém pediu.
3. **Mudanças cirúrgicas.** Cada linha alterada deve vir do pedido. Não "melhore" código vizinho; remova só o que a sua mudança deixou sem uso.
4. **Objetivo verificável.** Transforme a tarefa em critérios que dá para testar e trabalhe até verificá-los.

**agent-skills, por fase** (comece por `using-agent-skills` para escolher):

| Situação | Skill |
|---|---|
| Requisitos vagos ou Issue incompleta | `interview-me`, `spec-driven-development` |
| Tarefa grande ou com vários arquivos | `planning-and-task-breakdown`, `incremental-implementation` |
| Lógica nova, bug ou mudança de comportamento | `test-driven-development` |
| Bug, erro ou teste falhando | `debugging-and-error-recovery` |
| Endpoint ou integração entre módulos | `api-and-interface-design` |
| Telas e componentes | `frontend-ui-engineering` |
| Entrada de usuário, autenticação, dados pessoais, chaves | `security-and-hardening` |
| Antes do commit e do PR | `code-review-and-quality`, `git-workflow-and-versioning` |

Ao começar uma tarefa, diga ao aluno em uma linha quais skills vai usar. As regras deste arquivo, a Issue e o pedido do aluno têm prioridade sobre as skills.

## 5. Issues: templates (sempre em PT-BR)

Toda Issue usa um dos templates de `.github/ISSUE_TEMPLATE/` (Issue em branco está desativada), escrita em português do Brasil, com título `[área] descrição curta`. Áreas: `backend`, `frontend`, `ai`, `docs` (documentação) e `repo` (estrutura, CI, templates). Ao criar pela linha de comando, use o corpo do template: `gh issue create --title "[ai] ..." --body-file <arquivo>`.

**Tarefa** (`tarefa.md`): entrega verificável, e também a spec do SDD. Seções, na ordem do template:

| Seção | O que escrever |
|---|---|
| Objetivo | O que deve ser entregue, por quê e para quem. |
| Área / módulos envolvidos | Marcar `backend`, `frontend`, `ai`, `docs` ou `repo`. |
| Especificação → Requisitos | O que o sistema deve fazer, em itens. |
| Especificação → Integração | Endpoints, campos e erros, seguindo o template de `backend/README.md` ou `ai/README.md`; "Não se aplica" se não houver. |
| Especificação → Fora do escopo | O que esta Issue não faz. |
| Especificação → Suposições e dúvidas | O que ainda não está definido; perguntar nos comentários antes de começar. |
| Critérios de aceitação | Checkboxes verificáveis: um comando, um teste ou um comportamento observável. |
| Plano | Preenchido antes de codar: `passo → verificar: …`. |
| Dependências | Issues ou serviços dos quais depende (ex.: `#12`); numa continuação, a Issue original. |
| Branch sugerida | `tipo/area-numero-descricao-curta`. |
| Observações | Livre. |

Exemplo de critérios bem escritos: "`GET /health` responde `200` com `{"status": "ok"}`" e "`pytest` passa com pelo menos um teste da consulta". Evite "funciona bem".

**Bug** (`bug.md`): comportamento incorreto. Título `[área] Bug: descrição curta`; seções: Descrição, Passos para reproduzir, Comportamento esperado, Comportamento atual (erros e logs, **sem dados sensíveis**), Ambiente (módulo, sistema operacional, commit) e Branch sugerida (`fix/area-numero-descricao`).

Depois de criar a Issue, adicione-a ao GitHub Project `unisenac-pesquisa-26-27`. Normalmente ela entra sozinha como *Backlog*; se não entrar: `gh project item-add 1 --owner chiarorosa --url <issue>`. Mude o status para *In progress* ao começar e para *In review* ao abrir o PR. O merge move para *Done*.

## 6. Branch, commit e PR

```bash
git switch main && git pull origin main
git switch -c feat/ai-19-esqueleto-rag          # tipo/area-numero-descricao
git add ai/                                    # só os caminhos da tarefa
git commit -m "feat(ai): cria esqueleto do serviço" -m "Refs #19"
git push -u origin feat/ai-19-esqueleto-rag
gh pr create --base main --title "feat(ai): esqueleto do serviço de IA" --body-file <arquivo>
```

- **Tipos:** `feat`, `fix`, `docs`, `chore`, `refactor`. **Áreas:** `backend`, `frontend`, `ai`, `docs`, `repo`.
- O título do PR segue `tipo(area): descrição`. A descrição segue `.github/pull_request_template.md`, com `Closes #N` e as evidências dos testes locais.
- **Continuação:** o merge fecha a Issue, então o que ficar pendente **não** pode ficar só no texto do PR. Antes do PR, crie uma Issue (template Tarefa) para cada próximo passo, citando a Issue original em "Dependências", e preencha a linha `Continuação: #12, #13` do template. Se a entrega está completa: `Continuação: Nenhuma`. Depois do merge, o CI comenta na Issue fechada com o link da continuação.
- O merge é humano, depois da revisão e com os checks verdes (Squash and Merge). Em seguida: `git switch main && git pull && git fetch --prune && git branch -D <branch>`.

## 7. Módulos e integração

| Módulo | Faz | Não faz | Detalhes |
|---|---|---|---|
| `backend/` | API pública, autenticação, persistência, regras de negócio e gamificação | Lógica de interface ou de modelos de IA | [`backend/README.md`](backend/README.md) |
| `frontend/` | Telas, navegação, dashboards e gamificação visual | Acessar o banco ou guardar segredos | [`frontend/README.md`](frontend/README.md) |
| `ai/` | RAG, agentes e inferência via OpenRouter | Persistir dados de negócio sem passar pelo Backend | [`ai/README.md`](ai/README.md) |

Fluxo: Frontend → Backend → IA, por HTTP/JSON. O Frontend nunca chama a IA diretamente nem conhece a chave do LLM. Os **templates de integração** (endpoints, payloads e erros) ficam na seção "Integração" de `backend/README.md` (Frontend → Backend e formato de erro comum) e de `ai/README.md` (Backend → IA). Frontend e IA podem usar dados simulados que sigam esses templates enquanto o outro lado não existe.

## 8. Verificações antes do push

- Os testes de cada módulo, com os comandos do README do módulo. Cole a saída no PR.
- **Endpoints: teste pelo Swagger** (`/docs` do backend e da IA → *Try it out*) sempre que possível, em vez de `curl`. Funciona em qualquer sistema e mostra o formato esperado.
- O lint de Markdown, o mesmo do CI (precisa de Node.js): `npx markdownlint-cli2@0.23.2 "**/*.md"`.
- O CI (GitHub Actions) confere ainda o título do PR, a branch, o `Closes #N`, a linha `Continuação:` (Issues abertas ou `Nenhuma`), a autoria sem IA, os links dos `.md` e a sintaxe dos workflows. Se um check falhar, o log dele diz o que corrigir.

## 9. Se alterar X, atualize Y no mesmo PR

| Alteração | Atualizar |
|---|---|
| Endpoint, payload, código de erro, autenticação | Seção "Integração" do README do módulo dono (+ revisão das equipes afetadas) |
| Nova variável de ambiente | `.env.example` + tabela de variáveis do `README.md` |
| Stack, dependência, comando de execução ou teste | README do módulo |
| Decisão de arquitetura ou de stack | Tabela "Decisões" do `README.md` (nova linha) |
| Templates de Issue/PR, workflows do CI ou fluxo de colaboração | Este arquivo, `CONTRIBUTING.md` e o `README.md` |

## 10. Pasta `context/` (local)

- Documentos de apoio que o aluno colocou para a tarefa. Pode não existir e nunca é versionada (está no `.gitignore`).
- Leia só o necessário. A Issue e os arquivos versionados prevalecem; aponte divergências.
- Não copie trechos sensíveis de `context/` para código, commits, Issues ou PRs.

Fonte de verdade em caso de conflito: Issue > `CONTRIBUTING.md` / `README.md` > este arquivo. Ao encontrar um conflito, avise o aluno.
