# frontend/

Páginas, componentes, navegação, dashboards, gamificação e experiência do usuário do Projeto Horizonte.

- Chama **somente o Backend**, sempre por `/api/...` (o proxy repassa ao `API_BASE_URL`). Nunca chama a IA diretamente e não guarda segredos.
- Pode usar **dados simulados** até o endpoint existir, no mesmo formato da seção "Integração" de [`../backend/README.md`](../backend/README.md#integração-template).
- **Objetivo atual: MVP.** Só o suficiente para testar o backend e a IA (acesso, assistente e documentos).
- **Design system e layout base prontos** (menu lateral, barra superior, botão, campo e cartão). As páginas ainda são provisórias: implementar o conteúdo de cada tela do Figma é tarefa da equipe de frontend.

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
| Estilo | Tailwind CSS 4 (plugin `@tailwindcss/vite`), com os tokens do Figma em `src/estilos/tokens.css` |
| Fonte | Inter, pelo `@fontsource/inter` (pesos 400, 500, 600 e 700, sem Google Fonts) |
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
│   ├── assets/icones/     # Marca e ícones baixados do Figma (SVG)
│   ├── componentes/       # Layout (menu e barra superior), Botao, Campo e Cartao
│   ├── estilos/           # tokens.css: cores, tipografia e sombra do design system
│   └── paginas/           # Uma página por tela do Figma (hoje, provisórias)
└── vite.config.ts         # Lê o .env da raiz; proxy /api → API_BASE_URL
```

## Design system

Tudo vem do Figma ([Design system · Onboarding](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=173-1796)) e fica em **um lugar só**: [`src/estilos/tokens.css`](src/estilos/tokens.css). Nas telas, use as classes do Tailwind geradas pelos tokens e **nunca escreva uma cor solta** (`#...`).

| Token (`tokens.css`) | Classes | Exemplo de uso |
|---|---|---|
| Cores: `nav`, `brand`, `brandHover`, `brandSoft`, `assist`, `assistSoft`, `canvas`, `panel`, `text`, `muted`, `positive`, `line`, `input`, `inverse`, `error` | `bg-brand`, `text-muted`, `border-line` | Fundo do botão, texto secundário, bordas |
| Tipografia: `display`, `h1`, `h2`, `h3`, `body`, `label`, `small`, `button` | `text-h1`, `text-body`, `text-label` | Cada classe já traz tamanho, altura de linha, peso e espaçamento |
| Sombra: `painel` | `shadow-painel` | Cartões |

Espaçamentos (8, 12, 24, 32, 48 e 64 px) e raios (8, 12 e 16 px) do Figma já existem no Tailwind padrão (`p-2`, `p-3`, `p-6`, `rounded-lg`, `rounded-xl`, `rounded-2xl`). Para um token novo, adicione-o em `@theme` no `tokens.css`.

**Componentes reutilizáveis** (`src/componentes/`):

| Componente | Uso |
|---|---|
| `Layout` | Menu lateral e barra superior de todas as telas. Para uma tela nova, acrescente o item em `MENU`. Busca e notificações são só visuais. |
| `Botao` | `<Botao>Continuar</Botao>` (primário) ou `<Botao variante="secundario">`. Aceita as props de um `<button>`, inclusive `disabled`. |
| `Campo` | `<Campo placeholder="…" />`; `erro` marca o estado de erro. Aceita as props de um `<input>`. |
| `Cartao` | Painel branco com raio 16, padding 24 e sombra. Aceita `className` para ajustes de layout. |

Os ícones do menu ficam em `src/assets/icones/`, baixados do Figma. Ao precisar de um ícone novo, baixe-o do Figma para essa pasta em vez de redesenhá-lo.

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
