# backend/

API pública, autenticação, persistência, regras de negócio e gamificação do Projeto Horizonte. É o único módulo que o Frontend chama e o único que chama a IA.

## Stack

| Camada | Escolha |
|---|---|
| Linguagem e servidor | Node.js, TypeScript, Express |
| Banco de dados | PostgreSQL (Neon) em `DATABASE_URL`, o mesmo em que a IA guarda os vetores |
| ORM e migrações | Prisma ORM e Prisma Migrate |
| Validação e segurança | Zod (entrada), JWT (`JWT_SECRET`) e bcrypt (senhas) |
| Documentação da API | Swagger / OpenAPI, gerada a partir dos endpoints implementados |
| Testes | Vitest e Supertest |
| Deploy | [Render](https://render.com/) |

A spec de um endpoint é escrita **antes** na Issue, seguindo o modelo da seção "Integração". Depois de implementado, ele aparece no Swagger, que passa a ser a referência do endpoint pronto.

## Execução e testes

*A definir na Issue do esqueleto do backend* (versão do Node.js, instalação, migrações, execução e testes).

## Integração (template)

**Frontend → Backend**, HTTP/JSON. Cada endpoint novo é especificado com o modelo abaixo na seção "Integração" da Issue (fase "Especificar" do SDD) e revisado pelo Frontend. O que todos os módulos usam, como o `GET /health` e o formato de erro, fica registrado aqui.

### Modelo de endpoint

````markdown
### `MÉTODO /caminho`

O que faz e quem pode chamar (colaborador, gestor, administrador).

Autenticação: pública ou JWT (`Authorization: Bearer <token>`); perfis permitidos.

Requisição:
```json
{ "campo": "valor" }
```

Resposta `200`:
```json
{ "campo": "valor" }
```

Erros: `400` (...), `401` (...), `404` (...).
````

### `GET /health`

Resposta `200`:

```json
{ "status": "ok" }
```

### Formato de erro comum

Usado pelo Backend e pela IA em toda resposta com status `4xx` ou `5xx`:

```json
{
  "erro": {
    "codigo": "DOCUMENTO_NAO_ENCONTRADO",
    "mensagem": "Texto legível para o usuário.",
    "detalhes": {}
  }
}
```

`codigo` é estável e em `MAIUSCULAS_COM_SUBLINHADO`; o Frontend decide o que mostrar a partir dele, não da `mensagem`. Mudar ou remover um campo de um endpoint já usado exige revisão das equipes afetadas.
