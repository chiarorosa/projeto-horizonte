# Como contribuir com o Projeto Horizonte

Este documento resume as regras de colaboração. O passo a passo detalhado, com exemplos, está no [README](README.md#5-fluxo-de-trabalho-do-aluno-da-issue-à-entrega).

> **Regra principal:** cada tarefa tem sua própria Issue e branch. **Ninguém faz push diretamente na `main`**: toda integração ocorre por Pull Request revisado.

## 1. Issues

- Uma Issue por **entrega verificável**. Documentação ou manutenção sem Issue prévia exige abrir uma Issue antes de desenvolver.
- Use os templates disponíveis (**Tarefa** ou **Bug**) e preencha objetivo, critérios de aceitação, dependências e módulos envolvidos.
- Leia a Issue antes de começar. Dúvidas vão nos **comentários da Issue**, antes de iniciar o desenvolvimento.
- Mantenha o andamento atualizado no GitHub Project.

## 2. Branches

Fluxo **GitHub Flow**: apenas `main` é permanente; cada Issue gera uma branch temporária criada a partir da `main` atualizada.

**Formato:** `tipo/area-numero-descricao-curta`

| Tipo | Uso |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `chore` | Organização, configuração, manutenção |
| `refactor` | Reestruturação sem alterar comportamento |

Áreas: `backend`, `frontend`, `ai`, `docs` (documentação) ou `repo` (estrutura do repositório, CI e templates).

Exemplos: `feat/backend-12-login`, `feat/frontend-15-tela-login`, `fix/backend-21-validacao-token`.

```bash
git switch main
git pull origin main
git switch -c feat/backend-12-login
```

**Não** usar branches permanentes `backend`, `frontend` ou `ai`.

## 3. Commits

Commits pequenos, no formato [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

```text
tipo(area): descrição no presente, em minúsculas
```

Exemplos:

```text
feat(backend): implementa login
fix(frontend): corrige validação do formulário de cadastro
docs(backend): documenta endpoint de autenticação
chore(repo): ajusta template de Issue
```

- Inclua **somente** os arquivos da sua tarefa (`git add <caminho>`; evite `git add .` sem revisar).
- Antes de cada commit, revise `git status` e `git diff`.
- **Nunca** versione senhas, tokens, chaves de API ou arquivos `.env` reais. Use o [`.env.example`](.env.example).

## 4. Pull Requests

1. Publique a branch: `git push -u origin <sua-branch>`.
2. Abra o PR com **base `main`** e **compare** na sua branch.
3. Título no formato de commit (ex.: `feat(backend): login de usuários`).
4. Preencha o template: descrição, como testar, **resultados dos testes locais**, `Closes #<número>` e a linha `Continuação:`.
5. **Continuação:** o que ficou para depois vira Issue antes do merge (template Tarefa, citando a Issue original em "Dependências") e entra na linha `Continuação: #12, #13`. Se a entrega está completa, `Continuação: Nenhuma`. Próximos passos escritos só no PR somem do Project quando o merge fecha a Issue.
6. Solicite revisão a outro membro autorizado ou ao responsável técnico.

Regras:

- Não misturar funcionalidades independentes no mesmo PR.
- Mudanças na integração entre módulos (seção "Integração" dos READMEs de `backend/` e `ai/`) exigem revisão das equipes afetadas.
- **CI (GitHub Actions):** cada PR passa por dois workflows, e o merge na `main` exige que todos os checks estejam verdes:
  - **Regras do PR:** título `tipo(area): descrição`, branch `tipo/area-numero-descricao`, `Closes #N` na descrição, `Continuação:` com Issues abertas ou `Nenhuma` e autoria do aluno (§7). Se falhar, o log do check diz o que corrigir.
  - **Documentação:** lint de Markdown, links quebrados, validade dos workflows.
- Depois do merge, o workflow **Continuação** comenta em cada Issue fechada pelo PR com o link das Issues de continuação.
- Se o merge trouxe migrações (`backend/prisma/migrations/`), o workflow **Migrações (production)** aguarda a aprovação da coordenação e as aplica na `production` do Neon (README §4).
- Os testes de cada módulo ainda **não** rodam no CI: quem abre o PR executa os testes localmente e apresenta as evidências. Para rodar o lint de Markdown antes do push, veja o [`AGENTS.md`](AGENTS.md) §8.
- **PR aberto não é tarefa finalizada.** Ela termina após revisão e merge.

## 5. Revisão e integração

- O revisor verifica: aderência à Issue, contratos respeitados, testes informados, ausência de credenciais e de arquivos gerados.
- O autor corrige as observações na mesma branch (novos commits).
- Após aprovação: **Squash and Merge** e exclusão da branch remota.

Depois do merge, atualize o repositório local:

```bash
git switch main
git pull origin main
git branch -d feat/backend-12-login   # use -D somente após confirmar que o PR foi integrado
```

## 6. Critérios mínimos para considerar uma entrega concluída

- [ ] A Issue tem objetivo e critérios de aceitação atendidos.
- [ ] A implementação foi feita em branch própria, não diretamente na `main`.
- [ ] Foram executadas verificações/testes locais relevantes, com resultados descritos no PR, e os checks do CI estão verdes.
- [ ] O código não contém segredos, credenciais nem artefatos indevidos.
- [ ] Os commits são do aluno, sem coautoria de IA; o uso de IA, se houve, está declarado no PR (§7).
- [ ] Contratos e documentação foram atualizados, quando aplicável.
- [ ] O Pull Request referencia a Issue correta e foi revisado.
- [ ] O que ficou pendente está em Issues de continuação abertas, listadas no PR.
- [ ] O PR foi integrado na `main` e a Issue foi concluída no GitHub Project.

## 7. Desenvolvimento assistido por IA

Ao usar um assistente de IA (Claude Code, Codex, GitHub Copilot, Cursor ou outro), as mesmas regras valem: Issue, branch, PR revisado e nenhum segredo no Git. O [`AGENTS.md`](AGENTS.md) orienta o assistente sobre quais documentos ler e atualizar; mantenha-o atualizado quando criar documentos ou seções novas. O [`CLAUDE.md`](CLAUDE.md) só o importa, para o Claude Code.

**Autoria:** a contribuição é sempre **do aluno**, que responde pelo código e pelo texto gerados com IA, os revisa e os testa como qualquer outro.

- Commits, pushes, Issues e PRs são feitos com a sua conta e o seu nome no git. Não use contas de bot nem agentes autônomos que abrem PRs.
- Sem trailers de coautoria de IA (`Co-authored-by: <ferramenta de IA>`) e sem rodapés automáticos ("Generated with …") em commits ou PRs. O check **Regras do CONTRIBUTING** reprova o PR que tiver qualquer um deles. Coautoria entre pessoas da equipe continua permitida.
- Declare o uso de IA **apenas** com uma linha em "Observações", na descrição do PR: `Desenvolvimento assistido por IA (<ferramenta>).`
- Desligue a coautoria automática da sua ferramenta. No Claude Code, coloque `"attribution": { "commit": "", "pr": "" }` no seu `~/.claude/settings.json` pessoal; nas outras, procure a opção equivalente nas configurações.

**Pasta `context/` (local):** cada colaborador pode criar uma pasta `context/` na raiz e colocar ali documentos de apoio (PDFs, anotações, especificações) para o assistente ler durante uma tarefa. Ela está no `.gitignore` e nunca é versionada. Se um documento precisar fazer parte do projeto, abra uma Issue e inclua o arquivo no local adequado (README ou módulo) via PR. Evite colocar dados pessoais ou confidenciais sem necessidade.

## Resumo

`Issue → branch → implementação → testes locais → commit/push → Pull Request → revisão → Squash and Merge → Issue concluída`
