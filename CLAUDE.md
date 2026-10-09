# CLAUDE.md — Projeto Horizonte

Guia para o desenvolvimento assistido por IA. **Este arquivo é um índice:** não repete o conteúdo dos documentos, apenas indica o que ler, quando ler e o que atualizar. Leia somente as seções necessárias para a tarefa atual.

Projeto: plataforma agêntica gamificada com RAG para capacitação corporativa. Monorepo modular (`backend/`, `frontend/`, `ai/`, `contracts/`, `docs/`, `infra/`). Idioma do projeto: **português** (docs, commits, PRs, Issues).

## Regras inegociáveis

- Nunca commitar nem fazer push na `main`. Uma Issue → uma branch → um PR.
- Sem Issue não há trabalho: se não houver uma, proponha criá-la antes de alterar arquivos.
- Nunca versionar segredos, `.env` reais, modelos ou dados brutos (ver `.gitignore`).
- Não inventar stack, dependências ou comandos que as equipes ainda não definiram. Se for necessário, pergunte ou registre como "a definir".
- Não alterar módulos de outra equipe nem `contracts/` sem que a Issue peça isso explicitamente.
- Não há CI: execute localmente as verificações disponíveis e cole as evidências no PR.

## Índice de documentos: quando ler

| Situação | Ler |
|---|---|
| Iniciar qualquer tarefa | A Issue (`gh issue view <N>`) e esta página |
| Nome de branch, commit, PR, revisão | `CONTRIBUTING.md` §2–§5 |
| Verificar se a entrega está pronta | `CONTRIBUTING.md` §6 (critérios mínimos) |
| Entender módulos, limites e integrações | `docs/ARCHITECTURE.md` §2–§4 |
| Tomar ou consultar decisões técnicas (stack etc.) | `docs/ARCHITECTURE.md` §5 |
| Configurar ambiente, variáveis, rodar e testar | `docs/DEVELOPMENT.md` §1–§4 |
| Erro de git, SSH ou ambiente | `docs/DEVELOPMENT.md` §5 |
| Trabalhar dentro de um módulo | `<módulo>/README.md` |
| Integração entre módulos (API, schemas, erros) | `contracts/README.md` e os arquivos em `contracts/` |
| Visão geral, onboarding | `README.md` §1 e §5 |

Fonte de verdade em caso de conflito: Issue > `CONTRIBUTING.md` / `docs/` > este arquivo. Ao encontrar um conflito, aponte-o ao usuário.

## Fluxo de trabalho

1. **Issue**: `gh issue view <N>`. Confirme objetivo, critérios de aceitação e módulos. Registre dúvidas como comentário antes de começar.
2. **Branch**: `git switch main && git pull origin main && git switch -c tipo/area-N-descricao`.
3. **Implementar** só o escopo da Issue, atualizando a documentação afetada (matriz abaixo).
4. **Verificar**: rode o que estiver definido em `docs/DEVELOPMENT.md` §4 e revise `git status` e `git diff`.
5. **Commit**: `tipo(area): descrição`, com `git add` explícito por caminho e `Refs #N` no corpo.
6. **PR**: `git push -u origin <branch>` e depois `gh pr create --base main --body-file <arquivo>`, seguindo `.github/pull_request_template.md` e incluindo `Closes #N`.
7. **Merge** (humano, Squash and Merge), seguido de `git switch main && git pull && git fetch --prune && git branch -D <branch>`.

GitHub Project (`gh project`, requer permissão `project` no login do `gh`): ao começar, mova a Issue para *In progress*. O fechamento pelo merge move a Issue para *Done*.

## Matriz de atualização: se alterar X, atualize Y no mesmo PR

| Alteração | Atualizar |
|---|---|
| Endpoint, payload, código de erro, autenticação | `contracts/` (+ revisão das equipes afetadas) |
| Nova variável de ambiente | `.env.example` + `docs/DEVELOPMENT.md` §3 |
| Novo comando de execução ou teste, dependência ou pré-requisito | `docs/DEVELOPMENT.md` §1 / §4 |
| Novo serviço, porta ou Dockerfile | `compose.yaml`, `infra/` e `docs/DEVELOPMENT.md` |
| Escolha de stack ou mudança de arquitetura | `docs/ARCHITECTURE.md` §5 (nova linha de decisão) |
| Responsabilidade ou estrutura de um módulo | `<módulo>/README.md` e `docs/ARCHITECTURE.md` §2 |
| Fluxo de colaboração (branches, PR, revisão) | `CONTRIBUTING.md` (e `README.md` se for o resumo) |
| Novo documento ou seção importante | o índice desta página |

## Manutenção deste arquivo

- Mantenha-o curto: inclua ponteiros, não conteúdo. Se uma explicação passar de duas linhas, ela pertence a outro documento.
- Referencie seções (`§`), não números de linha.
- Preferências pessoais ficam em `CLAUDE.local.md` (não versionado).
