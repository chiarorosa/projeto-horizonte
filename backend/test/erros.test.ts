import express from "express";
import request from "supertest";
import { describe, expect, it } from "vitest";
import { z } from "zod";
import { createApp } from "../src/app.js";
import { AppError, tratarErro } from "../src/erros.js";

// App mínimo para provocar cada tipo de erro.
function appQueLanca(erro: unknown) {
  const app = express();
  app.get("/falha", () => {
    throw erro;
  });
  app.use(tratarErro);
  return app;
}

describe("formato de erro comum", () => {
  it("rota inexistente responde 404", async () => {
    const res = await request(createApp()).get("/nao-existe");

    expect(res.status).toBe(404);
    expect(res.body).toEqual({
      erro: { codigo: "ROTA_NAO_ENCONTRADA", mensagem: "Rota não encontrada: GET /nao-existe", detalhes: {} },
    });
  });

  it("JSON malformado responde 400", async () => {
    const res = await request(createApp()).post("/health").set("Content-Type", "application/json").send("{ruim");

    expect(res.status).toBe(400);
    expect(res.body.erro.codigo).toBe("REQUISICAO_INVALIDA");
  });

  it("AppError usa o status e o código informados", async () => {
    const res = await request(appQueLanca(new AppError(409, "EMAIL_JA_CADASTRADO", "E-mail já cadastrado."))).get("/falha");

    expect(res.status).toBe(409);
    expect(res.body).toEqual({ erro: { codigo: "EMAIL_JA_CADASTRADO", mensagem: "E-mail já cadastrado.", detalhes: {} } });
  });

  it("erro de validação do Zod responde 400 com os campos inválidos", async () => {
    const resultado = z.object({ email: z.email() }).safeParse({ email: "x" });
    const res = await request(appQueLanca(resultado.error)).get("/falha");

    expect(res.status).toBe(400);
    expect(res.body.erro.codigo).toBe("REQUISICAO_INVALIDA");
    expect(res.body.erro.detalhes.campos).toHaveProperty("email");
  });

  it("erro inesperado responde 500 sem expor a mensagem interna", async () => {
    const res = await request(appQueLanca(new Error("senha do banco: 123"))).get("/falha");

    expect(res.status).toBe(500);
    expect(res.body).toEqual({ erro: { codigo: "ERRO_INTERNO", mensagem: "Erro interno do servidor.", detalhes: {} } });
  });
});
