# frontend/

Páginas, componentes, navegação, dashboards, gamificação e experiência do usuário do Projeto Horizonte.

- Chama **somente o Backend**, no endereço `API_BASE_URL`, nunca a IA diretamente, e não guarda segredos.
- Pode usar **dados simulados (mocks)** até a API existir, seguindo os templates da seção "Integração" de [`../backend/README.md`](../backend/README.md#integração-template).
- Telas e fluxos: protótipos no [Figma](https://www.figma.com/design/7bFY4B5w0e5HukbLc3xB5F/Estudos-UI-UX---Sistemas-de-treinamento?node-id=47-2).

## Stack

| Camada | Escolha |
|---|---|
| Base | React, TypeScript, Vite |
| Navegação | React Router |
| Formulários e validação | React Hook Form e Zod |
| Estado | Zustand |
| Acesso à API | Fetch API (TanStack Query opcional, para cache e estados de carregamento) |
| Testes | Vitest e React Testing Library (unidade e componentes); Playwright (ponta a ponta) |
| Deploy | [Vercel](https://vercel.com/) |

## Execução e testes

*A definir na Issue do esqueleto do frontend* (versão do Node.js, instalação, execução e testes).
