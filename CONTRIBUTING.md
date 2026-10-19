# Como contribuir com o Projeto Horizonte

Este documento resume as regras de colaboração. O passo a passo detalhado, com exemplos, está no [README](README.md#3-fluxo-de-trabalho-do-aluno-da-issue-à-entrega).

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

Áreas: `backend`, `frontend`, `ai`, `contracts`, `docs`, `infra` (ou `repo` para a estrutura geral do repositório).

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
docs(contracts): documenta endpoint de autenticação
chore(infra): adiciona serviço do backend ao compose
```

- Inclua **somente** os arquivos da sua tarefa (`git add <caminho>`; evite `git add .` sem revisar).
- Antes de cada commit, revise `git status` e `git diff`.
- **Nunca** versione senhas, tokens, chaves de API ou arquivos `.env` reais. Use o [`.env.example`](.env.example).

## 4. Pull Requests

1. Publique a branch: `git push -u origin <sua-branch>`.
2. Abra o PR com **base `main`** e **compare** na sua branch.
3. Título no formato de commit (ex.: `feat(backend): login de usuários`).
4. Preencha o template: descrição, como testar, **resultados dos testes locais** e `Closes #<número>`.
5. Solicite revisão a outro membro autorizado ou ao responsável técnico.

Regras:

- Não misturar funcionalidades independentes no mesmo PR.
- Mudanças em `contracts/` exigem revisão das equipes afetadas.
- **CI (GitHub Actions):** cada PR passa por dois workflows, e o merge na `main` exige que todos os checks estejam verdes:
  - **Regras do PR:** título `tipo(area): descrição`, branch `tipo/area-numero-descricao` e `Closes #N` na descrição. Se falhar, corrija o título ou a descrição no próprio PR, ou renomeie a branch.
  - **Documentação:** lint de Markdown, links quebrados, validade dos workflows e do `compose.yaml`.
- Os testes de cada módulo ainda **não** rodam no CI: quem abre o PR executa os testes localmente e apresenta as evidências. Para rodar as verificações do CI antes do push, veja [`docs/DEVELOPMENT.md` §4](docs/DEVELOPMENT.md#4-execução-e-testes).
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
- [ ] Contratos e documentação foram atualizados, quando aplicável.
- [ ] O Pull Request referencia a Issue correta e foi revisado.
- [ ] O PR foi integrado na `main` e a Issue foi concluída no GitHub Project.

## 7. Desenvolvimento assistido por IA

Ao usar o Claude Code (ou outro assistente), as mesmas regras valem: Issue, branch, PR revisado e nenhum segredo no Git. O [`CLAUDE.md`](CLAUDE.md) orienta o agente sobre quais documentos ler e atualizar; mantenha-o atualizado quando criar documentos ou seções novas. O código gerado por IA é responsabilidade de quem abre o PR e deve ser revisado e testado como qualquer outro.

**Pasta `context/` (local):** cada colaborador pode criar uma pasta `context/` na raiz e colocar ali documentos de apoio (PDFs, anotações, especificações) para o assistente ler durante uma tarefa. Ela está no `.gitignore` e nunca é versionada. Se um documento precisar fazer parte do projeto, abra uma Issue e inclua o arquivo no local adequado (`docs/`, `contracts/` ou módulo) via PR. Evite colocar dados pessoais ou confidenciais sem necessidade.

## Resumo

`Issue → branch → implementação → testes locais → commit/push → Pull Request → revisão → Squash and Merge → Issue concluída`
