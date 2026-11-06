# frontend/

Páginas, componentes, navegação, dashboards, gamificação e experiência do usuário do Projeto Horizonte.

- Chama **somente o Backend**, sempre por `/api/...` (o proxy repassa ao `API_BASE_URL`). Nunca chama a IA diretamente e não guarda segredos.
- Pode usar **dados simulados** até o endpoint existir, no mesmo formato da seção "Integração" de [`../backend/README.md`](../backend/README.md#integração-template).
- **Objetivo atual: MVP.** Só o suficiente para testar o backend e a IA (acesso, assistente e documentos).
- **O esqueleto não tem design.** As páginas são provisórias e sem estilo: implementar as telas e o design system do Figma é tarefa da equipe de frontend.

## Figma

| O quê | Link |
|---|---|
| Fluxo de navegação | [User Flow](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=4-14) |
| Protótipo (todas as telas) | [Prototipação](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=47-2) |
| Design system | [Design system · Onboarding](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=173-1796) |

Telas do MVP: 01 · Acesso institucional, 02 · Privacidade / Modal, 03 · Boas-vindas, 09 · Minha trilha e 19 · IA — resposta com fonte. Cada página provisória indica a tela do Figma correspondente.

## Stack

| Camada | Escolha |
|---|---|
| Base | React 19, TypeScript, Vite 8 |
| Navegação | React Router |
| Formulários e validação | React Hook Form e Zod (entram com a tela de acesso) |
| Estado | Zustand (entra com a sessão do usuário) |
| Acesso à API | Fetch API, em `src/api/` (TanStack Query opcional) |
| Estilo | A definir pela equipe, a partir do design system do Figma |
| Testes | **Mínimos:** um teste de fumaça com Vitest e React Testing Library. Playwright fica para depois. |
| Deploy | [Vercel](https://vercel.com/) |

## Estrutura

```text
frontend/
├── src/
│   ├── main.tsx           # Ponto de entrada
│   ├── App.tsx            # Rotas (cada tela nova entra aqui)
│   ├── App.test.tsx       # Teste de fumaça
│   ├── api/               # cliente.ts (fetch + erro comum) e uma função por endpoint
│   ├── componentes/       # Layout (menu, sem estilo) e componentes reutilizáveis
│   └── paginas/           # Uma página por tela do Figma (hoje, provisórias)
└── vite.config.ts         # Lê o .env da raiz; proxy /api → API_BASE_URL
```

## Execução e testes

Pré-requisito: [Node.js](https://nodejs.org/) 24 ou mais recente. As variáveis vêm do `.env` da **raiz** do repositório.

```bash
cd frontend
npm install
npm run dev          # http://localhost:3000
npm test             # teste de fumaça
npm run build        # checa os tipos e gera a versão de produção
```

**Com ou sem o backend:** com `VITE_USAR_DADOS_SIMULADOS=true` no `.env`, as telas usam dados simulados e funcionam sem o backend. Com `false`, as chamadas vão para o backend em `API_BASE_URL` (suba o backend com `npm run dev` na pasta `backend/`). A visão geral mostra "API no ar" quando a conexão está certa.

**Para criar uma tela:** implemente a página em `src/paginas/` seguindo a tela do Figma, registre a rota em `src/App.tsx` (e no menu de `src/componentes/Layout.tsx`, se for o caso) e crie a função do endpoint em `src/api/`, com a versão simulada ao lado (veja `src/api/saude.ts`). Confira o resultado no navegador e, para os endpoints, no Swagger do backend (`/docs`).
