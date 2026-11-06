// Documentação OpenAPI da API, servida em /docs (Swagger UI).
// Ao implementar um endpoint, acrescente-o em `paths` no mesmo PR.
export const openapi = {
  openapi: "3.1.0",
  info: {
    title: "Projeto Horizonte — API",
    version: "0.1.0",
  },
  paths: {
    "/health": {
      get: {
        summary: "Verifica se a API está no ar",
        responses: {
          "200": {
            description: "API no ar",
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: { status: { type: "string", example: "ok" } },
                  required: ["status"],
                },
              },
            },
          },
        },
      },
    },
  },
  components: {
    schemas: {
      // Formato de erro comum, usado em toda resposta 4xx e 5xx.
      Erro: {
        type: "object",
        properties: {
          erro: {
            type: "object",
            properties: {
              codigo: { type: "string", example: "ROTA_NAO_ENCONTRADA" },
              mensagem: { type: "string" },
              detalhes: { type: "object" },
            },
            required: ["codigo", "mensagem", "detalhes"],
          },
        },
        required: ["erro"],
      },
    },
  },
};
