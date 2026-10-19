# Guia de desenvolvimento

Como preparar o ambiente local, configurar variáveis, executar e testar o Projeto Horizonte.

> As seções de cada módulo serão completadas pelas respectivas equipes quando a stack for definida (ver [ARCHITECTURE.md](ARCHITECTURE.md#5-decisões-arquiteturais)).

## 1. Pré-requisitos

| Ferramenta | Uso |
|---|---|
| [Git](https://git-scm.com/) | Controle de versão |
| Conta no GitHub com **chave SSH** configurada | Clonar, publicar branches e abrir PRs |
| [Docker](https://docs.docker.com/get-docker/) com Docker Compose | Execução integrada dos serviços (quando disponível) e verificações do CI localmente (§4) |
| [Node.js](https://nodejs.org/) (opcional) | Lint de Markdown local, o mesmo do CI (§4) |

Ferramentas específicas de cada módulo (ex.: versão de Node.js ou Python) serão listadas nas seções abaixo.

### Verificar o acesso SSH ao GitHub

```bash
ssh -T git@github.com
# Esperado: "Hi <usuario>! You've successfully authenticated..."
```

## 2. Configuração local

```bash
git clone git@github.com:chiarorosa/projeto-horizonte.git
cd projeto-horizonte
cp .env.example .env    # preencha os valores localmente
```

## 3. Variáveis de ambiente

As variáveis ficam no arquivo `.env` (não versionado). O [`.env.example`](../.env.example) lista todas, sem valores secretos.

| Variável | Módulo | Descrição |
|---|---|---|
| `APP_ENV` | todos | Ambiente de execução (`development`). |
| `BACKEND_PORT` | backend | Porta local da API. |
| `DATABASE_URL` | backend | URL de conexão com o banco de dados. |
| `JWT_SECRET` | backend | Segredo para assinatura de tokens. |
| `FRONTEND_PORT` | frontend | Porta local da interface. |
| `API_BASE_URL` | frontend | Endereço da API consumida pelo Frontend. |
| `AI_PORT` | ai | Porta local do serviço de IA. |
| `LLM_PROVIDER` | ai | Provedor de LLM utilizado. |
| `LLM_API_KEY` | ai | Chave de API do provedor de LLM. |

Ao adicionar uma variável: inclua-a no `.env.example` (sem valor real) e nesta tabela, no mesmo PR.

## 4. Execução e testes

### Execução integrada

```bash
docker compose up --build
```

> O `compose.yaml` ainda não possui serviços; eles serão adicionados conforme cada módulo disponibilizar seu Dockerfile.

### Verificações do CI

Cada PR passa por dois workflows do GitHub Actions (`.github/workflows/`), e o merge na `main` exige todos os checks verdes:

| Workflow | Check | O que confere |
|---|---|---|
| Regras do PR | Regras do CONTRIBUTING | Título `tipo(area): descrição`, branch `tipo/area-numero-descricao` e `Closes #N` na descrição ([CONTRIBUTING.md](../CONTRIBUTING.md) §2–§4). |
| Documentação | Markdown (markdownlint) | Estilo dos arquivos `.md`, conforme `.markdownlint-cli2.jsonc`. |
| Documentação | Links (lychee) | Links e âncoras dos arquivos `.md`, conforme `lychee.toml`. |
| Documentação | Workflows e compose.yaml | Sintaxe dos workflows (actionlint) e do `compose.yaml`. |

Para rodar as mesmas verificações antes do push (requer Node.js e Docker):

```bash
npx markdownlint-cli2@0.23.2 "**/*.md"
docker run --rm -v "$PWD:/input" -w /input lycheeverse/lychee:0.24.2 --config lychee.toml "**/*.md"
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.12 -color
docker compose -f compose.yaml config --quiet
```

### Backend

_A definir pela equipe de Backend: instalação de dependências, execução e testes._

### Frontend

_A definir pela equipe de Frontend: instalação de dependências, execução e testes._

### IA

_A definir pela equipe de IA: instalação de dependências, obtenção de modelos/dados, execução e avaliações._

## 5. Solução de problemas comuns

| Problema | Solução |
|---|---|
| `Permission denied (publickey)` ao fazer push/pull | Configure uma chave SSH e adicione-a à sua conta: [documentação do GitHub](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh). |
| Push para `main` rejeitado | Esperado: crie uma branch `tipo/area-numero-descricao` e abra um PR. |
| Check **Regras do CONTRIBUTING** falhou | Abra o log do check: ele diz o que corrigir. Título e `Closes #N` se corrigem editando o PR (o check roda de novo). Para a branch, crie outra com o nome certo (`git branch -m <novo-nome>` e `git push -u origin <novo-nome>`) e abra um novo PR. |
| Check **Markdown** ou **Links** falhou | Rode o comando correspondente em §4 ("Verificações do CI"), corrija e faça um novo push. Um link externo fora do ar pode ser temporário: rode o check de novo antes de alterar o texto. |
| `git branch -d` falha após o merge | Merges por squash não são reconhecidos; confirme que o PR foi integrado e use `git branch -D <branch>`. |
| Arquivos aparecem como alterados só por fim de linha | O `.gitattributes` normaliza para LF; rode `git add --renormalize .` em uma branch própria. |
| `.env` aparecendo no `git status` | Não deve ocorrer (está no `.gitignore`). Se já foi versionado, remova com `git rm --cached .env` e avise o responsável técnico para trocar as credenciais. |
